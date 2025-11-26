"""
Video Editor/Player - Main Application Entry Point

XJCO2811 User Interfaces Assessment
University of Leeds

This is the main entry point for the video editor/player application.
Based on the Tomeo application framework with enhanced features.
"""

import sys
from PyQt5.QtWidgets import QApplication
# Use OpenCV backend for better codec support on Windows
from ui.main_window_opencv import MainWindow


def main():
    """
    Initialize and run the application.
    """
    # Create the Qt application instance
    app = QApplication(sys.argv)

    # Set application metadata
    app.setApplicationName("Video Editor/Player")
    app.setOrganizationName("University of Leeds")
    app.setApplicationVersion("1.0.0 - Iteration 1")

    # Create and show the main window
    window = MainWindow()
    window.show()

    # Start the event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
