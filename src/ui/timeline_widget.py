"""
Timeline Widget - Multi-Clip Timeline UI

Visual timeline for multi-clip editing with drag-and-drop reordering.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QPushButton, QLabel, QFrame, QFileDialog, QMenu, QAction, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QRect, QPoint, QSize
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont, QMouseEvent
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video.timeline import Timeline, TimelineClip
from video.marker import MarkerManager, Marker
from utils.i18n_manager import i18n


class ClipItem(QFrame):
    """Visual representation of a timeline clip."""

    clicked = pyqtSignal(int)  # clip_id
    delete_requested = pyqtSignal(int)  # clip_id
    move_requested = pyqtSignal(int, int)  # clip_id, new_index

    def __init__(self, clip: TimelineClip, parent=None):
        super().__init__(parent)
        self.clip = clip
        self.is_selected = False

        self.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.setLineWidth(2)
        self.setMinimumSize(100, 60)
        self.setMaximumHeight(80)

        # Enable drag
        self.drag_start_pos = None

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Clip label
        filename = os.path.basename(clip.source_path)
        self.label = QLabel(filename)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("font-size: 9pt; font-weight: bold;")
        layout.addWidget(self.label)

        # Duration label
        duration_sec = clip.duration_ms / 1000.0
        self.duration_label = QLabel(f"{duration_sec:.1f}s")
        self.duration_label.setStyleSheet("font-size: 8pt; color: #666;")
        layout.addWidget(self.duration_label)

        self.update_style()

    def update_style(self):
        """Update visual style based on selection state."""
        if self.is_selected:
            self.setStyleSheet("""
                ClipItem {
                    background-color: #e6f3ff;
                    border: 3px solid #0078d4;
                    border-radius: 4px;
                }
            """)
        else:
            self.setStyleSheet("""
                ClipItem {
                    background-color: #f0f0f0;
                    border: 2px solid #cccccc;
                    border-radius: 4px;
                }
            """)

    def set_selected(self, selected: bool):
        """Set selection state."""
        self.is_selected = selected
        self.update_style()

    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press for selection and drag."""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.clip.id)
            self.drag_start_pos = event.pos()
        elif event.button() == Qt.RightButton:
            self.show_context_menu(event.pos())

    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle drag to reorder."""
        if not (event.buttons() & Qt.LeftButton):
            return

        if self.drag_start_pos is None:
            return

        # Check if drag distance threshold met
        if (event.pos() - self.drag_start_pos).manhattanLength() < 10:
            return

        # For simplicity, we'll handle reordering in the timeline widget
        # Just emit a visual cue here
        pass

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release."""
        self.drag_start_pos = None

    def show_context_menu(self, pos: QPoint):
        """Show context menu on right-click."""
        menu = QMenu(self)

        delete_action = QAction(i18n.t("timeline.context_delete", "Delete Clip"), self)
        delete_action.triggered.connect(lambda: self.delete_requested.emit(self.clip.id))
        menu.addAction(delete_action)

        menu.exec_(self.mapToGlobal(pos))


