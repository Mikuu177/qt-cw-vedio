"""
Timeline Data Model

Manages multi-clip timeline for video editing.
Supports adding, removing, reordering clips.
"""

from typing import List, Optional
from dataclasses import dataclass
from PyQt5.QtCore import QObject, pyqtSignal


@dataclass
class TimelineClip:
    """Represents a video clip on the timeline."""

    id: int
    source_path: str  # Path to source video file
    start_time_ms: int  # Trim start in source video
    duration_ms: int  # Duration of clip (after trim)
    position_ms: int  # Position on timeline
    label: str = ""  # Optional clip label

    @property
    def end_time_ms(self) -> int:
        """End time in source video."""
        return self.start_time_ms + self.duration_ms

    @property
    def timeline_end_ms(self) -> int:
        """End position on timeline."""
        return self.position_ms + self.duration_ms

    def __repr__(self):
        return (
            f"TimelineClip(id={self.id}, source='{self.source_path}', "
            f"start={self.start_time_ms}ms, duration={self.duration_ms}ms, "
            f"position={self.position_ms}ms)"
        )


class Timeline(QObject):
    """
    Timeline data model for multi-clip editing.

    Signals:
        clip_added: Emitted when clip is added (clip)
        clip_removed: Emitted when clip is removed (clip_id)
        clip_modified: Emitted when clip is modified (clip)
        timeline_cleared: Emitted when timeline is cleared
        duration_changed: Emitted when total duration changes (duration_ms)
    """

    clip_added = pyqtSignal(object)  # TimelineClip
    clip_removed = pyqtSignal(int)  # clip_id
    clip_modified = pyqtSignal(object)  # TimelineClip
    timeline_cleared = pyqtSignal()
    duration_changed = pyqtSignal(int)  # total_duration_ms

    def __init__(self):
        super().__init__()
        self.clips: List[TimelineClip] = []
        self._next_clip_id = 1

    def add_clip(
        self,
        source_path: str,
        start_time_ms: int = 0,
        duration_ms: Optional[int] = None,
        position_ms: Optional[int] = None,
        label: str = ""
    ) -> TimelineClip:
        """
        Add a clip to the timeline.

        Args:
            source_path: Path to video file
            start_time_ms: Start time in source (for trimmed clips)
            duration_ms: Duration of clip (None = use full video)
            position_ms: Position on timeline (None = append at end)
            label: Optional clip label

        Returns:
            The created TimelineClip
        """
        # If no position specified, append at end
        if position_ms is None:
            position_ms = self.get_total_duration()

        # If no duration specified, will be set when video is loaded
        if duration_ms is None:
            duration_ms = 0  # Placeholder

        clip = TimelineClip(
            id=self._next_clip_id,
            source_path=source_path,
            start_time_ms=start_time_ms,
            duration_ms=duration_ms,
            position_ms=position_ms,
            label=label
        )

        self._next_clip_id += 1

        # Insert clip at correct position (maintain sorted order)
        insert_idx = 0
        for i, existing_clip in enumerate(self.clips):
            if existing_clip.position_ms > position_ms:
                break
            insert_idx = i + 1

        self.clips.insert(insert_idx, clip)

        # Shift subsequent clips if inserting in middle
        if insert_idx < len(self.clips) - 1:
            self._shift_clips_after(insert_idx, clip.duration_ms)

        self.clip_added.emit(clip)
        self._update_duration()

        print(f"[Timeline] Added clip: {clip}")
        return clip

    def remove_clip(self, clip_id: int) -> bool:
        """
        Remove a clip from timeline.

        Args:
            clip_id: ID of clip to remove

        Returns:
            True if removed, False if not found
        """
        for i, clip in enumerate(self.clips):
            if clip.id == clip_id:
                removed_clip = self.clips.pop(i)

                # Shift subsequent clips backward
                self._shift_clips_after(i - 1, -removed_clip.duration_ms)

                self.clip_removed.emit(clip_id)
                self._update_duration()

                print(f"[Timeline] Removed clip: {removed_clip}")
                return True

        return False

    def get_clip(self, clip_id: int) -> Optional[TimelineClip]:
        """Get clip by ID."""
        for clip in self.clips:
            if clip.id == clip_id:
                return clip
        return None

    def get_clip_at_position(self, position_ms: int) -> Optional[TimelineClip]:
        """Get clip at specific timeline position."""
        for clip in self.clips:
            if clip.position_ms <= position_ms < clip.timeline_end_ms:
                return clip
        return None

    def move_clip(self, clip_id: int, new_position_ms: int) -> bool:
        """
        Move a clip to a new timeline position.

        Args:
            clip_id: ID of clip to move
            new_position_ms: New position on timeline

        Returns:
            True if moved successfully
        """
        clip = self.get_clip(clip_id)
        if not clip:
            return False

        # Remove from current position
        self.clips.remove(clip)

        # Update position
        clip.position_ms = new_position_ms

        # Re-insert at new position
        insert_idx = 0
        for i, existing_clip in enumerate(self.clips):
            if existing_clip.position_ms > new_position_ms:
                break
            insert_idx = i + 1

        self.clips.insert(insert_idx, clip)

        # Recalculate all positions to close gaps
        self._recalculate_positions()

        self.clip_modified.emit(clip)
        self._update_duration()

        print(f"[Timeline] Moved clip {clip_id} to {new_position_ms}ms")
        return True

    def reorder_clip(self, clip_id: int, new_index: int) -> bool:
        """
        Reorder clip by index (for drag-and-drop).

        Args:
            clip_id: ID of clip to reorder
            new_index: New index in clip list

        Returns:
            True if reordered successfully
        """
        # Find current index
        old_index = None
        for i, clip in enumerate(self.clips):
            if clip.id == clip_id:
                old_index = i
                break

        if old_index is None:
            return False

        # Clamp new_index
        new_index = max(0, min(new_index, len(self.clips) - 1))

        if old_index == new_index:
            return True

        # Remove and reinsert
        clip = self.clips.pop(old_index)
        self.clips.insert(new_index, clip)

        # Recalculate positions
        self._recalculate_positions()

        self.clip_modified.emit(clip)
        self._update_duration()

        print(f"[Timeline] Reordered clip {clip_id} from index {old_index} to {new_index}")
        return True

    def update_clip_duration(self, clip_id: int, new_duration_ms: int) -> bool:
        """Update clip duration (e.g., after trimming)."""
        clip = self.get_clip(clip_id)
        if not clip:
            return False

        old_duration = clip.duration_ms
        clip.duration_ms = new_duration_ms

        # Find clip index
        clip_idx = self.clips.index(clip)

        # Shift subsequent clips
        duration_delta = new_duration_ms - old_duration
        self._shift_clips_after(clip_idx, duration_delta)

        self.clip_modified.emit(clip)
        self._update_duration()

        return True

    def update_clip_in_out(self, clip_id: int, new_start_ms: int, new_end_ms: int) -> bool:
        """Update clip start and end (in/out) and shift timeline accordingly."""
        clip = self.get_clip(clip_id)
        if not clip:
            return False
        if new_end_ms < new_start_ms:
            return False

        old_duration = clip.duration_ms
        new_duration = new_end_ms - new_start_ms
        clip.start_time_ms = max(0, new_start_ms)
        clip.duration_ms = max(0, new_duration)

        clip_idx = self.clips.index(clip)
        duration_delta = clip.duration_ms - old_duration
        self._shift_clips_after(clip_idx, duration_delta)

        self.clip_modified.emit(clip)
        self._update_duration()
        return True

    def update_clip_label(self, clip_id: int, new_label: str) -> bool:
        """Update clip label and emit modified."""
        clip = self.get_clip(clip_id)
        if not clip:
            return False
        clip.label = new_label or ""
        self.clip_modified.emit(clip)
        return True

    def split_clip(self, clip_id: int, split_ms: int) -> Optional[TimelineClip]:
        """
        Split a clip at split_ms (absolute in source time). Returns the new right clip.
        Left clip keeps [start, split), right clip is [split, end).
        Positions on timeline are recomputed to avoid gaps.
        """
        clip = self.get_clip(clip_id)
        if not clip:
            return None
        # Validate split point is strictly inside
        if split_ms <= clip.start_time_ms or split_ms >= clip.end_time_ms:
            return None

        left_duration = split_ms - clip.start_time_ms
        right_duration = clip.end_time_ms - split_ms

        # Update left clip duration (this will shift subsequent clips by delta)
        old_duration = clip.duration_ms
        clip.duration_ms = left_duration
        clip_idx = self.clips.index(clip)
        duration_delta = left_duration - old_duration
        self._shift_clips_after(clip_idx, duration_delta)
        self.clip_modified.emit(clip)

        # Create right clip positioned immediately after left
        right_position = clip.timeline_end_ms
        new_clip = TimelineClip(
            id=self._next_clip_id,
            source_path=clip.source_path,
            start_time_ms=split_ms,
            duration_ms=right_duration,
            position_ms=right_position,
            label=clip.label + " (part 2)" if clip.label else ""
        )
        self._next_clip_id += 1

        # Insert new clip right after current index
        insert_idx = clip_idx + 1
        self.clips.insert(insert_idx, new_clip)

        # Shift any clips after the inserted right clip by its duration
        if insert_idx < len(self.clips) - 1:
            self._shift_clips_after(insert_idx, new_clip.duration_ms)

        # Recalculate positions to remove any rounding issues
        self._recalculate_positions()

        self.clip_added.emit(new_clip)
        self._update_duration()
        print(f"[Timeline] Split clip {clip_id} at {split_ms}ms -> new clip {new_clip.id}")
        return new_clip

    def clear(self):
        """Clear all clips from timeline."""
        self.clips.clear()
        self._next_clip_id = 1
        self.timeline_cleared.emit()
        self._update_duration()
        print("[Timeline] Cleared all clips")

    def get_total_duration(self) -> int:
        """Get total timeline duration in milliseconds."""
        if not self.clips:
            return 0

        # Find the end of the last clip
        max_end = 0
        for clip in self.clips:
            end = clip.timeline_end_ms
            if end > max_end:
                max_end = end

        return max_end

    def get_clip_count(self) -> int:
        """Get number of clips on timeline."""
        return len(self.clips)

    def _shift_clips_after(self, start_index: int, shift_ms: int):
        """Shift all clips after start_index by shift_ms."""
        for i in range(start_index + 1, len(self.clips)):
            self.clips[i].position_ms += shift_ms

    def _recalculate_positions(self):
        """Recalculate all clip positions to ensure no gaps/overlaps."""
        current_pos = 0
        for clip in self.clips:
            clip.position_ms = current_pos
            current_pos += clip.duration_ms

    def _update_duration(self):
        """Emit duration changed signal."""
        total = self.get_total_duration()
        self.duration_changed.emit(total)

    def get_clips_in_range(self, start_ms: int, end_ms: int) -> List[TimelineClip]:
        """Get all clips that overlap with the given time range."""
        result = []
        for clip in self.clips:
            # Check if clip overlaps with range
            if clip.timeline_end_ms > start_ms and clip.position_ms < end_ms:
                result.append(clip)
        return result

    def __repr__(self):
        return (
            f"Timeline(clips={len(self.clips)}, "
            f"duration={self.get_total_duration()}ms)"
        )

    # Helpers for program preview
    def get_sorted_clips(self) -> List[TimelineClip]:
        """Return clips sorted by position_ms."""
        return sorted(self.clips, key=lambda c: c.position_ms)

    def get_index_of_clip(self, clip_id: int) -> int:
        """Return index of clip in sorted order; -1 if not found."""
        sorted_clips = self.get_sorted_clips()
        for idx, c in enumerate(sorted_clips):
            if c.id == clip_id:
                return idx
        return -1


# Example usage
if __name__ == "__main__":
    timeline = Timeline()

    # Add clips
    clip1 = timeline.add_clip("video1.mp4", duration_ms=5000)
    clip2 = timeline.add_clip("video2.mp4", duration_ms=3000)
    clip3 = timeline.add_clip("video3.mp4", duration_ms=4000)

    print(f"Timeline: {timeline}")
    print(f"Total duration: {timeline.get_total_duration()}ms")

    # Reorder
    timeline.reorder_clip(clip2.id, 0)
    print(f"After reorder: {timeline}")

    # Remove
    timeline.remove_clip(clip1.id)
    print(f"After remove: {timeline}")
