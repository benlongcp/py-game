#!/usr/bin/env python3
"""
Demo script to showcase the FPS counter overlay feature.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from game_engine import GameEngine
from split_screen import SplitScreenView


def demo_fps_counter():
    """Demonstrate the FPS counter feature."""
    print("🎯 FPS Counter Demo")
    print("==================")
    print("• Real-time FPS display at bottom center of window")
    print("• Updates every second with current frame rate")
    print("• Semi-transparent background for easy reading")
    print("• Configurable via SHOW_FPS_COUNTER in config.py")
    print("• Target: ~60 FPS for smooth gameplay")
    print()
    print("Controls:")
    print("Player 1 (Red): Arrow Keys + Enter")
    print("Player 2 (Purple): WASD + Ctrl")
    print()
    print("📊 Watch the FPS counter as you play!")
    print("   • Should maintain ~60 FPS during normal gameplay")
    print("   • May drop during intensive actions (many projectiles, etc.)")
    print("   • Useful for performance monitoring and optimization")

    app = QApplication(sys.argv)

    # Create game engine and split screen
    game_engine = GameEngine()
    game_engine.create_purple_dot()
    split_screen = SplitScreenView(game_engine)

    # Show the window
    split_screen.show()

    # Start game timer
    game_timer = QTimer()
    game_timer.timeout.connect(game_engine.update_game_state)
    game_timer.start(16)  # ~60 FPS target

    sys.exit(app.exec())


if __name__ == "__main__":
    demo_fps_counter()
