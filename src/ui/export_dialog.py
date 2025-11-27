"""
Export Dialog - Video Export with Quality Settings

Allows users to export edited videos with quality presets.
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QLineEdit, QFileDialog, QProgressBar, QMessageBox, QGroupBox
)
from PyQt5.QtCore import Qt, pyqtSignal
import os


class ExportDialog(QDialog):
    """
    Dialog for exporting video with quality settings.

    Signals:
        export_started: Emitted when export begins
        export_completed: Emitted when export finishes (success: bool, output_path: str)
    """

    export_started = pyqtSignal()
    export_completed = pyqtSignal(bool, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.output_path = ""
        self.quality = "high"

        self.setWindowTitle("Export Video")
        self.setModal(True)
        self.setMinimumWidth(500)

        self.init_ui()

    def init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        title = QLabel("Export Video")
        title.setStyleSheet("font-size: 14pt; font-weight: bold;")
        layout.addWidget(title)

        layout.addSpacing(10)

        # Output file section
        output_group = QGroupBox("Output File")
        output_layout = QVBoxLayout()
        output_group.setLayout(output_layout)

        file_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("Select output file path...")
        self.path_edit.setReadOnly(True)
        file_layout.addWidget(self.path_edit)

        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_output)
        file_layout.addWidget(browse_btn)

        output_layout.addLayout(file_layout)
        layout.addWidget(output_group)

        # Quality settings section
        quality_group = QGroupBox("Quality Settings")
        quality_layout = QVBoxLayout()
        quality_group.setLayout(quality_layout)

        quality_select_layout = QHBoxLayout()
        quality_label = QLabel("Quality Preset:")
        quality_select_layout.addWidget(quality_label)

        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["High (1080p, CRF 18)", "Medium (720p, CRF 23)", "Low (480p, CRF 28)"])
        self.quality_combo.setCurrentIndex(0)
        self.quality_combo.currentIndexChanged.connect(self.on_quality_changed)
        quality_select_layout.addWidget(self.quality_combo)
        quality_select_layout.addStretch()

        quality_layout.addLayout(quality_select_layout)

        # Quality info
        self.quality_info = QLabel()
        self.quality_info.setStyleSheet("font-size: 9pt; color: #666;")
        self.update_quality_info()
        quality_layout.addWidget(self.quality_info)

        layout.addWidget(quality_group)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel()
        self.status_label.setStyleSheet("font-size: 9pt; color: #0078d4;")
        self.status_label.setVisible(False)
        layout.addWidget(self.status_label)

        layout.addSpacing(10)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.export_btn = QPushButton("Export")
        self.export_btn.setMinimumWidth(100)
        self.export_btn.clicked.connect(self.start_export)
        button_layout.addWidget(self.export_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setMinimumWidth(100)
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)

    def browse_output(self):
        """Browse for output file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Video As",
            "",
            "MP4 Video (*.mp4);;All Files (*.*)"
        )

        if file_path:
            # Ensure .mp4 extension
            if not file_path.lower().endswith('.mp4'):
                file_path += '.mp4'

            self.output_path = file_path
            self.path_edit.setText(file_path)

    def on_quality_changed(self, index: int):
        """Handle quality selection change."""
        quality_map = {0: "high", 1: "medium", 2: "low"}
        self.quality = quality_map.get(index, "high")
        self.update_quality_info()

    def update_quality_info(self):
        """Update quality information text."""
        info_text = {
            "high": "Best quality | Larger file size | H.264, 1080p, CRF 18, 192k audio",
            "medium": "Balanced quality | Moderate file size | H.264, 720p, CRF 23, 128k audio",
            "low": "Smaller file size | Lower quality | H.264, 480p, CRF 28, 96k audio"
        }
        self.quality_info.setText(info_text.get(self.quality, ""))

    def start_export(self):
        """Start the export process."""
        if not self.output_path:
            QMessageBox.warning(
                self,
                "No Output File",
                "Please select an output file path."
            )
            return

        # Check if file exists
        if os.path.exists(self.output_path):
            reply = QMessageBox.question(
                self,
                "File Exists",
                f"The file '{os.path.basename(self.output_path)}' already exists.\nOverwrite?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply != QMessageBox.Yes:
                return

        # Disable controls during export
        self.export_btn.setEnabled(False)
        self.quality_combo.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.status_label.setVisible(True)
        self.status_label.setText("Preparing export...")

        self.export_started.emit()

        # Note: Actual export would be handled by parent window
        # This dialog just collects settings
        # Parent will connect to signals and call set_progress(), set_status(), etc.

    def set_progress(self, percentage: int):
        """Update progress bar."""
        self.progress_bar.setValue(percentage)

    def set_status(self, message: str):
        """Update status message."""
        self.status_label.setText(message)

    def on_export_completed(self, success: bool, message: str):
        """Handle export completion."""
        self.progress_bar.setVisible(False)
        self.export_btn.setEnabled(True)
        self.quality_combo.setEnabled(True)

        if success:
            self.status_label.setStyleSheet("font-size: 9pt; color: #00aa00;")
            self.status_label.setText(f"✓ Export completed: {message}")

            QMessageBox.information(
                self,
                "Export Successful",
                f"Video exported successfully to:\n{message}"
            )

            self.export_completed.emit(True, message)
            self.accept()

        else:
            self.status_label.setStyleSheet("font-size: 9pt; color: #cc0000;")
            self.status_label.setText(f"✗ Export failed: {message}")

            QMessageBox.critical(
                self,
                "Export Failed",
                f"Export failed:\n{message}"
            )

            self.export_completed.emit(False, message)

    def get_export_settings(self):
        """
        Get export settings as dictionary.

        Returns:
            dict with keys: output_path, quality
        """
        return {
            "output_path": self.output_path,
            "quality": self.quality
        }


# Testing
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    dialog = ExportDialog()

    def on_export_started():
        print("Export started!")
        # Simulate progress
        import time
        for i in range(0, 101, 10):
            time.sleep(0.2)
            dialog.set_progress(i)
            dialog.set_status(f"Exporting... {i}%")

        dialog.on_export_completed(True, "/path/to/output.mp4")

    dialog.export_started.connect(on_export_started)

    result = dialog.exec_()

    if result == QDialog.Accepted:
        settings = dialog.get_export_settings()
        print(f"Export settings: {settings}")

    sys.exit(0)
