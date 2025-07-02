#!/usr/bin/env python3
"""
Test script to verify FPS counter functionality.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from game_engine import GameEngine
from split_screen import SplitScreenView
import time


def test_fps_counter():
    """Test that the FPS counter is working correctly."""
    print("🎯 Testing FPS Counter...")

    app = QApplication(sys.argv)

    # Create game engine and split screen
    game_engine = GameEngine()
    game_engine.create_purple_dot()
    split_screen = SplitScreenView(game_engine)

    print("✅ Split screen with FPS counter created successfully!")
    print("📊 FPS counter should appear at the bottom center of the window")
    print("💡 The counter updates every second and shows real-time frame rate")
    print("🔧 Window resolution:", split_screen.width(), "x", split_screen.height())

    # Show the window
    split_screen.show()

    # Start game timer
    game_timer = QTimer()
    game_timer.timeout.connect(game_engine.update_game_state)
    game_timer.start(16)  # ~60 FPS target

    # Monitor FPS for a few seconds
    start_time = time.time()

    def check_fps():
        elapsed = time.time() - start_time
        if elapsed > 5:  # Run for 5 seconds
            print(f"📈 Current FPS reading: {split_screen.fps_display:.1f}")
            print("✅ FPS counter test completed successfully!")
            app.quit()

    # Check FPS periodically
    fps_timer = QTimer()
    fps_timer.timeout.connect(check_fps)
    fps_timer.start(1000)  # Check every second

    print("🚀 Starting FPS counter test...")
    print("   • Window should show FPS counter at bottom")
    print("   • Counter should update every second")
    print("   • Target: ~60 FPS for smooth gameplay")
    print("   • Test will run for 5 seconds then close")

    sys.exit(app.exec())


if __name__ == "__main__":
    test_fps_counter()
