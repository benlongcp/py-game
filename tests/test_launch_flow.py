#!/usr/bin/env python3
"""
Test script for complete launch-to-game flow.
Tests keyboard input transition from launch screen to game.
"""

import sys
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QKeyEvent
from main import MultiPlayerController


def test_launch_to_game_flow():
    """Test the full launch screen to game transition."""
    print("Testing launch screen to game transition...")

    # Create QApplication instance
    app = QApplication(sys.argv)

    # Create controller and show launch screen
    controller = MultiPlayerController()
    controller.start_launch_screen()

    # Simulate a key press after 2 seconds
    def simulate_key_press():
        print("Simulating key press to start game...")
        launch_screen = controller.launch_screen
        if launch_screen:
            # Create a fake key press event (Space key)
            key_event = QKeyEvent(
                QKeyEvent.Type.KeyPress,
                Qt.Key.Key_Space,
                Qt.KeyboardModifier.NoModifier,
            )
            launch_screen.keyPressEvent(key_event)

    # Auto-close after 5 seconds total (2s + 3s for game)
    def auto_close():
        print("Auto-closing test...")
        app.quit()

    key_timer = QTimer()
    key_timer.timeout.connect(simulate_key_press)
    key_timer.start(2000)  # 2 seconds

    close_timer = QTimer()
    close_timer.timeout.connect(auto_close)
    close_timer.start(5000)  # 5 seconds total

    print("Launch screen visible for 2 seconds, then simulating spacebar press...")
    print("Game should start and run for 3 more seconds...")

    # Run the application
    app.exec()
    print("Launch to game flow test completed!")


if __name__ == "__main__":
    test_launch_to_game_flow()
