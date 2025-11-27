"""
Command Stack - Undo/Redo System

Implements the Command Pattern for reversible editing operations.
"""

from typing import List, Optional
from abc import ABC, abstractmethod
from PyQt5.QtCore import QObject, pyqtSignal


class Command(ABC):
    """Abstract base class for commands."""

    def __init__(self, description: str = ""):
        self.description = description

    @abstractmethod
    def execute(self):
        """Execute the command."""
        pass

    @abstractmethod
    def undo(self):
        """Undo the command."""
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({self.description})"


class CommandStack(QObject):
    """
    Manages undo/redo operations.

    Signals:
        can_undo_changed: Emitted when undo availability changes (can_undo: bool)
        can_redo_changed: Emitted when redo availability changes (can_redo: bool)
        command_executed: Emitted when command is executed (command: Command)
        command_undone: Emitted when command is undone (command: Command)
        command_redone: Emitted when command is redone (command: Command)
    """

    can_undo_changed = pyqtSignal(bool)
    can_redo_changed = pyqtSignal(bool)
    command_executed = pyqtSignal(object)  # Command
    command_undone = pyqtSignal(object)  # Command
    command_redone = pyqtSignal(object)  # Command

    def __init__(self, max_stack_size: int = 100):
        super().__init__()
        self.undo_stack: List[Command] = []
        self.redo_stack: List[Command] = []
        self.max_stack_size = max_stack_size

    def execute(self, command: Command):
        """
        Execute a command and add to undo stack.

        Args:
            command: Command to execute
        """
        # Execute the command
        command.execute()

        # Add to undo stack
        self.undo_stack.append(command)

        # Limit stack size
        if len(self.undo_stack) > self.max_stack_size:
            self.undo_stack.pop(0)

        # Clear redo stack (new action invalidates redo history)
        if self.redo_stack:
            self.redo_stack.clear()
            self.can_redo_changed.emit(False)

        self.command_executed.emit(command)
        self.can_undo_changed.emit(True)

        print(f"[Command] Executed: {command}")

    def undo(self):
        """Undo the last command."""
        if not self.can_undo():
            print("[Command] Nothing to undo")
            return

        # Pop from undo stack
        command = self.undo_stack.pop()

        # Undo the command
        command.undo()

        # Add to redo stack
        self.redo_stack.append(command)

        self.command_undone.emit(command)

        if not self.undo_stack:
            self.can_undo_changed.emit(False)

        if len(self.redo_stack) == 1:
            self.can_redo_changed.emit(True)

        print(f"[Command] Undone: {command}")

    def redo(self):
        """Redo the last undone command."""
        if not self.can_redo():
            print("[Command] Nothing to redo")
            return

        # Pop from redo stack
        command = self.redo_stack.pop()

        # Re-execute the command
        command.execute()

        # Add back to undo stack
        self.undo_stack.append(command)

        self.command_redone.emit(command)

        if not self.redo_stack:
            self.can_redo_changed.emit(False)

        if len(self.undo_stack) == 1:
            self.can_undo_changed.emit(True)

        print(f"[Command] Redone: {command}")

    def can_undo(self) -> bool:
        """Check if undo is available."""
        return len(self.undo_stack) > 0

    def can_redo(self) -> bool:
        """Check if redo is available."""
        return len(self.redo_stack) > 0

    def clear(self):
        """Clear all command history."""
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.can_undo_changed.emit(False)
        self.can_redo_changed.emit(False)
        print("[Command] Stack cleared")

    def get_undo_description(self) -> Optional[str]:
        """Get description of next undo operation."""
        if self.undo_stack:
            return self.undo_stack[-1].description
        return None

    def get_redo_description(self) -> Optional[str]:
        """Get description of next redo operation."""
        if self.redo_stack:
            return self.redo_stack[-1].description
        return None


# Example commands for timeline operations

class AddClipCommand(Command):
    """Command to add a clip to timeline."""

    def __init__(self, timeline, source_path: str, duration_ms: int):
        super().__init__(f"Add clip: {source_path}")
        self.timeline = timeline
        self.source_path = source_path
        self.duration_ms = duration_ms
        self.clip_id = None

    def execute(self):
        clip = self.timeline.add_clip(
            source_path=self.source_path,
            duration_ms=self.duration_ms
        )
        self.clip_id = clip.id

    def undo(self):
        if self.clip_id:
            self.timeline.remove_clip(self.clip_id)


