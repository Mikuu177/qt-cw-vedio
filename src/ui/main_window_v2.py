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
    QPushButton, QSlider, QLabel, QFileDialog, QStyle, QAction, QComboBox, QMessageBox
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
from utils.theme_manager import ThemeManager
from utils.command_stack import CommandStack, AddClipCommand, AddMarkerCommand
from video.ffmpeg_processor import FFmpegProcessor, FFmpegWorker
from utils.i18n_manager import i18n


class MainWindow(QMainWindow):
    """
    Enhanced main application window with video editing features.
    """

    def __init__(self, app):
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

        # FFmpeg processor
        self.ffmpeg_processor = FFmpegProcessor()
        self.ffmpeg_worker = None

        # Theme manager
        self.theme_manager = ThemeManager(app)

        # Settings
        self.settings = QSettings("XJCO2811", "VideoEditor")

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
        self.timeline_widget.marker_clicked.connect(self.on_marker_clicked)
        splitter.addWidget(self.timeline_widget)

        # Set splitter sizes (60% video, 40% timeline)
        splitter.setSizes([600, 400])

        main_layout.addWidget(splitter)

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
            self.statusBar().showMessage(f"Loaded: {os.path.basename(file_path)}")

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

    def on_duration_changed(self, duration_ms):
        self.timeline_slider.setRange(0, duration_ms)
        self.total_time_label.setText(self.format_time(duration_ms))

    def on_state_changed(self, state):
        if state == OpenCVVideoPlayer.STATE_PLAYING:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

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

    def set_out_point(self):
        self.out_point_ms = self.video_player.get_position()
        self.out_point_label.setText(f"Out: {self.format_time(self.out_point_ms)}")
        self.statusBar().showMessage(i18n.t("status.out_set", "Out point set at {time}").replace("{time}", self.format_time(self.out_point_ms)))

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

    def on_timeline_clip_selected(self, clip_id):
        clip = self.timeline.get_clip(clip_id)
        if clip:
            self.statusBar().showMessage(f"Selected clip: {os.path.basename(clip.source_path)}")

    def export_video(self):
        # Check if FFmpeg is available
        if not FFmpegProcessor.check_ffmpeg_available():
            QMessageBox.warning(
                self,
                i18n.t("dialog.ffmpeg_missing_title", "FFmpeg Not Found"),
                i18n.t("dialog.ffmpeg_missing_msg", "FFmpeg is required for video export but was not found on your system."),
                QMessageBox.Ok | QMessageBox.Cancel
            )
            return

        # Check if we have video loaded or clips in timeline
        has_video = self.video_player.capture is not None
        has_clips = self.timeline.get_clip_count() > 0

        if not has_video and not has_clips:
            QMessageBox.information(
                self,
                "No Video to Export",
                "Please load a video or add clips to the timeline before exporting."
            )
            return

        dialog = ExportDialog(self)
        dialog.export_started.connect(self.on_export_started)

        if dialog.exec_() == ExportDialog.Accepted:
            settings = dialog.get_export_settings()
            self.perform_export(settings, dialog)

    def on_export_started(self):
        self.statusBar().showMessage(i18n.t("status.export_start", "Starting export..."))

    def perform_export(self, settings, dialog):
        """Perform the actual video export."""
        output_path = settings["output_path"]
        quality = settings["quality"]

        # Determine export mode
        if self.timeline.get_clip_count() > 0:
            # Export timeline (multiple clips)
            self.export_timeline(output_path, quality, dialog)
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

    def export_timeline(self, output_path, quality, dialog):
        """Export timeline with multiple clips."""
        clips = self.timeline.get_clips_in_range(0, self.timeline.get_total_duration())

        if not clips:
            dialog.on_export_completed(False, "No clips in timeline")
            return

        dialog.set_status(f"Exporting {len(clips)} clips...")

        # Prepare clip data for FFmpeg
        clip_data = [
            (clip.source_path, clip.start_time_ms, clip.end_time_ms)
            for clip in clips
        ]

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
            lambda: processor.concatenate_clips(clip_data, output_path, quality)
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
