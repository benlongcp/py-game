"""
Main entry point for the Topographical Plane application.
Creates and runs the PyQt6 application.
"""

import sys
from PyQt6.QtWidgets import QApplication
from topographical_plane import TopographicalPlane


def main():
    """Create and run the application."""
    # Create QApplication instance
    app = QApplication(sys.argv)

    # Create main window
    window = TopographicalPlane()
    window.show()

    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
