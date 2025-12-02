"""
Help Dialog - Keyboard Shortcuts Reference

Shows all available keyboard shortcuts in an easy-to-read format.
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# i18n
import os as _os
import sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from utils.i18n_manager import i18n


class HelpDialog(QDialog):
    """Dialog showing keyboard shortcuts and help information."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(i18n.t("help.title", "Keyboard Shortcuts & Help"))
        self.setModal(False)
        self.setMinimumSize(700, 600)

        self.init_ui()

    def init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        title = QLabel(i18n.t("help.title", "Keyboard Shortcuts & Help"))
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Tab widget for categories
        tabs = QTabWidget()
        layout.addWidget(tabs)

        # Create tabs
        tabs.addTab(self.create_file_shortcuts(), i18n.t("help.tabs.file", "File"))
        tabs.addTab(self.create_edit_shortcuts(), i18n.t("help.tabs.edit", "Edit"))
        tabs.addTab(self.create_playback_shortcuts(), i18n.t("help.tabs.playback", "Playback"))
        tabs.addTab(self.create_markers_shortcuts(), i18n.t("help.tabs.markers", "Markers"))
        tabs.addTab(self.create_view_shortcuts(), i18n.t("help.tabs.view", "View"))

        # Close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        close_btn = QPushButton(i18n.t("help.btn_close", "Close"))
        close_btn.setMinimumWidth(100)
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

    def create_file_shortcuts(self):
        """Create file operations shortcuts table."""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        shortcuts = [
            ("Ctrl+O", "Open video file", "Opens file dialog to load a video"),
            ("Ctrl+E", "Export video", "Opens export dialog to save edited video"),
            ("Ctrl+Q", "Quit application", "Closes the application"),
        ]

        table = self.create_shortcuts_table(shortcuts)
        layout.addWidget(table)

        return widget

    def create_edit_shortcuts(self):
        """Create editing shortcuts table."""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        shortcuts = [
            ("Ctrl+Z", "Undo", "Undo last action (add/remove clip or marker)"),
            ("Ctrl+Y", "Redo", "Redo previously undone action"),
            ("Ctrl+T", "Toggle trim mode", "Enable/disable trim mode for cutting video"),
            ("I", "Set In point", "Mark start of trim range at current position"),
            ("O", "Set Out point", "Mark end of trim range at current position"),
        ]

        table = self.create_shortcuts_table(shortcuts)
        layout.addWidget(table)

        return widget

    def create_playback_shortcuts(self):
        """Create playback control shortcuts table."""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        shortcuts = [
            ("Space", "Play/Pause", "Toggle video playback"),
            ("Left Arrow", "Seek backward 5s", "Move 5 seconds backward"),
            ("Right Arrow", "Seek forward 5s", "Move 5 seconds forward"),
            ("Up Arrow", "Volume up", "Increase volume by 5%"),
            ("Down Arrow", "Volume down", "Decrease volume by 5%"),
            ("M", "Mute/Unmute", "Toggle audio mute (note: OpenCV has no audio)"),
        ]

        table = self.create_shortcuts_table(shortcuts)
        layout.addWidget(table)

        # Add note about OpenCV
        note = QLabel("Note: OpenCV backend does not support audio playback.")
        note.setStyleSheet("color: #666; font-style: italic; padding: 10px;")
        layout.addWidget(note)

        return widget

    def create_markers_shortcuts(self):
        """Create marker navigation shortcuts table."""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        shortcuts = [
            ("M", "Add marker", "Add a marker at current video position"),
            ("[", "Previous marker", "Jump to previous marker"),
            ("]", "Next marker", "Jump to next marker"),
        ]

        table = self.create_shortcuts_table(shortcuts)
        layout.addWidget(table)

        # Add explanation
        info = QLabel(
            "Markers help you navigate long videos by marking important moments.\n"
            "Click on marker flags in the timeline to jump directly to that position."
        )
        info.setWordWrap(True)
        info.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 4px;")
        layout.addWidget(info)

        return widget

    def create_view_shortcuts(self):
        """Create view control shortcuts table."""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        shortcuts = [
            ("F", "Fullscreen", "Toggle fullscreen mode"),
            ("Escape", "Exit fullscreen", "Return to normal window mode"),
            ("Ctrl+Shift+H", "High contrast mode", "Toggle high contrast theme for accessibility"),
        ]

        table = self.create_shortcuts_table(shortcuts)
        layout.addWidget(table)

        # Add accessibility info
        info = QLabel(
            "High Contrast Mode (WCAG 2.1 Level AAA):\n"
            "• Black background with yellow/white text\n"
            "• 19:1 contrast ratio (exceeds 7:1 requirement)\n"
            "• Bold fonts and thick borders\n"
            "• Enhanced focus indicators\n\n"
            "Designed for users with visual impairments."
        )
        info.setWordWrap(True)
        info.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 4px;")
        layout.addWidget(info)

        return widget

    def create_shortcuts_table(self, shortcuts):
        """
        Create a table widget from shortcuts list.

        Args:
            shortcuts: List of (key, action, description) tuples

        Returns:
            QTableWidget configured with shortcuts
        """
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels([
            i18n.t("help.table.shortcut", "Shortcut"),
            i18n.t("help.table.action", "Action"),
            i18n.t("help.table.desc", "Description")
        ])
        table.setRowCount(len(shortcuts))

        # Populate table
        for row, (key, action, description) in enumerate(shortcuts):
            # Shortcut key
            key_item = QTableWidgetItem(key)
            key_font = QFont()
            key_font.setBold(True)
            key_item.setFont(key_font)
            table.setItem(row, 0, key_item)

            # Action
            action_item = QTableWidgetItem(action)
            table.setItem(row, 1, action_item)

            # Description
            desc_item = QTableWidgetItem(description)
            table.setItem(row, 2, desc_item)

        # Configure header
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setSelectionMode(QTableWidget.SingleSelection)

        return table
