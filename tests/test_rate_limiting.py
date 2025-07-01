#!/usr/bin/env python3
"""
Test script to demonstrate the projectile rate limiting system.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from game_engine import GameEngine
from split_screen import SplitScreenView
from config import *


def test_rate_limiting():
    """Test the projectile rate limiting system."""
    app = QApplication(sys.argv)

    # Create game engine and split screen
    game_engine = GameEngine()
    game_engine.create_purple_dot()
    split_screen = SplitScreenView(game_engine)

    frame_count = 0

    def debug_frame():
        nonlocal frame_count
        frame_count += 1

        # Show rate limiter status every 30 frames
        if frame_count % 30 == 0:
            p1_data = game_engine.get_player1_rate_limiter_progress()
            p2_data = game_engine.get_player2_rate_limiter_progress()

            print(f"\n=== Frame {frame_count} ===")
            print(f"Player 1 Rate Limiter:")
            print(f"  Type: {p1_data['type']}")
            print(f"  Progress: {p1_data['progress']:.2f}")
            print(f"  Time Remaining: {p1_data['time_remaining']:.1f}s")

            print(f"Player 2 Rate Limiter:")
            print(f"  Type: {p2_data['type']}")
            print(f"  Progress: {p2_data['progress']:.2f}")
            print(f"  Time Remaining: {p2_data['time_remaining']:.1f}s")

            print(f"Total Projectiles: {len(game_engine.projectiles)}")

    debug_timer = QTimer()
    debug_timer.timeout.connect(debug_frame)
    debug_timer.start(16)  # Run at same rate as game

    split_screen.show()

    # Start game timer
    game_timer = QTimer()
    game_timer.timeout.connect(game_engine.update_game_state)
    game_timer.start(16)

    print("🎮 Rate Limiting Test Mode")
    print("💡 Rapidly press the shooting button to test rate limiting")
    print("🎯 Player 1: Enter key (keyboard) or A button (gamepad)")
    print("🎯 Player 2: Left Ctrl (keyboard) or A button (gamepad)")
    print("📊 Watch the pie chart indicators fill up as you shoot")
    print("🔴 When you hit 5 shots in 1 second, you'll enter a 1-second cooldown")
    print("Close the game window to exit.")

    sys.exit(app.exec())


if __name__ == "__main__":
    test_rate_limiting()
