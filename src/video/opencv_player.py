"""
OpenCV Video Player Widget

This module provides a video player using OpenCV backend,
which has better codec support on Windows than QMediaPlayer.
"""

import cv2
import numpy as np
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap


class OpenCVVideoPlayer(QLabel):
    """
    Video player widget using OpenCV for video decoding.
    Displays video frames and provides playback controls.

    Signals:
        positionChanged(int): Emitted when playback position changes (in ms)
        durationChanged(int): Emitted when video duration is available (in ms)
        stateChanged(int): Emitted when playback state changes (0=stopped, 1=playing, 2=paused)
    """

    # Playback states
    STATE_STOPPED = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2

    # Signals
    positionChanged = pyqtSignal(int)
    durationChanged = pyqtSignal(int)
    stateChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Video capture object
        self.capture = None
        self.video_path = None

        # Playback state
        self.state = self.STATE_STOPPED
        self.current_frame = 0
        self.total_frames = 0
        self.fps = 30.0
        self.duration_ms = 0

        # Playback speed (1.0 = normal, 0.5 = half speed, 2.0 = double speed)
        self.playback_speed = 1.0

        # Timer for frame updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_frame)

        # Volume (not applicable for OpenCV, but kept for API compatibility)
        self.volume = 70
        self.is_muted = False

        # Widget setup
        self.setMinimumSize(640, 480)
        self.setScaledContents(True)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: black;")
        self.setText("No video loaded")

        print("[DEBUG] OpenCVVideoPlayer initialized")

    def load_video(self, file_path):
        """
        Load a video file.

        Args:
            file_path (str): Path to the video file

        Returns:
            bool: True if video loaded successfully, False otherwise
        """
        print(f"[DEBUG] Loading video with OpenCV: {file_path}")

        # Release previous video if any
        if self.capture is not None:
            self.capture.release()

        # Open video file
        self.capture = cv2.VideoCapture(file_path)
        self.video_path = file_path

        if not self.capture.isOpened():
            print(f"[ERROR] Failed to open video: {file_path}")
            self.setText("Failed to load video")
            return False

        # Get video properties
        self.total_frames = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.capture.get(cv2.CAP_PROP_FPS)
        if self.fps <= 0:
            self.fps = 30.0  # Default fallback

        self.duration_ms = int((self.total_frames / self.fps) * 1000)
        self.current_frame = 0

        print(f"[DEBUG] Video loaded:")
        print(f"  Total frames: {self.total_frames}")
        print(f"  FPS: {self.fps}")
        print(f"  Duration: {self.duration_ms} ms")

        # Emit duration
        self.durationChanged.emit(self.duration_ms)

        # Display first frame
        self._display_current_frame()

        return True

    def play(self):
        """Start video playback."""
        if self.capture is None or not self.capture.isOpened():
            print("[DEBUG] Cannot play: No video loaded")
            return

        print(f"[DEBUG] Starting playback at {self.playback_speed}x speed")
        self.state = self.STATE_PLAYING
        self.stateChanged.emit(self.state)

        # Calculate timer interval based on FPS and playback speed
        interval = int((1000 / self.fps) / self.playback_speed)
        self.timer.start(interval)

    def pause(self):
        """Pause video playback."""
        print("[DEBUG] Pausing playback")
        self.state = self.STATE_PAUSED
        self.stateChanged.emit(self.state)
        self.timer.stop()

    def stop(self):
        """Stop video playback and return to beginning."""
        print("[DEBUG] Stopping playback")
        self.state = self.STATE_STOPPED
        self.stateChanged.emit(self.state)
        self.timer.stop()

        if self.capture is not None:
            self.current_frame = 0
            self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self._display_current_frame()
            self.positionChanged.emit(0)

    def seek(self, position_ms):
        """
        Seek to a specific position in the video.

        Args:
            position_ms (int): Position in milliseconds
        """
        if self.capture is None or not self.capture.isOpened():
            return

        # Calculate frame number from milliseconds
        frame_number = int((position_ms / 1000.0) * self.fps)
        frame_number = max(0, min(frame_number, self.total_frames - 1))

        print(f"[DEBUG] Seeking to {position_ms}ms (frame {frame_number})")

        self.current_frame = frame_number
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        self._display_current_frame()

        # Emit position change
        actual_position = int((self.current_frame / self.fps) * 1000)
        self.positionChanged.emit(actual_position)

    def set_volume(self, volume):
        """
        Set playback volume (not applicable for OpenCV, kept for API compatibility).

        Args:
            volume (int): Volume level 0-100
        """
        self.volume = volume

    def set_mute(self, muted):
        """
        Set mute state (not applicable for OpenCV, kept for API compatibility).

        Args:
            muted (bool): True to mute, False to unmute
        """
        self.is_muted = muted
        print(f"[DEBUG] Mute: {muted}")

    def set_playback_speed(self, speed):
        """
        Set playback speed.

        Args:
            speed (float): Playback speed (0.25, 0.5, 1.0, 1.5, 2.0, etc.)
        """
        self.playback_speed = speed
        print(f"[DEBUG] Playback speed set to {speed}x")

        # If currently playing, restart timer with new interval
        if self.state == self.STATE_PLAYING:
            interval = int((1000 / self.fps) / self.playback_speed)
            self.timer.setInterval(interval)

    def get_playback_speed(self):
        """Get current playback speed."""
        return self.playback_speed

    def get_state(self):
        """Get current playback state."""
        return self.state

    def get_position(self):
        """Get current playback position in milliseconds."""
        if self.capture is None:
            return 0
        return int((self.current_frame / self.fps) * 1000)

    def get_duration(self):
        """Get total duration in milliseconds."""
        return int(self.duration_ms or 0)

    def _update_frame(self):
        """Update to next frame (called by timer)."""
        if self.capture is None or not self.capture.isOpened():
            self.timer.stop()
            return

        # Read next frame
        ret, frame = self.capture.read()

        if not ret:
            # End of video
            print("[DEBUG] End of video reached")
            self.stop()
            return

        self.current_frame += 1

        # Display frame
        self._display_frame(frame)

        # Emit position update
        position_ms = int((self.current_frame / self.fps) * 1000)
        self.positionChanged.emit(position_ms)

    def _display_current_frame(self):
        """Display the current frame."""
        if self.capture is None or not self.capture.isOpened():
            return

        ret, frame = self.capture.read()
        if ret:
            self._display_frame(frame)

    def _display_frame(self, frame):
        """
        Display a frame in the widget.

        Args:
            frame: OpenCV frame (numpy array in BGR format)
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get frame dimensions
        height, width, channel = rgb_frame.shape
        bytes_per_line = 3 * width

        # Convert to QImage
        q_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Convert to QPixmap and display
        pixmap = QPixmap.fromImage(q_image)

        # Scale to fit widget while maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(
            self.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.setPixmap(scaled_pixmap)

    def cleanup(self):
        """Release resources."""
        print("[DEBUG] Cleaning up OpenCV player")
        self.timer.stop()
        if self.capture is not None:
            self.capture.release()
            self.capture = None
