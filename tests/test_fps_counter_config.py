#!/usr/bin/env python3
"""
Test script to verify FPS counter can be disabled via configuration.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from game_engine import GameEngine
from split_screen import SplitScreenView
import config


def test_fps_counter_disabled():
    """Test that FPS counter can be disabled via config."""
    print("🔧 Testing FPS Counter Configuration...")

    # Temporarily disable the FPS counter
    original_setting = config.SHOW_FPS_COUNTER
    config.SHOW_FPS_COUNTER = False

    app = QApplication(sys.argv)

    # Create game engine and split screen
    game_engine = GameEngine()
    game_engine.create_purple_dot()
    split_screen = SplitScreenView(game_engine)

    print("✅ Split screen created with FPS counter disabled")
    print("📊 FPS counter should NOT appear at the bottom of the window")
    print("💡 This demonstrates the configurable nature of the FPS counter")

    # Show the window
    split_screen.show()

    # Start game timer
    game_timer = QTimer()
    game_timer.timeout.connect(game_engine.update_game_state)
    game_timer.start(16)

    # Auto-close after 3 seconds
    def close_test():
        print("✅ FPS counter configuration test completed!")
        print("🔧 Restoring original FPS counter setting...")
        config.SHOW_FPS_COUNTER = original_setting
        app.quit()

    close_timer = QTimer()
    close_timer.timeout.connect(close_test)
    close_timer.start(3000)  # 3 seconds

    print("🚀 Window will close automatically in 3 seconds...")
    print("   • Verify that NO FPS counter appears at bottom")

    sys.exit(app.exec())


if __name__ == "__main__":
    test_fps_counter_disabled()
