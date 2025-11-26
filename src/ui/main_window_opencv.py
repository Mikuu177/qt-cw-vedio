"""
Main Window - OpenCV Backend Version

This version uses OpenCV for video playback, providing better codec support
on Windows compared to QMediaPlayer.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QSlider, QLabel, QFileDialog, QStyle, QAction
)
from PyQt5.QtCore import Qt
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video.opencv_player import OpenCVVideoPlayer


class MainWindow(QMainWindow):
    """
    Main application window with OpenCV-based video player.
    """

    def __init__(self):
        super().__init__()
        self.is_seeking = False  # Flag to prevent seek loops
        self.init_ui()
        self.load_sample_video()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Video Editor/Player - XJCO2811 (OpenCV Backend)")
        self.setGeometry(100, 100, 1024, 768)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Menu bar
        self.create_menu_bar()

        # Video player widget (OpenCV-based)
        self.video_player = OpenCVVideoPlayer()
        self.video_player.setMinimumSize(640, 480)
        main_layout.addWidget(self.video_player)

        # Connect signals
        self.video_player.positionChanged.connect(self.on_position_changed)
        self.video_player.durationChanged.connect(self.on_duration_changed)
        self.video_player.stateChanged.connect(self.on_state_changed)

        # Timeline slider
        self.timeline_slider = QSlider(Qt.Horizontal)
        self.timeline_slider.setRange(0, 0)
        self.timeline_slider.sliderPressed.connect(self.on_slider_pressed)
        self.timeline_slider.sliderReleased.connect(self.on_slider_released)
        self.timeline_slider.sliderMoved.connect(self.on_slider_moved)
        main_layout.addWidget(self.timeline_slider)

        # Time labels
        time_layout = QHBoxLayout()
        self.current_time_label = QLabel("00:00")
        self.total_time_label = QLabel("00:00")
        time_layout.addWidget(self.current_time_label)
        time_layout.addStretch()
        time_layout.addWidget(self.total_time_label)
        main_layout.addLayout(time_layout)

        # Control panel
        control_layout = self.create_control_panel()
        main_layout.addLayout(control_layout)

        # Status bar
        self.statusBar().showMessage("Ready")

    def create_menu_bar(self):
        """Create menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        # Open action
        open_action = QAction("&Open Video...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def create_control_panel(self):
        """Create playback controls."""
        control_layout = QHBoxLayout()

        # Play/Pause button
        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.setToolTip("Play (Space)")
        self.play_button.clicked.connect(self.play_pause)
        self.play_button.setMinimumSize(50, 50)
        self.play_button.setEnabled(False)
        control_layout.addWidget(self.play_button)

        # Stop button
        self.stop_button = QPushButton()
        self.stop_button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stop_button.setToolTip("Stop")
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.setMinimumSize(50, 50)
        self.stop_button.setEnabled(False)
        control_layout.addWidget(self.stop_button)

        control_layout.addSpacing(20)

        # Volume control
        volume_label = QLabel("Volume:")
        control_layout.addWidget(volume_label)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.setMaximumWidth(150)
        self.volume_slider.valueChanged.connect(self.set_volume)
        control_layout.addWidget(self.volume_slider)

        self.volume_label = QLabel("70%")
        self.volume_label.setMinimumWidth(40)
        control_layout.addWidget(self.volume_label)

        control_layout.addStretch()

        return control_layout

    def open_file(self):
        """Open file dialog to select video."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Video File",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv);;All Files (*.*)"
        )

        if file_path:
            self.load_video_file(file_path)

    def load_video_file(self, file_path):
        """Load a video file."""
        print(f"[DEBUG] Loading video file: {file_path}")

        if self.video_player.load_video(file_path):
            self.play_button.setEnabled(True)
            self.stop_button.setEnabled(True)
            self.statusBar().showMessage(f"Loaded: {os.path.basename(file_path)}")
        else:
            self.statusBar().showMessage(f"Failed to load: {os.path.basename(file_path)}")

    def play_pause(self):
        """Toggle play/pause."""
        state = self.video_player.get_state()

        if state == OpenCVVideoPlayer.STATE_PLAYING:
            self.video_player.pause()
        else:
            self.video_player.play()

    def stop(self):
        """Stop playback."""
        self.video_player.stop()

    def set_volume(self, volume):
        """Set volume (not applicable for OpenCV, but update label)."""
        self.volume_label.setText(f"{volume}%")
        self.video_player.set_volume(volume)

    def on_slider_pressed(self):
        """Handle slider press."""
        self.is_seeking = True

    def on_slider_released(self):
        """Handle slider release."""
        position = self.timeline_slider.value()
        self.video_player.seek(position)
        self.is_seeking = False

    def on_slider_moved(self, position):
        """Handle slider movement."""
        # Update time label while dragging
        self.current_time_label.setText(self.format_time(position))

    def on_position_changed(self, position_ms):
        """Handle position changes from player."""
        if not self.is_seeking:
            self.timeline_slider.setValue(position_ms)
        self.current_time_label.setText(self.format_time(position_ms))

    def on_duration_changed(self, duration_ms):
        """Handle duration changes from player."""
        self.timeline_slider.setRange(0, duration_ms)
        self.total_time_label.setText(self.format_time(duration_ms))

    def on_state_changed(self, state):
        """Handle state changes from player."""
        if state == OpenCVVideoPlayer.STATE_PLAYING:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.play_button.setToolTip("Pause (Space)")
            self.statusBar().showMessage("Playing")
        else:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.play_button.setToolTip("Play (Space)")
            if state == OpenCVVideoPlayer.STATE_PAUSED:
                self.statusBar().showMessage("Paused")
            elif state == OpenCVVideoPlayer.STATE_STOPPED:
                self.statusBar().showMessage("Stopped")

    @staticmethod
    def format_time(milliseconds):
        """Format milliseconds to MM:SS."""
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def keyPressEvent(self, event):
        """Handle keyboard shortcuts."""
        if event.key() == Qt.Key_Space:
            self.play_pause()
        elif event.key() == Qt.Key_Left:
            # Seek backward 5 seconds
            new_pos = max(0, self.video_player.get_position() - 5000)
            self.video_player.seek(new_pos)
        elif event.key() == Qt.Key_Right:
            # Seek forward 5 seconds
            duration = self.timeline_slider.maximum()
            new_pos = min(duration, self.video_player.get_position() + 5000)
            self.video_player.seek(new_pos)
        elif event.key() == Qt.Key_Up:
            # Increase volume
            new_volume = min(100, self.volume_slider.value() + 5)
            self.volume_slider.setValue(new_volume)
        elif event.key() == Qt.Key_Down:
            # Decrease volume
            new_volume = max(0, self.volume_slider.value() - 5)
            self.volume_slider.setValue(new_volume)
        else:
            super().keyPressEvent(event)

    def load_sample_video(self):
        """Auto-load sample video from videos folder."""
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        videos_dir = os.path.join(current_dir, "..", "videos")

        if os.path.exists(videos_dir):
            video_files = [f for f in os.listdir(videos_dir)
                          if f.endswith(('.mp4', '.avi', '.mkv', '.mov'))]

            if video_files:
                sample_video = os.path.join(videos_dir, video_files[0])
                sample_video = os.path.abspath(sample_video)
                self.load_video_file(sample_video)

    def closeEvent(self, event):
        """Handle window close event."""
        self.video_player.cleanup()
        event.accept()