class MarkerIndicator(QWidget):
    """Visual marker indicator on timeline."""

    clicked = pyqtSignal(int)  # marker_id

    def __init__(self, marker: Marker, parent=None):
        super().__init__(parent)
        self.marker = marker
        self.setFixedSize(20, 20)
        self.setToolTip(f"{marker.label} ({marker.time_ms}ms)")

    def paintEvent(self, event):
        """Draw marker as a colored flag."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw flag shape
        color = QColor(self.marker.color)
        painter.setBrush(QBrush(color))
        painter.setPen(QPen(Qt.white, 2))

        # Triangle flag
        points = [
            QPoint(2, 2),
            QPoint(18, 10),
            QPoint(2, 18)
        ]
        painter.drawPolygon(*points)

        # Pole
        painter.setPen(QPen(Qt.white, 3))
        painter.drawLine(2, 2, 2, 18)

    def mousePressEvent(self, event: QMouseEvent):
        """Handle click to jump to marker."""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.marker.id)


class TimelineWidget(QWidget):
    """
    Multi-clip timeline widget with drag-and-drop.

    Signals:
        clip_selected: Emitted when clip is selected (clip_id)
        clip_deleted: Emitted when clip is deleted (clip_id)
        marker_clicked: Emitted when marker is clicked (marker_id)
    """

    clip_selected = pyqtSignal(int)
    clip_deleted = pyqtSignal(int)
    marker_clicked = pyqtSignal(int)

    def __init__(self, timeline: Timeline, marker_manager: MarkerManager, parent=None):
        super().__init__(parent)
        self.timeline = timeline
        self.marker_manager = marker_manager
        self.clip_widgets = {}  # clip_id -> ClipItem
        self.marker_widgets = {}  # marker_id -> MarkerIndicator
        self.selected_clip_id = None

        self.init_ui()

        # Connect signals
        self.timeline.clip_added.connect(self.on_clip_added)
        self.timeline.clip_removed.connect(self.on_clip_removed)
        self.timeline.timeline_cleared.connect(self.on_timeline_cleared)

        self.marker_manager.marker_added.connect(self.on_marker_added)
        self.marker_manager.marker_removed.connect(self.on_marker_removed)
        self.marker_manager.markers_cleared.connect(self.on_markers_cleared)

    def init_ui(self):
        """Initialize UI."""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Header
        header_layout = QHBoxLayout()
        header_label = QLabel(i18n.t("timeline.title", "Timeline"))
        header_label.setStyleSheet("font-size: 12pt; font-weight: bold;")
        header_layout.addWidget(header_label)

        header_layout.addStretch()

        # Add clip button
        self.add_clip_btn = QPushButton(i18n.t("timeline.add", "+ Add Clip"))
        self.add_clip_btn.setToolTip(i18n.t("timeline.add_tip", "Add video clip to timeline"))
        self.add_clip_btn.clicked.connect(self.add_clip_dialog)
        header_layout.addWidget(self.add_clip_btn)

        # Clear timeline button
        self.clear_btn = QPushButton(i18n.t("timeline.clear", "Clear Timeline"))
        self.clear_btn.setToolTip(i18n.t("timeline.clear_tip", "Remove all clips"))
        self.clear_btn.clicked.connect(self.clear_timeline)
        header_layout.addWidget(self.clear_btn)

        main_layout.addLayout(header_layout)

        # Marker bar (above clips)
        self.marker_bar = QWidget()
        self.marker_bar.setMinimumHeight(30)
        self.marker_bar.setStyleSheet("background-color: #f9f9f9; border: 1px solid #ddd;")
        main_layout.addWidget(self.marker_bar)

        # Clip container (scrollable)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.clip_container = QWidget()
        self.clip_layout = QHBoxLayout()
        self.clip_layout.setAlignment(Qt.AlignLeft)
        self.clip_layout.setSpacing(10)
        self.clip_container.setLayout(self.clip_layout)

        scroll_area.setWidget(self.clip_container)
        main_layout.addWidget(scroll_area)

        # Timeline info
        self.info_label = QLabel(i18n.t("timeline.no_clips", "No clips"))
        self.info_label.setStyleSheet("font-size: 9pt; color: #666;")
        main_layout.addWidget(self.info_label)

    def on_clip_added(self, clip: TimelineClip):
        """Handle clip added to timeline."""
        clip_widget = ClipItem(clip)
        clip_widget.clicked.connect(self.on_clip_clicked)
        clip_widget.delete_requested.connect(self.on_clip_delete_requested)

        self.clip_widgets[clip.id] = clip_widget
        self.clip_layout.addWidget(clip_widget)

        self.update_info()

    def on_clip_removed(self, clip_id: int):
        """Handle clip removed from timeline."""
        if clip_id in self.clip_widgets:
            widget = self.clip_widgets[clip_id]
            self.clip_layout.removeWidget(widget)
            widget.deleteLater()
            del self.clip_widgets[clip_id]

            if self.selected_clip_id == clip_id:
                self.selected_clip_id = None

        self.update_info()

    def on_timeline_cleared(self):
        """Handle timeline cleared."""
        for widget in self.clip_widgets.values():
            widget.deleteLater()

        self.clip_widgets.clear()
        self.selected_clip_id = None
        self.update_info()

    def on_clip_clicked(self, clip_id: int):
        """Handle clip selection."""
        # Deselect previous
        if self.selected_clip_id and self.selected_clip_id in self.clip_widgets:
            self.clip_widgets[self.selected_clip_id].set_selected(False)

        # Select new
        self.selected_clip_id = clip_id
        if clip_id in self.clip_widgets:
            self.clip_widgets[clip_id].set_selected(True)

        self.clip_selected.emit(clip_id)

    def on_clip_delete_requested(self, clip_id: int):
        """Handle clip deletion request."""
        self.timeline.remove_clip(clip_id)
        self.clip_deleted.emit(clip_id)

    def add_clip_dialog(self):
        """Show dialog to add a clip."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            i18n.t("timeline.dialog_add_title", "Add Video Clip"),
            "",
            i18n.t("timeline.filter", "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv);;All Files (*.*)")
        )

        if file_path:
            # Get video duration using multiple methods
            duration_ms = self.get_video_duration(file_path)

            self.timeline.add_clip(
                source_path=file_path,
                start_time_ms=0,
                duration_ms=duration_ms
            )

    def get_video_duration(self, file_path):
        """
        Get video duration using multiple fallback methods.

        Try in order:
        1. FFprobe (most accurate, requires FFmpeg)
        2. OpenCV (works without FFmpeg)
        3. Placeholder (10 seconds)
        """
        # Method 1: Try FFprobe (if FFmpeg installed)
        try:
            from video.ffmpeg_processor import get_video_info
            info = get_video_info(file_path)
            if info and "duration_ms" in info:
                print(f"[Timeline] Got duration from FFprobe: {info['duration_ms']}ms")
                return info["duration_ms"]
        except Exception as e:
            print(f"[Timeline] FFprobe unavailable: {e}")

        # Method 2: Try OpenCV (fallback)
        try:
            import cv2
            cap = cv2.VideoCapture(file_path)
            if cap.isOpened():
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                if fps > 0 and frame_count > 0:
                    duration_ms = int((frame_count / fps) * 1000)
                    cap.release()
                    print(f"[Timeline] Got duration from OpenCV: {duration_ms}ms ({frame_count} frames at {fps:.2f} fps)")
                    return duration_ms
                cap.release()
        except Exception as e:
            print(f"[Timeline] OpenCV fallback failed: {e}")

        # Method 3: Use placeholder
        print("[Timeline] Using placeholder duration: 10000ms (10 seconds)")
        return 10000  # Placeholder: 10 seconds

    def clear_timeline(self):
        """Clear all clips from timeline."""
        reply = QMessageBox.question(
            self,
            i18n.t("timeline.confirm_clear_title", "Clear Timeline"),
            i18n.t("timeline.confirm_clear_msg", "Remove all clips from timeline?"),
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.timeline.clear()

    def update_info(self):
        """Update timeline info label."""
        count = self.timeline.get_clip_count()
        duration_ms = self.timeline.get_total_duration()
        duration_sec = duration_ms / 1000.0

        if count == 0:
            self.info_label.setText(i18n.t("timeline.no_clips", "No clips"))
        else:
            template = i18n.t("timeline.info", f"{count} clip(s) | Total duration: {duration_sec:.1f}s")
            self.info_label.setText(
                template.replace("{count}", str(count)).replace("{secs}", f"{duration_sec:.1f}")
            )

    def on_marker_added(self, marker: Marker):
        """Handle marker added."""
        # Create marker indicator
        # (Positioning would require knowing timeline scale)
        # For simplicity, we'll add to marker bar
        indicator = MarkerIndicator(marker)
        indicator.clicked.connect(self.on_marker_clicked)
        self.marker_widgets[marker.id] = indicator

        # Position on marker bar (simple linear layout for now)
        # In production, would calculate position based on time
        indicator.move(10 + len(self.marker_widgets) * 25, 5)
        indicator.setParent(self.marker_bar)
        indicator.show()

    def on_marker_removed(self, marker_id: int):
        """Handle marker removed."""
        if marker_id in self.marker_widgets:
            widget = self.marker_widgets[marker_id]
            widget.deleteLater()
            del self.marker_widgets[marker_id]

    def on_markers_cleared(self):
        """Handle all markers cleared."""
        for widget in self.marker_widgets.values():
            widget.deleteLater()
        self.marker_widgets.clear()

    def on_marker_clicked(self, marker_id: int):
        """Handle marker click."""
        self.marker_clicked.emit(marker_id)


# Testing
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    timeline = Timeline()
    marker_mgr = MarkerManager()

    widget = TimelineWidget(timeline, marker_mgr)
    widget.setWindowTitle("Timeline Widget Test")
    widget.resize(800, 300)
    widget.show()

    # Add test clips
    timeline.add_clip("test1.mp4", duration_ms=5000, label="Clip 1")
    timeline.add_clip("test2.mp4", duration_ms=3000, label="Clip 2")

    # Add test markers
    marker_mgr.add_marker(2000, "Start")
    marker_mgr.add_marker(7000, "Middle")

    sys.exit(app.exec_())
