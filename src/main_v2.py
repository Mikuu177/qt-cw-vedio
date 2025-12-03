"""
Video Editor/Player - Iteration 2
Main Entry Point

XJCO2811 User Interfaces Assessment
University of Leeds
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window_v2 import MainWindow

# Auth imports
from utils.auth_manager import AuthManager
from ui.auth_dialogs import LoginDialog


def main():
    """Main entry point for the application with authentication."""
    app = QApplication(sys.argv)

    # Set application metadata
    app.setApplicationName("Video Editor/Player")
    app.setOrganizationName("XJCO2811")
    app.setOrganizationDomain("leeds.ac.uk")

    # Auth: force login before showing main window
    auth = AuthManager()
    login = LoginDialog(auth)
    result = login.exec_()
    if result != login.Accepted or auth.current_user is None:
        # User cancelled or login failed
        return 0

    # Create and show main window
    window = MainWindow(app, auth)
    window.show()

    # Start event loop
    return app.exec_()


if __name__ == "__main__":
    import sys as _sys
    _sys.exit(main())
