"""
Composition Bar - Visualize merged timeline composition under the main slider

Shows each clip as a colored segment proportionally to its duration, with
segment boundaries and a moving playhead. Supports hover tooltip and click-to-seek.
"""
from typing import List, Optional
from PyQt5.QtWidgets import QWidget, QToolTip
from PyQt5.QtCore import Qt, QRectF, QPoint, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont
import os
import hashlib

# Add parent directory to path for imports when run directly
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from video.timeline import Timeline, TimelineClip


class CompositionBar(QWidget):
    seekRequested = pyqtSignal(int)  # position_ms
    segmentClicked = pyqtSignal(int)  # clip_id

    def __init__(self, parent=None):
        super().__init__(parent)
        self._timeline: Optional[Timeline] = None
        self._position_ms: int = 0
        self._selected_clip_id: Optional[int] = None
        self._transitions_enabled: bool = False
        self._transition_ms: int = 500
        self.setFixedHeight(26)
        self.setMouseTracking(True)
        self.setToolTip("")

    # Public API
    def set_timeline(self, timeline: Timeline):
        if self._timeline is not None:
            try:
                self._timeline.clip_added.disconnect(self._on_timeline_changed)
                self._timeline.clip_removed.disconnect(self._on_timeline_changed)
                self._timeline.clip_modified.disconnect(self._on_timeline_changed)
                self._timeline.timeline_cleared.disconnect(self._on_timeline_changed)
                self._timeline.duration_changed.disconnect(self._on_timeline_changed)
            except Exception:
                pass
        self._timeline = timeline
        if self._timeline is not None:
            self._timeline.clip_added.connect(self._on_timeline_changed)
            self._timeline.clip_removed.connect(self._on_timeline_changed)
            self._timeline.clip_modified.connect(self._on_timeline_changed)
            self._timeline.timeline_cleared.connect(self._on_timeline_changed)
            self._timeline.duration_changed.connect(self._on_timeline_changed)
        self.update()

    def set_transitions(self, enabled: bool, transition_ms: int = 500):
        self._transitions_enabled = bool(enabled)
        self._transition_ms = max(0, int(transition_ms))
        self.update()

    def set_position(self, position_ms: int):
        self._position_ms = max(0, int(position_ms))
        self.update()

    def set_selected_clip(self, clip_id: Optional[int]):
        self._selected_clip_id = clip_id
        self.update()

    # Timeline changed handler
    def _on_timeline_changed(self, *args, **kwargs):
        # Any structural change in timeline triggers a repaint
        self.update()

    # Painting helpers
    def _get_total_duration(self) -> int:
        if not self._timeline:
            return 0
        return int(self._timeline.get_total_duration())

    def _get_sorted_clips(self) -> List[TimelineClip]:
        if not self._timeline:
            return []
        try:
            return self._timeline.get_sorted_clips()
        except Exception:
            # Fallback if helper not present
            clips = list(self._timeline.clips)
            clips.sort(key=lambda c: c.position_ms)
            return clips

    def _color_for_source(self, path: str) -> QColor:
        # Stable color based on file path hash
        h = int(hashlib.md5(path.encode('utf-8', errors='ignore')).hexdigest()[:6], 16)
        r = (h >> 16) & 0xFF
        g = (h >> 8) & 0xFF
        b = h & 0xFF
        # Slight desaturation for softer look
        r = int((r + 180) / 2)
        g = int((g + 180) / 2)
        b = int((b + 180) / 2)
        return QColor(r, g, b)

    # QWidget events
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        # Background
        painter.fillRect(rect, QColor(245, 245, 245))
        painter.setPen(QPen(QColor(210, 210, 210), 1))
        painter.drawRect(rect.adjusted(0, 0, -1, -1))

        total = self._get_total_duration()
        clips = self._get_sorted_clips()
        if total <= 0 or not clips:
            # Draw hint text
            painter.setPen(QPen(QColor(130, 130, 130)))
            font = painter.font(); font.setPointSize(8)
            painter.setFont(font)
            try:
                from utils.i18n_manager import i18n
                text = i18n.t("timeline.no_clips", "No clips")
            except Exception:
                text = "No clips"
            painter.drawText(rect, Qt.AlignCenter, text)
            return

        # Draw segments
        width = rect.width()
        height = rect.height()
        scale = width / float(total)

        # Draw each clip as a segment
        for i, clip in enumerate(clips):
            seg_x = int(clip.position_ms * scale)
            seg_w = max(2, int(clip.duration_ms * scale))
            color = self._color_for_source(clip.source_path)
            # Fill
            painter.fillRect(QRectF(seg_x, 1, seg_w, height - 2), QBrush(color))
            # Border (thicker if selected)
            is_selected = (self._selected_clip_id == clip.id)
            pen = QPen(QColor(90, 90, 90) if not is_selected else QColor(10, 120, 200), 2 if is_selected else 1)
            painter.setPen(pen)
            painter.drawRect(QRectF(seg_x + 0.5, 0.5, seg_w - 1, height - 1))
            # Separator line at start (except first)
            if i > 0:
                painter.setPen(QPen(QColor(255, 255, 255, 200), 2))
                painter.drawLine(seg_x, 0, seg_x, height)

        # Optionally draw transition zones
        if self._transitions_enabled and len(clips) > 1 and self._transition_ms > 0:
            tw = int(self._transition_ms * scale)
            if tw >= 1:
                painter.setBrush(QBrush(QColor(255, 255, 255, 80)))
                painter.setPen(Qt.NoPen)
                acc = 0
                for idx in range(len(clips) - 1):
                    left = clips[idx]
                    acc += left.duration_ms
                    x = int(acc * scale) - tw
                    if x < 0:
                        x = 0
                    painter.drawRect(QRectF(x, 1, tw, height - 2))

        # Draw playhead
        x_play = int(self._position_ms * scale)
        painter.setPen(QPen(QColor(200, 30, 30), 1))
        painter.drawLine(x_play, 0, x_play, height)

    def _time_from_x(self, x: int) -> int:
        total = self._get_total_duration()
        if total <= 0:
            return 0
        x = max(0, min(self.width(), x))
        pos = int((x / float(self.width())) * total)
        return pos

    def mouseMoveEvent(self, event):
        pos_ms = self._time_from_x(event.x())
        clip = self._clip_at_time(pos_ms)
        if clip:
            label = clip.label if clip.label else os.path.basename(clip.source_path)
            info = f"{label}\nIn: {self._fmt_ms(clip.start_time_ms)}  Out: {self._fmt_ms(clip.end_time_ms)}  Dur: {self._fmt_ms(clip.duration_ms)}"
            QToolTip.showText(event.globalPos(), info, self)
        else:
            QToolTip.hideText()
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos_ms = self._time_from_x(event.x())
            self.seekRequested.emit(pos_ms)
        super().mousePressEvent(event)

    # Helpers
    def _clip_at_time(self, t_ms: int) -> Optional[TimelineClip]:
        clips = self._get_sorted_clips()
        for c in clips:
            if c.position_ms <= t_ms < c.position_ms + c.duration_ms:
                return c
        return None

    @staticmethod
    def _fmt_ms(ms: int) -> str:
        ms = max(0, int(ms))
        s, milli = divmod(ms, 1000)
        m, sec = divmod(s, 60)
        return f"{m:02d}:{sec:02d}.{milli:03d}"

