#!/usr/bin/env python3
"""
Template for test scripts in the tests/ folder.
Copy this template when creating new test files.
"""

import sys
import os

# Add parent directory to path for imports (required for tests/ folder)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import from the main project
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from game_engine import GameEngine
from split_screen import SplitScreenView

# Add other imports as needed


def main():
    """Main test function."""
    app = QApplication(sys.argv)

    print("Test Template")
    print("=============")
    print("This is a template for test scripts.")
    print("Replace this with your actual test logic.")

    # Example: Create game engine and view
    game_engine = GameEngine()
    game_engine.create_purple_dot()  # For multiplayer tests

    split_screen = SplitScreenView(game_engine)
    split_screen.show()

    # Setup game timer
    game_timer = QTimer()
    game_timer.timeout.connect(game_engine.update_game_state)
    game_timer.start(16)  # ~60 FPS

    # Add your test logic here
    print("Test is running... Close the window to exit.")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
