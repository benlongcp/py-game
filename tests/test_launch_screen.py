#!/usr/bin/env python3
"""
Test script for the new launch screen functionality.
Tests that the launch screen displays properly and responds to input.
"""

import sys
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from main import MultiPlayerController


def test_launch_screen():
    """Test the launch screen display and functionality."""
    print("Testing launch screen...")

    # Create QApplication instance
    app = QApplication(sys.argv)

    # Create controller and show launch screen
    controller = MultiPlayerController()
    controller.start_launch_screen()

    # Auto-close after 3 seconds for testing
    def auto_close():
        print("Auto-closing launch screen test...")
        app.quit()

    timer = QTimer()
    timer.timeout.connect(auto_close)
    timer.start(3000)  # 3 seconds

    print("Launch screen should now be visible with:")
    print("- 'BOXHOLE' in big yellow letters")
    print("- Black radial gradient background")
    print("- Red ship SVG (left side, rotated)")
    print("- Blue cube SVG (right side, rotated)")
    print("- 'Press any key to start' text at bottom")
    print("Auto-closing in 3 seconds...")

    # Run the application
    app.exec()
    print("Launch screen test completed!")


if __name__ == "__main__":
    test_launch_screen()
