"""
Marker System

Allows users to mark important moments in videos for quick navigation.
"""

from typing import List, Optional
from dataclasses import dataclass
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QColor


@dataclass
class Marker:
    """Represents a marker at a specific time in the video."""

    id: int
    time_ms: int  # Position in milliseconds
    label: str  # Marker label/description
    color: str  # Color code (hex: #RRGGBB)

    def __repr__(self):
        return f"Marker(id={self.id}, time={self.time_ms}ms, label='{self.label}', color='{self.color}')"


class MarkerManager(QObject):
    """
    Manages markers for video navigation.

    Signals:
        marker_added: Emitted when marker is added (marker)
        marker_removed: Emitted when marker is removed (marker_id)
        marker_modified: Emitted when marker is modified (marker)
        markers_cleared: Emitted when all markers are cleared
    """

    marker_added = pyqtSignal(object)  # Marker
    marker_removed = pyqtSignal(int)  # marker_id
    marker_modified = pyqtSignal(object)  # Marker
    markers_cleared = pyqtSignal()

    # Predefined marker colors
    COLOR_RED = "#FF0000"
    COLOR_BLUE = "#0000FF"
    COLOR_GREEN = "#00FF00"
    COLOR_YELLOW = "#FFFF00"
    COLOR_ORANGE = "#FF8800"
    COLOR_PURPLE = "#8800FF"
    COLOR_CYAN = "#00FFFF"
    COLOR_PINK = "#FF00FF"

    DEFAULT_COLORS = [
        COLOR_RED,
        COLOR_BLUE,
        COLOR_GREEN,
        COLOR_YELLOW,
        COLOR_ORANGE,
        COLOR_PURPLE,
        COLOR_CYAN,
        COLOR_PINK
    ]

    def __init__(self):
        super().__init__()
        self.markers: List[Marker] = []
        self._next_marker_id = 1
        self._color_index = 0  # For cycling through colors

    def add_marker(
        self,
        time_ms: int,
        label: str = "",
        color: Optional[str] = None
    ) -> Marker:
        """
        Add a marker at the specified time.

        Args:
            time_ms: Time position in milliseconds
            label: Optional label (default: "Marker N")
            color: Marker color (default: cycle through predefined colors)

        Returns:
            The created Marker
        """
        # Generate default label if not provided
        if not label:
            label = f"Marker {self._next_marker_id}"

        # Use next color in cycle if not provided
        if not color:
            color = self.DEFAULT_COLORS[self._color_index % len(self.DEFAULT_COLORS)]
            self._color_index += 1

        marker = Marker(
            id=self._next_marker_id,
            time_ms=time_ms,
            label=label,
            color=color
        )

        self._next_marker_id += 1

        # Insert in sorted order by time
        insert_idx = 0
        for i, existing_marker in enumerate(self.markers):
            if existing_marker.time_ms > time_ms:
                break
            insert_idx = i + 1

        self.markers.insert(insert_idx, marker)
        self.marker_added.emit(marker)

        print(f"[Markers] Added marker: {marker}")
        return marker

    def remove_marker(self, marker_id: int) -> bool:
        """
        Remove a marker by ID.

        Args:
            marker_id: ID of marker to remove

        Returns:
            True if removed, False if not found
        """
        for i, marker in enumerate(self.markers):
            if marker.id == marker_id:
                removed_marker = self.markers.pop(i)
                self.marker_removed.emit(marker_id)
                print(f"[Markers] Removed marker: {removed_marker}")
                return True

        return False

    def get_marker(self, marker_id: int) -> Optional[Marker]:
        """Get marker by ID."""
        for marker in self.markers:
            if marker.id == marker_id:
                return marker
        return None

    def get_marker_at_time(self, time_ms: int, tolerance_ms: int = 500) -> Optional[Marker]:
        """
        Get marker at or near the specified time.

        Args:
            time_ms: Time to search
            tolerance_ms: Search tolerance (default: 500ms)

        Returns:
            Nearest marker within tolerance, or None
        """
        nearest_marker = None
        min_distance = float('inf')

        for marker in self.markers:
            distance = abs(marker.time_ms - time_ms)
            if distance <= tolerance_ms and distance < min_distance:
                min_distance = distance
                nearest_marker = marker

        return nearest_marker

    def update_marker_label(self, marker_id: int, new_label: str) -> bool:
        """Update marker label."""
        marker = self.get_marker(marker_id)
        if not marker:
            return False

        marker.label = new_label
        self.marker_modified.emit(marker)
        print(f"[Markers] Updated marker {marker_id} label to '{new_label}'")
        return True

    def update_marker_color(self, marker_id: int, new_color: str) -> bool:
        """Update marker color."""
        marker = self.get_marker(marker_id)
        if not marker:
            return False

        marker.color = new_color
        self.marker_modified.emit(marker)
        print(f"[Markers] Updated marker {marker_id} color to '{new_color}'")
        return True

    def update_marker_time(self, marker_id: int, new_time_ms: int) -> bool:
        """Move marker to a new time position."""
        marker = self.get_marker(marker_id)
        if not marker:
            return False

        # Remove from current position
        self.markers.remove(marker)

        # Update time
        marker.time_ms = new_time_ms

        # Re-insert in sorted order
        insert_idx = 0
        for i, existing_marker in enumerate(self.markers):
            if existing_marker.time_ms > new_time_ms:
                break
            insert_idx = i + 1

        self.markers.insert(insert_idx, marker)
        self.marker_modified.emit(marker)

        print(f"[Markers] Moved marker {marker_id} to {new_time_ms}ms")
        return True

    def get_next_marker(self, current_time_ms: int) -> Optional[Marker]:
        """Get the next marker after current time."""
        for marker in self.markers:
            if marker.time_ms > current_time_ms:
                return marker
        return None

    def get_previous_marker(self, current_time_ms: int) -> Optional[Marker]:
        """Get the previous marker before current time."""
        for marker in reversed(self.markers):
            if marker.time_ms < current_time_ms:
                return marker
        return None

    def get_all_markers(self) -> List[Marker]:
        """Get all markers sorted by time."""
        return self.markers.copy()

    def get_markers_in_range(self, start_ms: int, end_ms: int) -> List[Marker]:
        """Get all markers within a time range."""
        return [m for m in self.markers if start_ms <= m.time_ms <= end_ms]

    def clear(self):
        """Remove all markers."""
        self.markers.clear()
        self._next_marker_id = 1
        self._color_index = 0
        self.markers_cleared.emit()
        print("[Markers] Cleared all markers")

    def get_marker_count(self) -> int:
        """Get number of markers."""
        return len(self.markers)

    def export_markers(self) -> List[dict]:
        """
        Export markers as list of dicts (for saving to file).

        Returns:
            List of marker dictionaries
        """
        return [
            {
                "id": m.id,
                "time_ms": m.time_ms,
                "label": m.label,
                "color": m.color
            }
            for m in self.markers
        ]

    def import_markers(self, marker_data: List[dict]):
        """
        Import markers from list of dicts (for loading from file).

        Args:
            marker_data: List of marker dictionaries
        """
        self.clear()

        for data in marker_data:
            marker = Marker(
                id=data["id"],
                time_ms=data["time_ms"],
                label=data["label"],
                color=data["color"]
            )
            self.markers.append(marker)

            # Update next ID
            if marker.id >= self._next_marker_id:
                self._next_marker_id = marker.id + 1

            self.marker_added.emit(marker)

        # Sort by time
        self.markers.sort(key=lambda m: m.time_ms)

        print(f"[Markers] Imported {len(marker_data)} markers")

    def __repr__(self):
        return f"MarkerManager(markers={len(self.markers)})"


# Example usage
if __name__ == "__main__":
    manager = MarkerManager()

    # Add markers
    m1 = manager.add_marker(5000, "Introduction")
    m2 = manager.add_marker(15000, "Main Content")
    m3 = manager.add_marker(25000, "Conclusion")

    print(f"Manager: {manager}")
    print(f"All markers: {manager.get_all_markers()}")

    # Navigate
    print(f"Next marker after 10s: {manager.get_next_marker(10000)}")
    print(f"Previous marker before 20s: {manager.get_previous_marker(20000)}")

    # Export/Import
    exported = manager.export_markers()
    print(f"Exported: {exported}")

    manager.clear()
    manager.import_markers(exported)
    print(f"After import: {manager.get_all_markers()}")
