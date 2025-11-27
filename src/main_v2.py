"""
Video Editor/Player - Iteration 2
Main Entry Point

XJCO2811 User Interfaces Assessment
University of Leeds
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window_v2 import MainWindow


def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)

    # Set application metadata
    app.setApplicationName("Video Editor/Player")
    app.setOrganizationName("XJCO2811")
    app.setOrganizationDomain("leeds.ac.uk")

    # Create and show main window
    window = MainWindow(app)
    window.show()

    # Start event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
