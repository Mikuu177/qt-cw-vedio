"""
Main Window - Iteration 2 Enhanced Version

Integrates all video editing features:
- Multi-clip timeline
- Markers for navigation
- Trim/cut functionality
- Export with quality options
- High contrast mode
- Undo/redo system
- Internationalization (en/zh) - Iteration 3
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QPushButton, QSlider, QLabel, QFileDialog, QStyle, QAction, QComboBox, QMessageBox, QDockWidget, QInputDialog, QToolBar, QDialog, QProgressBar
)
from PyQt5.QtCore import Qt, QSettings
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video.opencv_player import OpenCVVideoPlayer
from video.timeline import Timeline
from video.marker import MarkerManager
from ui.timeline_widget import TimelineWidget
from ui.export_dialog import ExportDialog
from ui.help_dialog import HelpDialog
from ui.inspector_panel import InspectorPanel
from ui.composition_bar import CompositionBar
from ui.select_clips_dialog import SelectClipsDialog
from utils.theme_manager import ThemeManager
from utils.command_stack import CommandStack, AddClipCommand, AddMarkerCommand
from video.ffmpeg_processor import FFmpegProcessor, FFmpegWorker
from utils.i18n_manager import i18n
# Auth dialogs
from ui.auth_dialogs import LoginDialog


class MainWindow(QMainWindow):
    """
    Enhanced main application window with video editing features.
    """

    def __init__(self, app, auth=None):
        super().__init__()
        self.app = app
        self.is_seeking = False
        self.in_point_ms = None  # Trim in point
        self.out_point_ms = None  # Trim out point
        self.trim_mode = False

        # Data models
        self.timeline = Timeline()
        self.marker_manager = MarkerManager()
        self.command_stack = CommandStack()
        self.selected_clip_id = None

        # FFmpeg processor
        self.ffmpeg_processor = FFmpegProcessor()
        self.ffmpeg_worker = None
        self.ffmpeg_workers = []  # keep multiple background workers alive

        # Program preview state
        self.program_mode = False
        self.program_order = []  # list of clip ids in order
        self.program_index = 0
        self.program_current_clip_id = None

        # Theme manager
        self.theme_manager = ThemeManager(app)

        # Settings
        self.settings = QSettings("XJCO2811", "VideoEditor")

        # Auth
        self.auth = auth

        self.init_ui()
        self.load_sample_video()
        self.update_undo_redo_state()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle(i18n.t("window.title", "Video Editor/Player - XJCO2811 (Iteration 2)"))
        self.setGeometry(100, 100, 1280, 900)

        # Central widget with splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Menu bar
        self.create_menu_bar()

        # Inspector dock (right)
        self.inspector_dock = QDockWidget(i18n.t("inspector.title", "Inspector"), self)
        self.inspector_dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.inspector = InspectorPanel(self)
        self.inspector_dock.setWidget(self.inspector)
        self.addDockWidget(Qt.RightDockWidgetArea, self.inspector_dock)

        # Connect inspector signals
        self.inspector.apply_inout.connect(self.on_inspector_apply_inout)
        self.inspector.rename_clip.connect(self.on_inspector_rename_clip)
        self.inspector.set_in_from_player.connect(self.on_inspector_set_in_from_player)
        self.inspector.set_out_from_player.connect(self.on_inspector_set_out_from_player)

        # Main splitter (video player + timeline)
        splitter = QSplitter(Qt.Vertical)

        # Top section: Video player and controls
        top_widget = QWidget()
        top_layout = QVBoxLayout()
        top_widget.setLayout(top_layout)

        # Video player
        self.video_player = OpenCVVideoPlayer()
        self.video_player.setMinimumSize(640, 480)
        top_layout.addWidget(self.video_player)

        # Connect signals
        self.video_player.positionChanged.connect(self.on_position_changed)
        self.video_player.durationChanged.connect(self.on_duration_changed)
        self.video_player.stateChanged.connect(self.on_state_changed)

        # Timeline slider with marker overlay
        timeline_container = QWidget()
        timeline_container_layout = QVBoxLayout()
        timeline_container_layout.setContentsMargins(0, 0, 0, 0)
        timeline_container.setLayout(timeline_container_layout)

        self.timeline_slider = QSlider(Qt.Horizontal)
        self.timeline_slider.setRange(0, 0)
        self.timeline_slider.sliderPressed.connect(self.on_slider_pressed)
        self.timeline_slider.sliderReleased.connect(self.on_slider_released)
        self.timeline_slider.sliderMoved.connect(self.on_slider_moved)
        timeline_container_layout.addWidget(self.timeline_slider)

        # Composition bar under slider
        self.composition_bar = CompositionBar(self)
        self.composition_bar.set_timeline(self.timeline)
        self.composition_bar.seekRequested.connect(self.on_composition_seek)
        timeline_container_layout.addWidget(self.composition_bar)

        top_layout.addWidget(timeline_container)

        # Time labels
        time_layout = QHBoxLayout()
        self.current_time_label = QLabel(i18n.t("label.current_time", "00:00"))
        self.total_time_label = QLabel(i18n.t("label.total_time", "00:00"))

        # Trim points indicators
        self.in_point_label = QLabel("")
        self.out_point_label = QLabel("")
        self.in_point_label.setStyleSheet("color: #00aa00; font-weight: bold;")
        self.out_point_label.setStyleSheet("color: #cc0000; font-weight: bold;")

        time_layout.addWidget(self.current_time_label)
        time_layout.addWidget(self.in_point_label)
        time_layout.addStretch()
        time_layout.addWidget(self.out_point_label)
        time_layout.addWidget(self.total_time_label)
        top_layout.addLayout(time_layout)

        # Control panel
        control_layout = self.create_control_panel()
        top_layout.addLayout(control_layout)

        splitter.addWidget(top_widget)

        # Bottom section: Multi-clip timeline
        self.timeline_widget = TimelineWidget(self.timeline, self.marker_manager)
        self.timeline_widget.setMinimumHeight(200)
        self.timeline_widget.clip_selected.connect(self.on_timeline_clip_selected)
        self.timeline_widget.clip_activated.connect(self.on_timeline_clip_activated)
        self.timeline_widget.marker_clicked.connect(self.on_marker_clicked)
        # Timeline context actions
        self.timeline_widget.clip_rename_requested.connect(self.on_timeline_clip_rename_requested)
        self.timeline_widget.clip_jump_to_in.connect(self.on_timeline_clip_jump_to_in)
        self.timeline_widget.clip_jump_to_out.connect(self.on_timeline_clip_jump_to_out)
        self.timeline_widget.clip_set_in_from_current.connect(self.on_timeline_clip_set_in_from_current)
        self.timeline_widget.clip_set_out_from_current.connect(self.on_timeline_clip_set_out_from_current)
        self.timeline_widget.clip_split_requested.connect(self.on_timeline_clip_split_requested)
        splitter.addWidget(self.timeline_widget)

        # Set splitter sizes (60% video, 40% timeline)
        splitter.setSizes([600, 400])

        main_layout.addWidget(splitter)

        # Tool bar - explicit trim actions
        toolbar = QToolBar(i18n.t("toolbar.edit_tools", "Edit Tools"), self)
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        self.action_apply_io_to_clip = QAction(self.style().standardIcon(QStyle.SP_DialogApplyButton), i18n.t("action.apply_io", "Apply I/O to selected clip"), self)
        self.action_apply_io_to_clip.setToolTip(i18n.t("tooltip.apply_io", "Apply global I/O to current selected clip"))
        self.action_apply_io_to_clip.triggered.connect(self.apply_global_io_to_selected_clip)
        toolbar.addAction(self.action_apply_io_to_clip)

        self.action_add_io_as_clip = QAction(self.style().standardIcon(QStyle.SP_FileDialogNewFolder), i18n.t("action.add_io_as_clip", "Add I/O as new clip"), self)
        self.action_add_io_as_clip.setToolTip(i18n.t("tooltip.add_io_as_clip", "Add current video I/O as a new clip"))
        self.action_add_io_as_clip.triggered.connect(self.add_global_io_as_new_clip)
        toolbar.addAction(self.action_add_io_as_clip)

        self.action_extract_io_new_file = QAction(self.style().standardIcon(QStyle.SP_DialogSaveButton), i18n.t("action.extract_io_new_file", "Extract I/O to new file and add"), self)
        self.action_extract_io_new_file.setToolTip("使用 FFmpeg 真裁剪：把当前视频 I/O 段导出为独立文件，并自动加入时间轴")
        self.action_extract_io_new_file.triggered.connect(self.extract_global_io_to_new_file_and_add)
        toolbar.addAction(self.action_extract_io_new_file)

        # Status bar
        self.statusBar().showMessage(i18n.t("status.ready", "Ready"))  # i18n

    def create_menu_bar(self):
        """Create menu bar with all options."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu(i18n.t("menu.file", "&File"))

        open_action = QAction(i18n.t("action.open", "&Open Video..."), self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        export_action = QAction(i18n.t("action.export", "&Export Video..."), self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_video)
        file_menu.addAction(export_action)

        export_selected_action = QAction(i18n.t("action.export_selected", "Export Selected Clips..."), self)
        export_selected_action.setShortcut("Ctrl+Shift+E")
        export_selected_action.triggered.connect(self.export_selected_clips)
        file_menu.addAction(export_selected_action)

        file_menu.addSeparator()

        exit_action = QAction(i18n.t("action.exit", "E&xit"), self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu(i18n.t("menu.edit", "&Edit"))

        self.undo_action = QAction(i18n.t("action.undo", "&Undo"), self)
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.triggered.connect(self.undo)
        self.undo_action.setEnabled(False)
        edit_menu.addAction(self.undo_action)

        self.redo_action = QAction(i18n.t("action.redo", "&Redo"), self)
        self.redo_action.setShortcut("Ctrl+Y")
        self.redo_action.triggered.connect(self.redo)
        self.redo_action.setEnabled(False)
        edit_menu.addAction(self.redo_action)

        edit_menu.addSeparator()

        trim_mode_action = QAction(i18n.t("action.trim_mode", "&Trim Mode"), self)
        trim_mode_action.setShortcut("Ctrl+T")
        trim_mode_action.triggered.connect(self.toggle_trim_mode)
        edit_menu.addAction(trim_mode_action)

        set_in_action = QAction(i18n.t("action.set_in", "Set &In Point"), self)
        set_in_action.setShortcut("I")
        set_in_action.triggered.connect(self.set_in_point)
        edit_menu.addAction(set_in_action)

        set_out_action = QAction(i18n.t("action.set_out", "Set &Out Point"), self)
        set_out_action.setShortcut("O")
        set_out_action.triggered.connect(self.set_out_point)
        edit_menu.addAction(set_out_action)

        clear_trim_action = QAction(i18n.t("action.clear_trim", "Clear Trim Points"), self)
        clear_trim_action.triggered.connect(self.clear_trim_points)
        edit_menu.addAction(clear_trim_action)

        # View menu
        view_menu = menubar.addMenu(i18n.t("menu.view", "&View"))

        fullscreen_action = QAction(i18n.t("action.fullscreen", "&Fullscreen"), self)
        fullscreen_action.setShortcut("F")
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)

        view_menu.addSeparator()

        high_contrast_action = QAction(i18n.t("action.high_contrast", "&High Contrast Mode"), self)
        high_contrast_action.setShortcut("Ctrl+Shift+H")
        high_contrast_action.setCheckable(True)
        high_contrast_action.setChecked(self.theme_manager.is_high_contrast())
        high_contrast_action.triggered.connect(self.toggle_high_contrast)
        view_menu.addAction(high_contrast_action)

        # Language menu (Iteration 3)
        language_menu = menubar.addMenu(i18n.t("menu.language", "&Language"))
        lang_en_action = QAction(i18n.t("action.lang_en", "English"), self)
        lang_en_action.triggered.connect(lambda: self.change_language("en"))
        language_menu.addAction(lang_en_action)
        lang_zh_action = QAction(i18n.t("action.lang_zh", "中文"), self)
        lang_zh_action.triggered.connect(lambda: self.change_language("zh"))
        language_menu.addAction(lang_zh_action)

        # Markers menu
        markers_menu = menubar.addMenu(i18n.t("menu.markers", "&Markers"))

        add_marker_action = QAction(i18n.t("action.add_marker", "&Add Marker"), self)
        add_marker_action.setShortcut("M")
        add_marker_action.triggered.connect(self.add_marker)
        markers_menu.addAction(add_marker_action)

        prev_marker_action = QAction(i18n.t("action.prev_marker", "&Previous Marker"), self)
        prev_marker_action.setShortcut("[")
        prev_marker_action.triggered.connect(self.goto_previous_marker)
        markers_menu.addAction(prev_marker_action)

        next_marker_action = QAction(i18n.t("action.next_marker", "&Next Marker"), self)
        next_marker_action.setShortcut("]")
        next_marker_action.triggered.connect(self.goto_next_marker)
        markers_menu.addAction(next_marker_action)

        # Playback menu (Program preview controls)
        playback_menu = menubar.addMenu(i18n.t("menu.playback", "&Playback"))

        self.program_toggle_action = QAction(i18n.t("action.program_start", "Start Program Preview"), self)
        self.program_toggle_action.setShortcut("Ctrl+Shift+P")
        self.program_toggle_action.triggered.connect(self.toggle_program_preview)
        playback_menu.addAction(self.program_toggle_action)

        self.program_prev_action = QAction(i18n.t("action.program_prev", "Previous Clip"), self)
        self.program_prev_action.setShortcut("Ctrl+Shift+,")
        self.program_prev_action.triggered.connect(self.program_prev_clip)
        playback_menu.addAction(self.program_prev_action)

        self.program_next_action = QAction(i18n.t("action.program_next", "Next Clip"), self)
        self.program_next_action.setShortcut("Ctrl+Shift+.")
        self.program_next_action.triggered.connect(self.program_next_clip)
        playback_menu.addAction(self.program_next_action)

        # Help menu
        help_menu = menubar.addMenu(i18n.t("menu.help", "&Help"))

        shortcuts_action = QAction(i18n.t("action.shortcuts", "&Keyboard Shortcuts"), self)
        shortcuts_action.setShortcut("F1")
        shortcuts_action.triggered.connect(self.show_help)
        help_menu.addAction(shortcuts_action)

        help_menu.addSeparator()

        about_action = QAction(i18n.t("action.about", "&About"), self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # Account menu
        account_menu = menubar.addMenu(i18n.t("menu.account", "&Account"))
        # Current user label (disabled)
        current_user = self.auth.current_user.username if (hasattr(self, 'auth') and self.auth and self.auth.current_user) else "Guest"
        self.account_user_action = QAction(i18n.t("account.signed_in_as", "Signed in as: {user}").replace("{user}", current_user), self)
        self.account_user_action.setEnabled(False)
        account_menu.addAction(self.account_user_action)

        switch_action = QAction(i18n.t("account.switch_user", "&Switch User / Logout..."), self)
        switch_action.triggered.connect(self.switch_user)
        account_menu.addAction(switch_action)

    def create_control_panel(self):
        """Create playback controls."""
        control_layout = QHBoxLayout()

        # Rewind button
        self.rewind_button = QPushButton()
        self.rewind_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.rewind_button.setToolTip(i18n.t("tooltip.rewind", "Rewind 10s"))
        self.rewind_button.clicked.connect(self.rewind)
        self.rewind_button.setMinimumSize(40, 40)
        self.rewind_button.setEnabled(False)
        control_layout.addWidget(self.rewind_button)

        # Play/Pause button
        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.setToolTip(i18n.t("tooltip.play", "Play (Space)"))
        self.play_button.clicked.connect(self.play_pause)
        self.play_button.setMinimumSize(50, 50)
        self.play_button.setEnabled(False)
        control_layout.addWidget(self.play_button)

        # Stop button
        self.stop_button = QPushButton()
        self.stop_button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stop_button.setToolTip(i18n.t("tooltip.stop", "Stop"))
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.setMinimumSize(50, 50)
        self.stop_button.setEnabled(False)
        control_layout.addWidget(self.stop_button)

        # Fast-forward button
        self.forward_button = QPushButton()
        self.forward_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.forward_button.setToolTip(i18n.t("tooltip.forward", "Forward 10s"))
        self.forward_button.clicked.connect(self.fast_forward)
        self.forward_button.setMinimumSize(40, 40)
        self.forward_button.setEnabled(False)
        control_layout.addWidget(self.forward_button)

        control_layout.addSpacing(20)

        # Speed control
        self.speed_label = QLabel(i18n.t("label.speed", "Speed:"))
        control_layout.addWidget(self.speed_label)

        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["0.25x", "0.5x", "0.75x", "1x", "1.25x", "1.5x", "2x"])
        self.speed_combo.setCurrentText("1x")
        self.speed_combo.currentTextChanged.connect(self.change_speed)
        control_layout.addWidget(self.speed_combo)

        control_layout.addSpacing(20)

        # Volume control
        self.volume_text_label = QLabel(i18n.t("label.volume", "Volume:"))
        control_layout.addWidget(self.volume_text_label)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.setMaximumWidth(100)
        self.volume_slider.valueChanged.connect(self.set_volume)
        control_layout.addWidget(self.volume_slider)

        self.volume_label = QLabel("70%")
        self.volume_label.setMinimumWidth(40)
        control_layout.addWidget(self.volume_label)

        # Mute button
        self.mute_button = QPushButton()
        self.mute_button.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.mute_button.setToolTip(i18n.t("tooltip.mute", "Mute (M)"))
        self.mute_button.clicked.connect(self.toggle_mute)
        self.mute_button.setMaximumSize(40, 40)
        control_layout.addWidget(self.mute_button)

        control_layout.addSpacing(20)

        # Fullscreen button
        self.fullscreen_button = QPushButton()
        self.fullscreen_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton))
        self.fullscreen_button.setToolTip(i18n.t("tooltip.fullscreen", "Fullscreen (F)"))
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        self.fullscreen_button.setMaximumSize(40, 40)
        control_layout.addWidget(self.fullscreen_button)

        control_layout.addStretch()

        return control_layout

    # Playback controls (same as Iteration 1)
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, i18n.t("action.open", "Open Video File"), "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv);;All Files (*.*)"
        )
        if file_path:
            self.load_video_file(file_path)

    def load_video_file(self, file_path):
        if self.video_player.load_video(file_path):
            self.play_button.setEnabled(True)
            self.stop_button.setEnabled(True)
            self.rewind_button.setEnabled(True)
            self.forward_button.setEnabled(True)
            self.statusBar().showMessage(i18n.t("status.loaded", "Loaded: {name}").replace("{name}", os.path.basename(file_path)))

    def play_pause(self):
        state = self.video_player.get_state()
        if state == OpenCVVideoPlayer.STATE_PLAYING:
            self.video_player.pause()
        else:
            self.video_player.play()

    def stop(self):
        self.video_player.stop()

    def rewind(self):
        new_pos = max(0, self.video_player.get_position() - 10000)
        self.video_player.seek(new_pos)

    def fast_forward(self):
        duration = self.timeline_slider.maximum()
        new_pos = min(duration, self.video_player.get_position() + 10000)
        self.video_player.seek(new_pos)

    def set_volume(self, volume):
        self.volume_label.setText(f"{volume}%")
        self.video_player.set_volume(volume)

    def change_speed(self, speed_text):
        speed = float(speed_text.replace('x', ''))
        self.video_player.set_playback_speed(speed)
        msg = i18n.t("status.speed", "Playback speed: {speed}").replace("{speed}", speed_text)
        self.statusBar().showMessage(msg)

    def toggle_mute(self):
        current_muted = self.video_player.is_muted
        self.video_player.set_mute(not current_muted)
        if not current_muted:
            self.mute_button.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))
            self.statusBar().showMessage(i18n.t("status.muted", "Muted"))
        else:
            self.mute_button.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
            self.statusBar().showMessage(i18n.t("status.unmuted", "Unmuted"))

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.fullscreen_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton))
        else:
            self.showFullScreen()
            self.fullscreen_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarNormalButton))

    # Slider events
    def on_slider_pressed(self):
        self.is_seeking = True

    def on_slider_released(self):
        position = self.timeline_slider.value()
        self.video_player.seek(position)
        self.is_seeking = False

    def on_slider_moved(self, position):
        self.current_time_label.setText(self.format_time(position))

    def on_position_changed(self, position_ms):
        if not self.is_seeking:
            self.timeline_slider.setValue(position_ms)
        self.current_time_label.setText(self.format_time(position_ms))
        # Sync composition bar playhead
        if hasattr(self, 'composition_bar') and self.composition_bar:
            self.composition_bar.set_position(position_ms)
        # Program preview: if current clip has an Out point, auto-advance when reaching it
        if self.program_mode and self.program_current_clip_id:
            clip = self.timeline.get_clip(self.program_current_clip_id)
            if clip and position_ms >= clip.end_time_ms - 1:
                self.program_next_clip()
                return

    def on_duration_changed(self, duration_ms):
        self.timeline_slider.setRange(0, duration_ms)
        self.total_time_label.setText(self.format_time(duration_ms))

    def on_state_changed(self, state):
        if state == OpenCVVideoPlayer.STATE_PLAYING:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        # Program preview: auto-advance when a clip finishes
        if self.program_mode and state == OpenCVVideoPlayer.STATE_STOPPED:
            self.program_next_clip()

    @staticmethod
    def format_time(milliseconds):
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    # Iteration 2 features
    def toggle_high_contrast(self):
        self.theme_manager.toggle_high_contrast()
        if self.theme_manager.is_high_contrast():
            self.statusBar().showMessage(i18n.t("status.hc_on", "High contrast mode enabled"))
        else:
            self.statusBar().showMessage(i18n.t("status.hc_off", "High contrast mode disabled"))

    def toggle_trim_mode(self):
        self.trim_mode = not self.trim_mode
        if self.trim_mode:
            self.statusBar().showMessage(i18n.t("status.trim_on", "Trim mode: Press I for In point, O for Out point"))
        else:
            self.statusBar().showMessage(i18n.t("status.trim_off", "Trim mode disabled"))

    def set_in_point(self):
        self.in_point_ms = self.video_player.get_position()
        self.in_point_label.setText(f"In: {self.format_time(self.in_point_ms)}")
        self.statusBar().showMessage(i18n.t("status.in_set", "In point set at {time}").replace("{time}", self.format_time(self.in_point_ms)))
        # UX: if a clip is selected and we're previewing its source, reflect to Inspector field automatically
        if self.selected_clip_id is not None:
            clip = self.timeline.get_clip(self.selected_clip_id)
            if clip and self.video_player.video_path and os.path.abspath(clip.source_path) == os.path.abspath(self.video_player.video_path):
                self.inspector.set_in_from_ms(self.in_point_ms)
                # Auto-apply if Out exists and valid
                if self.out_point_ms is not None and self.out_point_ms > self.in_point_ms:
                    self.timeline.update_clip_in_out(clip.id, self.in_point_ms, self.out_point_ms)
                    # refresh inspector to show applied values
                    self.inspector.set_clip(clip.id, clip.label or os.path.basename(clip.source_path), clip.start_time_ms, clip.end_time_ms)
                    self.statusBar().showMessage(f"Applied to clip: {self.format_time(clip.start_time_ms)} - {self.format_time(clip.end_time_ms)}")

    def set_out_point(self):
        self.out_point_ms = self.video_player.get_position()
        self.out_point_label.setText(f"Out: {self.format_time(self.out_point_ms)}")
        self.statusBar().showMessage(i18n.t("status.out_set", "Out point set at {time}").replace("{time}", self.format_time(self.out_point_ms)))
        # UX: reflect to Inspector if a matching clip/source is in context
        if self.selected_clip_id is not None:
            clip = self.timeline.get_clip(self.selected_clip_id)
            if clip and self.video_player.video_path and os.path.abspath(clip.source_path) == os.path.abspath(self.video_player.video_path):
                self.inspector.set_out_from_ms(self.out_point_ms)
        else:
            # If no clip selected, try to bind Inspector to the first clip with same source
            if self.video_player.video_path:
                try:
                    from pathlib import Path
                    cur = os.path.abspath(self.video_player.video_path)
                    for c in self.timeline.clips:
                        if os.path.abspath(c.source_path) == cur:
                            self.selected_clip_id = c.id
                            self.inspector.set_clip(c.id, c.label or os.path.basename(c.source_path), c.start_time_ms, c.end_time_ms)
                            self.inspector.set_out_from_ms(self.out_point_ms)
                            break
                except Exception:
                    pass

    def clear_trim_points(self):
        self.in_point_ms = None
        self.out_point_ms = None
        self.in_point_label.setText("")
        self.out_point_label.setText("")
        self.statusBar().showMessage(i18n.t("status.trim_cleared", "Trim points cleared"))

    def add_marker(self):
        current_time = self.video_player.get_position()
        cmd = AddMarkerCommand(
            self.marker_manager,
            time_ms=current_time,
            label=f"Marker {self.marker_manager.get_marker_count() + 1}",
            color=MarkerManager.COLOR_RED
        )
        self.command_stack.execute(cmd)
        self.statusBar().showMessage(i18n.t("status.marker_added", "Marker added at {time}").replace("{time}", self.format_time(current_time)))

    def goto_previous_marker(self):
        current_time = self.video_player.get_position()
        marker = self.marker_manager.get_previous_marker(current_time)
        if marker:
            self.video_player.seek(marker.time_ms)
            self.statusBar().showMessage(i18n.t("status.marker_prev", "Jumped to marker: {label}").replace("{label}", marker.label))

    def goto_next_marker(self):
        current_time = self.video_player.get_position()
        marker = self.marker_manager.get_next_marker(current_time)
        if marker:
            self.video_player.seek(marker.time_ms)
            self.statusBar().showMessage(f"Jumped to marker: {marker.label}")

    def on_marker_clicked(self, marker_id):
        marker = self.marker_manager.get_marker(marker_id)
        if marker:
            self.video_player.seek(marker.time_ms)

    # Timeline context handlers
    def on_timeline_clip_rename_requested(self, clip_id: int):
        clip = self.timeline.get_clip(clip_id)
        if not clip:
            return
        text, ok = QInputDialog.getText(self, i18n.t("dialog.rename_title", "Rename Clip"), i18n.t("dialog.rename_prompt", "New name:"), text=clip.label or os.path.basename(clip.source_path))
        if ok:
            if self.timeline.update_clip_label(clip_id, text.strip()):
                c = self.timeline.get_clip(clip_id)
                if c:
                    self.inspector.set_clip(c.id, c.label or os.path.basename(c.source_path), c.start_time_ms, c.end_time_ms)
                    self.statusBar().showMessage(f"Renamed clip to: {c.label or os.path.basename(c.source_path)}")

    def _ensure_clip_loaded_for_preview(self, clip: 'TimelineClip') -> bool:
        """Load clip's source if different, set selected and inspector."""
        self.selected_clip_id = clip.id
        if self.video_player.video_path and os.path.abspath(self.video_player.video_path) == os.path.abspath(clip.source_path):
            self.inspector.set_clip(clip.id, clip.label or os.path.basename(clip.source_path), clip.start_time_ms, clip.end_time_ms)
            return True
        if self.video_player.load_video(clip.source_path):
            self.timeline_slider.setRange(0, self.video_player.get_duration())
            self.inspector.set_clip(clip.id, clip.label or os.path.basename(clip.source_path), clip.start_time_ms, clip.end_time_ms)
            return True
        return False

    def on_timeline_clip_jump_to_in(self, clip_id: int):
        clip = self.timeline.get_clip(clip_id)
        if not clip:
            return
        if self._ensure_clip_loaded_for_preview(clip):
            self.video_player.seek(clip.start_time_ms)
            self.video_player.play()
            self.statusBar().showMessage(i18n.t("status.jump_in","Jumped to In: {time}").replace("{time}", self.format_time(clip.start_time_ms)))

    def on_timeline_clip_jump_to_out(self, clip_id: int):
        clip = self.timeline.get_clip(clip_id)
        if not clip:
            return
        if self._ensure_clip_loaded_for_preview(clip):
            pos = max(0, clip.end_time_ms - 1)
            self.video_player.seek(pos)
            self.video_player.play()
            self.statusBar().showMessage(f"Jumped to Out: {self.format_time(clip.end_time_ms)}")

    def on_timeline_clip_set_in_from_current(self, clip_id: int):
        clip = self.timeline.get_clip(clip_id)
        if not clip:
            return
        cur = self.video_player.get_position()
        new_start = cur
        new_end = max(new_start + 10, clip.end_time_ms)  # ensure at least 10ms
        if self.timeline.update_clip_in_out(clip_id, new_start, new_end):
            c = self.timeline.get_clip(clip_id)
            if c:
                self.inspector.set_clip(c.id, c.label or os.path.basename(c.source_path), c.start_time_ms, c.end_time_ms)
                self.statusBar().showMessage(f"Set In: {self.format_time(c.start_time_ms)}")

    def on_timeline_clip_set_out_from_current(self, clip_id: int):
        clip = self.timeline.get_clip(clip_id)
        if not clip:
            return
        cur = self.video_player.get_position()
        new_end = cur
        new_start = min(clip.start_time_ms, new_end - 10) if new_end - 10 > 0 else 0
        if new_end <= new_start:
            new_end = new_start + 10
        if self.timeline.update_clip_in_out(clip_id, new_start, new_end):
            c = self.timeline.get_clip(clip_id)
            if c:
                self.inspector.set_clip(c.id, c.label or os.path.basename(c.source_path), c.start_time_ms, c.end_time_ms)
                self.statusBar().showMessage(f"Set Out: {self.format_time(c.end_time_ms)}")

    def on_timeline_clip_split_requested(self, clip_id: int):
        """Split selected clip at current player position (source time)."""
        clip = self.timeline.get_clip(clip_id)
        if not clip:
            return
        # Ensure correct source loaded
        if not self._ensure_clip_loaded_for_preview(clip):
            return
        split_ms = self.video_player.get_position()
        # Clamp split inside (start, end)
        if split_ms <= clip.start_time_ms:
            split_ms = clip.start_time_ms + 10
        if split_ms >= clip.end_time_ms:
            split_ms = clip.end_time_ms - 10
        if split_ms <= clip.start_time_ms or split_ms >= clip.end_time_ms:
            self.statusBar().showMessage("Cannot split: position out of range")
            return
        new_clip = self.timeline.split_clip(clip_id, split_ms)
        if new_clip:
            # Focus the right part after split
            self.selected_clip_id = new_clip.id
            self.inspector.set_clip(new_clip.id, new_clip.label or os.path.basename(new_clip.source_path), new_clip.start_time_ms, new_clip.end_time_ms)
            self.statusBar().showMessage(f"Split at {self.format_time(split_ms)} -> new clip #{new_clip.id}")

    # Program preview controls
    def toggle_program_preview(self):
        if not self.program_mode:
            # start program preview
            order = [c.id for c in self.timeline.get_sorted_clips()]
            if not order:
                self.statusBar().showMessage(i18n.t("status.program_no_clips", "No clips for program preview"))
                return
            self.program_order = order
            # start from selected clip if present else index 0
            if self.selected_clip_id in order:
                self.program_index = order.index(self.selected_clip_id)
            else:
                self.program_index = 0
            self.program_mode = True
            self.program_toggle_action.setText(i18n.t("action.program_stop", "Stop Program Preview"))
            self._program_play_clip_by_index(self.program_index)
        else:
            self.program_mode = False
            self.program_current_clip_id = None
            self.program_toggle_action.setText(i18n.t("action.program_start", "Start Program Preview"))
            self.statusBar().showMessage(i18n.t("status.program_stopped", "Program preview stopped"))

    def _program_play_clip_by_index(self, idx: int):
        if idx < 0 or idx >= len(self.program_order):
            self.toggle_program_preview()
            return
        clip_id = self.program_order[idx]
        clip = self.timeline.get_clip(clip_id)
        if not clip:
            self.program_next_clip()
            return
        self.program_current_clip_id = clip_id
        self.on_timeline_clip_activated(clip_id)

    def program_next_clip(self):
        if not self.program_mode:
            return
        self.program_index += 1
        if self.program_index >= len(self.program_order):
            # end
            self.toggle_program_preview()
            return
        self._program_play_clip_by_index(self.program_index)

    def program_prev_clip(self):
        if not self.program_mode:
            return
        self.program_index -= 1
        if self.program_index < 0:
            self.program_index = 0
        self._program_play_clip_by_index(self.program_index)

    # Composition bar handlers
    def on_composition_seek(self, pos_ms: int):
        """Seek via composition bar: map timeline time to source clip and seek accordingly."""
        clip = self.timeline.get_clip_at_position(pos_ms)
        if not clip:
            # If no clip at this time, just seek by position in current video if any
            if self.video_player.capture is not None:
                self.video_player.seek(pos_ms)
            return
        # Compute source time = clip.start + (globalPos - clip.position)
        src_time = clip.start_time_ms + max(0, pos_ms - clip.position_ms)
        # Load source if different
        need_load = (not self.video_player.video_path) or (os.path.abspath(self.video_player.video_path) != os.path.abspath(clip.source_path))
        prior_state = self.video_player.get_state()
        if need_load:
            if not self.video_player.load_video(clip.source_path):
                return
            self.timeline_slider.setRange(0, self.video_player.get_duration())
        # Seek
        self.video_player.seek(src_time)
        # Keep paused unless原本在播放
        if prior_state == OpenCVVideoPlayer.STATE_PLAYING:
            self.video_player.play()
        # Sync selection and inspector
        self.selected_clip_id = clip.id
        self.inspector.set_clip(clip.id, clip.label or os.path.basename(clip.source_path), clip.start_time_ms, clip.end_time_ms)
        if hasattr(self, 'composition_bar') and self.composition_bar:
            self.composition_bar.set_selected_clip(clip.id)
        self.statusBar().showMessage(f"Seek to {self.format_time(src_time)} in clip #{clip.id}")

    # Toolbar actions
    def apply_global_io_to_selected_clip(self):
        """Apply global I/O (set via I/O keys) to the currently selected clip."""
        if self.selected_clip_id is None:
            self.statusBar().showMessage("No clip selected")
            return
        clip = self.timeline.get_clip(self.selected_clip_id)
        if not clip:
            self.statusBar().showMessage("No clip selected")
            return
        # Ensure preview source matches; if not, load it
        if not self.video_player.video_path or os.path.abspath(self.video_player.video_path) != os.path.abspath(clip.source_path):
            if not self.video_player.load_video(clip.source_path):
                self.statusBar().showMessage("Failed to load clip source for applying I/O")
                return
            self.timeline_slider.setRange(0, self.video_player.get_duration())
        in_ms = self.in_point_ms if self.in_point_ms is not None else clip.start_time_ms
        out_ms = self.out_point_ms if self.out_point_ms is not None else clip.end_time_ms
        if out_ms <= in_ms:
            out_ms = in_ms + 10
        if self.timeline.update_clip_in_out(clip.id, in_ms, out_ms):
            c = self.timeline.get_clip(clip.id)
            if c:
                self.inspector.set_clip(c.id, c.label or os.path.basename(c.source_path), c.start_time_ms, c.end_time_ms)
                self.statusBar().showMessage(f"Applied global I/O to clip: {self.format_time(c.start_time_ms)} - {self.format_time(c.end_time_ms)}")

    def add_global_io_as_new_clip(self):
        """Add current video (global I/O range) as a new clip to timeline (referencing source file)."""
        if not self.video_player.video_path:
            self.statusBar().showMessage("No video loaded")
            return
        total = self.video_player.get_duration()
        in_ms = self.in_point_ms if self.in_point_ms is not None else 0
        out_ms = self.out_point_ms if self.out_point_ms is not None else total
        if out_ms <= in_ms:
            out_ms = in_ms + 10
        duration = out_ms - in_ms
        new_clip = self.timeline.add_clip(
            source_path=self.video_player.video_path,
            start_time_ms=in_ms,
            duration_ms=duration
        )
        self.selected_clip_id = new_clip.id
        self.inspector.set_clip(new_clip.id, new_clip.label or os.path.basename(new_clip.source_path), new_clip.start_time_ms, new_clip.end_time_ms)
        self.statusBar().showMessage(f"Added new clip from I/O: {self.format_time(in_ms)} - {self.format_time(out_ms)}")

    def extract_global_io_to_new_file_and_add(self):
        """Physically trim global I/O to a new file via FFmpeg and add to timeline."""
        if not self.video_player.video_path:
            QMessageBox.information(self, "No Video", "No video loaded.")
            return
        # Check FFmpeg
        if not FFmpegProcessor.check_ffmpeg_available():
            QMessageBox.warning(self, "FFmpeg Not Found", "FFmpeg is required to physically trim to a new file.")
            return
        total = self.video_player.get_duration()
        in_ms = self.in_point_ms if self.in_point_ms is not None else 0
        out_ms = self.out_point_ms if self.out_point_ms is not None else total
        if out_ms <= in_ms:
            out_ms = in_ms + 10
        duration = out_ms - in_ms
        # Suggest default path in videos/exports
        try:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "videos", "exports"))
        except Exception:
            base_dir = os.path.abspath(os.path.join(os.getcwd(), "videos", "exports"))
        os.makedirs(base_dir, exist_ok=True)
        from datetime import datetime
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"trim_{ts}.mp4"
        default_path = os.path.join(base_dir, default_name)
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Trimmed Clip As", default_path, "MP4 Video (*.mp4)")
        if not save_path:
            return
        if not save_path.lower().endswith('.mp4'):
            save_path += '.mp4'

        # Prepare processor and background thread
        processor = FFmpegProcessor()
        from PyQt5.QtCore import QThread
        worker = QThread()
        processor.moveToThread(worker)

        def on_completed(success: bool, msg: str):
            # Back to GUI thread context by Qt signals queue (already queued)
            if success and os.path.exists(save_path):
                # Add the new file as a fresh clip (0..duration)
                new_clip = self.timeline.add_clip(
                    source_path=save_path,
                    start_time_ms=0,
                    duration_ms=duration
                )
                self.selected_clip_id = new_clip.id
                self.inspector.set_clip(new_clip.id, new_clip.label or os.path.basename(new_clip.source_path), new_clip.start_time_ms, new_clip.end_time_ms)
                QMessageBox.information(self, "Trim Completed", f"New clip saved to:\n{save_path}")
                self.statusBar().showMessage("Trimmed new file added to timeline")
            else:
                QMessageBox.critical(self, "Trim Failed", f"{msg}")
            # Cleanup thread
            try:
                worker.quit()
                worker.wait(100)
                self.ffmpeg_workers.remove(worker)
            except Exception:
                pass

        processor.process_completed.connect(on_completed)
        # Progress feedback to status bar
        processor.progress_updated.connect(lambda p: self.statusBar().showMessage(f"Trimming... {p}%"))

        worker.started.connect(lambda: processor.trim_video(self.video_player.video_path, save_path, in_ms, out_ms, FFmpegProcessor.QUALITY_HIGH))
        worker.start()
        self.ffmpeg_workers.append(worker)
        self.statusBar().showMessage("Trimming...")

    def on_timeline_clip_selected(self, clip_id):
        """Select a clip and show in inspector (do not change playback)."""
        clip = self.timeline.get_clip(clip_id)
        if clip:
            self.selected_clip_id = clip_id
            self.inspector.set_clip(clip.id, clip.label or os.path.basename(clip.source_path), clip.start_time_ms, clip.end_time_ms)
            self.statusBar().showMessage(i18n.t("status.selected_clip","Selected clip: {name}").replace("{name}", os.path.basename(clip.source_path)))

    def on_timeline_clip_activated(self, clip_id):
        """Double-click: load clip's source and preview from its In point."""
        clip = self.timeline.get_clip(clip_id)
        if not clip:
            return
        self.selected_clip_id = clip_id
        # Load source and seek to In point
        if self.video_player.load_video(clip.source_path):
            self.timeline_slider.setRange(0, self.video_player.get_duration())
            self.video_player.seek(clip.start_time_ms)
            self.video_player.play()
            self.inspector.set_clip(clip.id, clip.label or os.path.basename(clip.source_path), clip.start_time_ms, clip.end_time_ms)
            self.statusBar().showMessage(f"Preview clip from {self.format_time(clip.start_time_ms)}")

    # Inspector handlers
    def on_inspector_apply_inout(self, clip_id: int, start_ms: int, end_ms: int):
        """Apply edited In/Out to timeline clip and refresh UI."""
        if not self.timeline.update_clip_in_out(clip_id, start_ms, end_ms):
            return
        clip = self.timeline.get_clip(clip_id)
        if clip:
            # If currently previewing this clip, seek to new In point
            if self.selected_clip_id == clip_id and self.video_player.video_path == clip.source_path:
                self.video_player.seek(clip.start_time_ms)
            # Reflect into inspector and status bar
            self.inspector.set_clip(clip.id, clip.label or os.path.basename(clip.source_path), clip.start_time_ms, clip.end_time_ms)
            self.statusBar().showMessage(f"Updated clip In/Out: {self.format_time(clip.start_time_ms)} - {self.format_time(clip.end_time_ms)}")

    def on_inspector_rename_clip(self, clip_id: int, new_label: str):
        if self.timeline.update_clip_label(clip_id, new_label):
            clip = self.timeline.get_clip(clip_id)
            if clip:
                self.inspector.set_clip(clip.id, clip.label or os.path.basename(clip.source_path), clip.start_time_ms, clip.end_time_ms)
                self.statusBar().showMessage(f"Renamed clip to: {clip.label or os.path.basename(clip.source_path)}")

    def on_inspector_set_in_from_player(self):
        pos = self.video_player.get_position()
        self.inspector.set_in_from_ms(pos)

    def on_inspector_set_out_from_player(self):
        pos = self.video_player.get_position()
        self.inspector.set_out_from_ms(pos)

    def export_video(self):
        # Determine exportability first
        has_video = self.video_player.capture is not None
        has_clips = self.timeline.get_clip_count() > 0

        if not has_video and not has_clips:
            QMessageBox.information(
                self,
                i18n.t("dialog.no_video_to_export_title", "No Video to Export"),
                i18n.t("dialog.no_video_to_export_msg", "Please load a video or add clips to the timeline before exporting.")
            )
            return

        dialog = ExportDialog(self)
        dialog.export_started.connect(self.on_export_started)

        if dialog.exec_() == ExportDialog.Accepted:
            settings = dialog.get_export_settings()
            # If export mode requires FFmpeg, check availability here
            requires_ffmpeg = False
            if has_clips:
                requires_ffmpeg = True
            else:
                # Single video export: trimming requires FFmpeg; full copy does not
                if self.in_point_ms is not None or self.out_point_ms is not None:
                    requires_ffmpeg = True
            if requires_ffmpeg and not FFmpegProcessor.check_ffmpeg_available():
                QMessageBox.warning(
                    self,
                    i18n.t("dialog.ffmpeg_missing_title", "FFmpeg Not Found"),
                    i18n.t("dialog.ffmpeg_missing_msg", "FFmpeg is required for video export but was not found on your system."),
                    QMessageBox.Ok
                )
                return
            self.perform_export(settings, dialog)

    def export_selected_clips(self):
        # Build selection list from current timeline
        clips = self.timeline.get_sorted_clips()
        if not clips:
            QMessageBox.information(self, "No Clips", "There are no clips on the timeline.")
            return
        # Open selection dialog
        dlg = SelectClipsDialog(clips, self)
        if dlg.exec_() != QDialog.Accepted:
            return
        selected = dlg.get_selection()
        if not selected:
            QMessageBox.information(self, "No Selection", "Please select at least one clip.")
            return
        # Open export dialog for quality/transitions
        dialog = ExportDialog(self)
        dialog.export_started.connect(self.on_export_started)
        if dialog.exec_() != QDialog.Accepted:
            return
        settings = dialog.get_export_settings()
        # Selection export requires FFmpeg (concat)
        if not FFmpegProcessor.check_ffmpeg_available():
            QMessageBox.warning(self, "FFmpeg Not Found", "FFmpeg is required to export selected clips.")
            return
        # Determine output path etc.
        output_path = settings["output_path"]
        quality = settings["quality"]
        self.export_selected_timeline(selected, output_path, quality, dialog, settings)

    def on_export_started(self):
        self.statusBar().showMessage(i18n.t("status.export_start", "Starting export..."))

    def perform_export(self, settings, dialog):
        """Perform the actual video export."""
        output_path = settings["output_path"]
        quality = settings["quality"]

        # Determine export mode
        if self.timeline.get_clip_count() > 0:
            # Export timeline (multiple clips)
            self.export_timeline(output_path, quality, dialog, settings)
        elif self.in_point_ms is not None or self.out_point_ms is not None:
            # Export trimmed single video
            self.export_trimmed_video(output_path, quality, dialog)
        else:
            # Export full single video
            self.export_full_video(output_path, quality, dialog)

    def export_full_video(self, output_path, quality, dialog):
        """Export the current loaded video as-is."""
        if not self.video_player.video_path:
            dialog.on_export_completed(False, "No video loaded")
            return

        dialog.set_status("Copying video file...")

        # Simple copy or re-encode
        import shutil
        try:
            # For now, just copy the file
            # In production, would use FFmpeg to re-encode
            shutil.copy2(self.video_player.video_path, output_path)
            dialog.on_export_completed(True, output_path)
        except Exception as e:
            dialog.on_export_completed(False, str(e))

    def export_trimmed_video(self, output_path, quality, dialog):
        """Export trimmed video using In/Out points."""
        if not self.video_player.video_path:
            dialog.on_export_completed(False, "No video loaded")
            return

        # Get trim range
        in_point = self.in_point_ms if self.in_point_ms is not None else 0
        out_point = self.out_point_ms if self.out_point_ms is not None else self.video_player.get_duration()

        dialog.set_status(f"Trimming video from {self.format_time(in_point)} to {self.format_time(out_point)}...")

        # Create FFmpeg worker
        from PyQt5.QtCore import QThread

        processor = FFmpegProcessor()
        processor.progress_updated.connect(dialog.set_progress)
        processor.process_completed.connect(
            lambda success, msg: dialog.on_export_completed(success, msg)
        )

        # Run in thread
        worker = QThread()
        processor.moveToThread(worker)
        worker.started.connect(
            lambda: processor.trim_video(
                self.video_player.video_path,
                output_path,
                in_point,
                out_point,
                quality
            )
        )
        worker.start()

        self.ffmpeg_worker = worker  # Keep reference

    def export_selected_timeline(self, selected_clips, output_path, quality, dialog, settings=None):
        """Export only the selected clips in the provided order."""
        if not selected_clips:
            dialog.on_export_completed(False, "No clips selected")
            return

        dialog.set_status(f"Exporting {len(selected_clips)} selected clips...")

        clip_data = [
            (clip.source_path, clip.start_time_ms, clip.end_time_ms)
            for clip in selected_clips
        ]

        transitions_enabled = bool(settings.get("transitions_enabled", False)) if settings else False
        transition_ms = int(settings.get("transition_ms", 500)) if settings else 500

        from PyQt5.QtCore import QThread
        processor = FFmpegProcessor()
        processor.progress_updated.connect(dialog.set_progress)
        processor.process_completed.connect(lambda success, msg: dialog.on_export_completed(success, msg))

        worker = QThread()
        processor.moveToThread(worker)
        worker.started.connect(
            lambda: processor.concatenate_clips(
                clip_data,
                output_path,
                quality,
                transitions_enabled=transitions_enabled,
                transition_ms=transition_ms
            )
        )
        worker.start()
        self.ffmpeg_worker = worker

    def export_timeline(self, output_path, quality, dialog, settings=None):
        """Export timeline with multiple clips."""
        # Use sorted clips to preserve visual order
        clips = self.timeline.get_sorted_clips()

        if not clips:
            dialog.on_export_completed(False, "No clips in timeline")
            return

        dialog.set_status(f"Exporting {len(clips)} clips...")

        # Prepare clip data for FFmpeg
        clip_data = [
            (clip.source_path, clip.start_time_ms, clip.end_time_ms)
            for clip in clips
        ]

        transitions_enabled = bool(settings.get("transitions_enabled", False)) if settings else False
        transition_ms = int(settings.get("transition_ms", 500)) if settings else 500

        # Create FFmpeg worker
        from PyQt5.QtCore import QThread

        processor = FFmpegProcessor()
        processor.progress_updated.connect(dialog.set_progress)
        processor.process_completed.connect(
            lambda success, msg: dialog.on_export_completed(success, msg)
        )

        # Run in thread
        worker = QThread()
        processor.moveToThread(worker)
        worker.started.connect(
            lambda: processor.concatenate_clips(
                clip_data,
                output_path,
                quality,
                transitions_enabled=transitions_enabled,
                transition_ms=transition_ms
            )
        )
        worker.start()

        self.ffmpeg_worker = worker  # Keep reference

    def undo(self):
        self.command_stack.undo()
        self.update_undo_redo_state()

    def redo(self):
        self.command_stack.redo()
        self.update_undo_redo_state()

    def update_undo_redo_state(self):
        self.undo_action.setEnabled(self.command_stack.can_undo())
        self.redo_action.setEnabled(self.command_stack.can_redo())

    def keyPressEvent(self, event):
        """Handle keyboard shortcuts."""
        if event.key() == Qt.Key_Space:
            self.play_pause()
        elif event.key() == Qt.Key_Left:
            new_pos = max(0, self.video_player.get_position() - 5000)
            self.video_player.seek(new_pos)
        elif event.key() == Qt.Key_Right:
            duration = self.timeline_slider.maximum()
            new_pos = min(duration, self.video_player.get_position() + 5000)
            self.video_player.seek(new_pos)
        elif event.key() == Qt.Key_Up:
            new_volume = min(100, self.volume_slider.value() + 5)
            self.volume_slider.setValue(new_volume)
        elif event.key() == Qt.Key_Down:
            new_volume = max(0, self.volume_slider.value() - 5)
            self.volume_slider.setValue(new_volume)
        elif event.key() == Qt.Key_F:
            self.toggle_fullscreen()
        elif event.key() == Qt.Key_M:
            if event.modifiers() == Qt.NoModifier:
                self.toggle_mute()
        elif event.key() == Qt.Key_I and event.modifiers() == Qt.NoModifier:
            self.set_in_point()
        elif event.key() == Qt.Key_O and event.modifiers() == Qt.NoModifier:
            self.set_out_point()
        elif event.key() == Qt.Key_Escape and self.isFullScreen():
            self.toggle_fullscreen()
        else:
            super().keyPressEvent(event)

    def load_sample_video(self):
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        videos_dir = os.path.join(current_dir, "..", "videos")
        if os.path.exists(videos_dir):
            video_files = [f for f in os.listdir(videos_dir)
                          if f.endswith(('.mp4', '.avi', '.mkv', '.mov'))]
            if video_files:
                sample_video = os.path.join(videos_dir, video_files[0])
                sample_video = os.path.abspath(sample_video)
                self.load_video_file(sample_video)

    def show_help(self):
        """Show keyboard shortcuts help dialog."""
        help_dialog = HelpDialog(self)
        help_dialog.exec_()

    def show_about(self):
        """Show about dialog."""
        about_text = """
        <h2>Video Editor/Player</h2>
        <p><b>Version:</b> 2.0 (Iteration 2)</p>
        <p><b>Course:</b> XJCO2811 User Interfaces</p>
        <p><b>Institution:</b> University of Leeds</p>
        <p><b>Academic Year:</b> 2024-2025</p>

        <h3>Features:</h3>
        <ul>
            <li>Video playback with advanced controls</li>
            <li>Video trimming and cutting</li>
            <li>Multi-clip timeline assembly</li>
            <li>Marker-based navigation</li>
            <li>High contrast mode (WCAG AAA)</li>
            <li>Undo/Redo system</li>
            <li>FFmpeg-powered export</li>
        </ul>

        <h3>Technologies:</h3>
        <ul>
            <li>Python 3.8+</li>
            <li>PyQt5 5.15.10</li>
            <li>OpenCV 4.8.0+</li>
            <li>FFmpeg 4.4+</li>
        </ul>

        <p><b>Press F1</b> to view all keyboard shortcuts.</p>

        <p style="margin-top: 20px; font-size: 9pt; color: #666;">
        © 2024-2025 XJCO2811 Assessment Project
        </p>
        """

        QMessageBox.about(self, "About Video Editor/Player", about_text)

    def update_account_user_menu(self):
        """Refresh Account menu label to show current user."""
        try:
            if hasattr(self, 'account_user_action'):
                current_user = self.auth.current_user.username if (self.auth and self.auth.current_user) else "Guest"
                self.account_user_action.setText(i18n.t("account.signed_in_as", f"Signed in as: {current_user}"))
        except Exception:
            pass

    def switch_user(self):
        """Logout and prompt login again. If cancelled, quit app to enforce auth gate."""
        reply = QMessageBox.question(
            self,
            i18n.t("account.switch_user_title", "Switch User"),
            i18n.t("account.switch_user_msg", "Logout current user and switch?"),
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return
        # Logout current
        try:
            if self.auth:
                self.auth.logout()
        except Exception:
            pass
        # Show login dialog
        login = LoginDialog(self.auth, self)
        result = login.exec_()
        if result == QDialog.Accepted and self.auth and self.auth.current_user:
            self.update_account_user_menu()
            self.statusBar().showMessage(i18n.t("account.signed_in_as", f"Signed in as: {self.auth.current_user.username}"))
        else:
            QMessageBox.information(self, i18n.t("account.not_signed_in", "Not signed in"), i18n.t("account.exit_msg", "No user signed in. The app will close."))
            self.close()

    def change_language(self, lang: str):
        """Change UI language and prompt restart for full effect."""
        current = i18n.get_language()
        if lang == current:
            return
        i18n.set_language(lang)
        # Update window title and status immediately
        self.setWindowTitle(i18n.t("window.title", self.windowTitle()))
        self.statusBar().showMessage(i18n.t("status.ready", "Ready"))
        QMessageBox.information(
            self,
            "Language Changed",
            "Language has been changed. Please restart the application to apply all translations."
        )

    def closeEvent(self, event):
        self.video_player.cleanup()
        event.accept()
