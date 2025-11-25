"""
Main Window - Primary Application Interface

This module implements the main window of the video editor/player,
following Qt conventions and HCI principles:
- Fitts's Law: Large, accessible controls for frequent actions
- Gestalt Principles: Grouped, logically organized interface
- Consistency: Standard Qt widgets and layouts
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QSlider, QLabel, QFileDialog, QStyle, QAction, QMenuBar
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget


class MainWindow(QMainWindow):
    """
    Main application window containing video player and controls.
    """

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_media_player()

    def init_ui(self):
        """
        Initialize the user interface components.
        Applies HCI principles for optimal usability.
        """
        self.setWindowTitle("Video Editor/Player - XJCO2811")
        self.setGeometry(100, 100, 1024, 768)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Create menu bar
        self.create_menu_bar()

        # Video display widget
        # Fitts's Law: Large target area for primary content
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumSize(640, 480)
        main_layout.addWidget(self.video_widget)

        # Timeline slider
        # Positioned prominently for easy access
        self.timeline_slider = QSlider(Qt.Horizontal)
        self.timeline_slider.setRange(0, 0)
        self.timeline_slider.sliderMoved.connect(self.set_position)
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
        # Gestalt Principle: Grouped related controls
        control_layout = self.create_control_panel()
        main_layout.addLayout(control_layout)

        # Status bar for user feedback
        # Feedback principle: Inform users of system state
        self.statusBar().showMessage("Ready")

    def create_menu_bar(self):
        """
        Create the menu bar with File menu.
        Follows standard application conventions (Consistency principle).
        """
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        # Open action
        open_action = QAction("&Open Video...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip("Open a video file")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def create_control_panel(self):
        """
        Create the playback control panel.

        Design rationale:
        - Fitts's Law: Large buttons for frequent actions (play/pause)
        - Hick's Law: Limited choices, clear grouping
        - Feedback: Visual state indication

        Returns:
            QHBoxLayout: Layout containing control widgets
        """
        control_layout = QHBoxLayout()

        # Play button
        # Fitts's Law: Large, prominent button for most frequent action
        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.setToolTip("Play (Space)")
        self.play_button.clicked.connect(self.play_pause)
        self.play_button.setMinimumSize(50, 50)
        control_layout.addWidget(self.play_button)

        # Stop button
        self.stop_button = QPushButton()
        self.stop_button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stop_button.setToolTip("Stop")
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.setMinimumSize(50, 50)
        control_layout.addWidget(self.stop_button)

        # Add spacing
        control_layout.addSpacing(20)

        # Volume control
        # Grouped with other playback controls
        volume_label = QLabel("Volume:")
        control_layout.addWidget(volume_label)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.setMaximumWidth(150)
        self.volume_slider.setToolTip("Volume")
        self.volume_slider.valueChanged.connect(self.set_volume)
        control_layout.addWidget(self.volume_slider)

        self.volume_label = QLabel("70%")
        self.volume_label.setMinimumWidth(40)
        control_layout.addWidget(self.volume_label)

        # Add stretch to push controls to the left
        control_layout.addStretch()

        return control_layout

    def init_media_player(self):
        """
        Initialize the Qt media player and connect signals.
        """
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)

        # Connect signals for state updates
        # Feedback principle: Keep user informed of system state
        self.media_player.stateChanged.connect(self.media_state_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.error.connect(self.handle_error)

        # Set initial volume
        self.media_player.setVolume(70)

    def open_file(self):
        """
        Open a file dialog to select a video file.
        Error prevention: Only show supported video formats.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Video File",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv);;All Files (*.*)"
        )

        if file_path:
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.play_button.setEnabled(True)
            self.stop_button.setEnabled(True)
            # Feedback: Inform user of loaded file
            self.statusBar().showMessage(f"Loaded: {file_path}")

    def play_pause(self):
        """
        Toggle between play and pause states.
        Feedback: Visual indication of current state.
        """
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def stop(self):
        """
        Stop video playback.
        """
        self.media_player.stop()

    def set_position(self, position):
        """
        Seek to a specific position in the video.

        Args:
            position (int): Position in milliseconds
        """
        self.media_player.setPosition(position)

    def set_volume(self, volume):
        """
        Set the playback volume.
        Feedback: Display current volume level.

        Args:
            volume (int): Volume level (0-100)
        """
        self.media_player.setVolume(volume)
        self.volume_label.setText(f"{volume}%")

    def media_state_changed(self, state):
        """
        Handle media player state changes.
        Feedback principle: Update UI to reflect current state.

        Args:
            state (QMediaPlayer.State): New media player state
        """
        if state == QMediaPlayer.PlayingState:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.play_button.setToolTip("Pause (Space)")
            self.statusBar().showMessage("Playing")
        else:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.play_button.setToolTip("Play (Space)")
            if state == QMediaPlayer.PausedState:
                self.statusBar().showMessage("Paused")
            elif state == QMediaPlayer.StoppedState:
                self.statusBar().showMessage("Stopped")

    def position_changed(self, position):
        """
        Update UI when playback position changes.
        Feedback: Show current playback time.

        Args:
            position (int): Current position in milliseconds
        """
        self.timeline_slider.setValue(position)
        self.current_time_label.setText(self.format_time(position))

    def duration_changed(self, duration):
        """
        Update UI when media duration is known.

        Args:
            duration (int): Total duration in milliseconds
        """
        self.timeline_slider.setRange(0, duration)
        self.total_time_label.setText(self.format_time(duration))

    def handle_error(self):
        """
        Handle media player errors.
        Error prevention & feedback: Inform user of issues.
        """
        error_string = self.media_player.errorString()
        self.statusBar().showMessage(f"Error: {error_string}")

    @staticmethod
    def format_time(milliseconds):
        """
        Format time in milliseconds to MM:SS format.

        Args:
            milliseconds (int): Time in milliseconds

        Returns:
            str: Formatted time string (MM:SS)
        """
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def keyPressEvent(self, event):
        """
        Handle keyboard shortcuts.
        Accessibility: Keyboard access to all major functions.

        Args:
            event (QKeyEvent): Key press event
        """
        # Space bar: Play/Pause (most common action)
        if event.key() == Qt.Key_Space:
            self.play_pause()
        # Left arrow: Seek backward 5 seconds
        elif event.key() == Qt.Key_Left:
            new_position = max(0, self.media_player.position() - 5000)
            self.media_player.setPosition(new_position)
        # Right arrow: Seek forward 5 seconds
        elif event.key() == Qt.Key_Right:
            new_position = min(
                self.media_player.duration(),
                self.media_player.position() + 5000
            )
            self.media_player.setPosition(new_position)
        # Up arrow: Increase volume
        elif event.key() == Qt.Key_Up:
            new_volume = min(100, self.volume_slider.value() + 5)
            self.volume_slider.setValue(new_volume)
        # Down arrow: Decrease volume
        elif event.key() == Qt.Key_Down:
            new_volume = max(0, self.volume_slider.value() - 5)
            self.volume_slider.setValue(new_volume)
        else:
            super().keyPressEvent(event)
