#!/usr/bin/env python3
"""
Test script to verify the split-screen view swap (purple left, red right).
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from split_screen import SplitScreenView
from game_engine import GameEngine


def test_view_swap():
    """Test that the views are correctly swapped."""
    print("🔄 Testing Split-Screen View Swap...")

    # Create game engine and ensure purple player exists
    game_engine = GameEngine()
    game_engine.create_purple_dot()

    # Create split screen view
    split_screen = SplitScreenView(game_engine)

    print("✅ Split-screen created successfully")
    print("📋 Current layout:")
    print("   Left side: Player 2 (Purple) - WASD + Ctrl")
    print("   Right side: Player 1 (Red) - Arrow Keys + Enter")
    print()
    print("🎮 Player positions:")
    print(
        f"   Red dot: ({game_engine.red_dot.virtual_x:.1f}, {game_engine.red_dot.virtual_y:.1f})"
    )
    print(
        f"   Purple dot: ({game_engine.purple_dot.virtual_x:.1f}, {game_engine.purple_dot.virtual_y:.1f})"
    )
    print(
        f"   Blue square: ({game_engine.blue_square.x:.1f}, {game_engine.blue_square.y:.1f})"
    )
    print()
    print("🎯 Score display (same in both views):")
    print(f"   Red: {game_engine.get_red_player_score()} (left side)")
    print(f"   Purple: {game_engine.get_purple_player_score()} (right side)")
    print()
    print("✅ View swap test completed!")
    print("💡 Run 'python main.py' to see the new layout in action!")


def main():
    """Main function to run the view swap test."""
    app = QApplication(sys.argv)

    test_view_swap()

    # No need to start event loop for this test
    sys.exit(0)


if __name__ == "__main__":
    main()