class RemoveClipCommand(Command):
    """Command to remove a clip from timeline."""

    def __init__(self, timeline, clip_id: int):
        super().__init__(f"Remove clip: {clip_id}")
        self.timeline = timeline
        self.clip_id = clip_id
        self.removed_clip_data = None

    def execute(self):
        # Save clip data before removing
        clip = self.timeline.get_clip(self.clip_id)
        if clip:
            self.removed_clip_data = {
                "source_path": clip.source_path,
                "start_time_ms": clip.start_time_ms,
                "duration_ms": clip.duration_ms,
                "position_ms": clip.position_ms,
                "label": clip.label
            }
        self.timeline.remove_clip(self.clip_id)

    def undo(self):
        if self.removed_clip_data:
            self.timeline.add_clip(**self.removed_clip_data)


class ReorderClipCommand(Command):
    """Command to reorder a clip on timeline."""

    def __init__(self, timeline, clip_id: int, old_index: int, new_index: int):
        super().__init__(f"Reorder clip: {clip_id}")
        self.timeline = timeline
        self.clip_id = clip_id
        self.old_index = old_index
        self.new_index = new_index

    def execute(self):
        self.timeline.reorder_clip(self.clip_id, self.new_index)

    def undo(self):
        self.timeline.reorder_clip(self.clip_id, self.old_index)


class AddMarkerCommand(Command):
    """Command to add a marker."""

    def __init__(self, marker_manager, time_ms: int, label: str, color: str):
        super().__init__(f"Add marker: {label}")
        self.marker_manager = marker_manager
        self.time_ms = time_ms
        self.label = label
        self.color = color
        self.marker_id = None

    def execute(self):
        marker = self.marker_manager.add_marker(
            time_ms=self.time_ms,
            label=self.label,
            color=self.color
        )
        self.marker_id = marker.id

    def undo(self):
        if self.marker_id:
            self.marker_manager.remove_marker(self.marker_id)


class RemoveMarkerCommand(Command):
    """Command to remove a marker."""

    def __init__(self, marker_manager, marker_id: int):
        super().__init__(f"Remove marker: {marker_id}")
        self.marker_manager = marker_manager
        self.marker_id = marker_id
        self.removed_marker_data = None

    def execute(self):
        # Save marker data before removing
        marker = self.marker_manager.get_marker(self.marker_id)
        if marker:
            self.removed_marker_data = {
                "time_ms": marker.time_ms,
                "label": marker.label,
                "color": marker.color
            }
        self.marker_manager.remove_marker(self.marker_id)

    def undo(self):
        if self.removed_marker_data:
            self.marker_manager.add_marker(**self.removed_marker_data)


# Testing
if __name__ == "__main__":
    from video.timeline import Timeline
    from video.marker import MarkerManager

    # Create timeline and marker manager
    timeline = Timeline()
    marker_mgr = MarkerManager()

    # Create command stack
    stack = CommandStack()

    print("=== Testing Command Stack ===\n")

    # Add clips
    cmd1 = AddClipCommand(timeline, "video1.mp4", 5000)
    stack.execute(cmd1)
    print(f"Timeline: {timeline.get_clip_count()} clips\n")

    cmd2 = AddClipCommand(timeline, "video2.mp4", 3000)
    stack.execute(cmd2)
    print(f"Timeline: {timeline.get_clip_count()} clips\n")

    # Add marker
    cmd3 = AddMarkerCommand(marker_mgr, 2000, "Introduction", "#FF0000")
    stack.execute(cmd3)
    print(f"Markers: {marker_mgr.get_marker_count()}\n")

    # Undo
    print("=== Undo Operations ===")
    stack.undo()
    print(f"After undo: Markers: {marker_mgr.get_marker_count()}\n")

    stack.undo()
    print(f"After undo: Clips: {timeline.get_clip_count()}\n")

    # Redo
    print("=== Redo Operations ===")
    stack.redo()
    print(f"After redo: Clips: {timeline.get_clip_count()}\n")

    stack.redo()
    print(f"After redo: Markers: {marker_mgr.get_marker_count()}\n")

    print(f"Can undo: {stack.can_undo()}")
    print(f"Can redo: {stack.can_redo()}")
