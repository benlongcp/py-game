#!/usr/bin/env python3
"""
Quick test to verify that centering and scaling issues are fixed.
This creates a window that starts resizable and tests maximization behavior.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from split_screen import SplitScreenView
from game_engine import GameEngine


class CenteringTestWindow(QMainWindow):
    """Test window for verifying centering fixes."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Centering Fix Test - Try Maximizing!")

        # Create game engine
        self.game_engine = GameEngine()

        # Create split screen view
        self.split_screen = SplitScreenView(self.game_engine)
        self.setCentralWidget(self.split_screen)

        # Start with a medium size, but allow resizing
        self.resize(1000, 600)

        # Show instructions
        print("CENTERING FIX TEST:")
        print("1. Window should start resizable")
        print("2. Try maximizing the window")
        print("3. Check that player views are centered")
        print("4. Check that play area extends to edges")
        print("5. Try resizing the window")
        print("6. Press Escape to close")

    def keyPressEvent(self, event):
        """Handle key events."""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            # Pass other events to the split screen
            self.split_screen.keyPressEvent(event)

    def keyReleaseEvent(self, event):
        """Handle key release events."""
        self.split_screen.keyReleaseEvent(event)


def main():
    """Run the centering test."""
    app = QApplication(sys.argv)

    window = CenteringTestWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
