#!/usr/bin/env python3
"""
Demo script to showcase the off-screen indicator feature.
Move around to see the blue arrow point toward the off-screen blue square.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from split_screen import SplitScreenView
from game_engine import GameEngine


def demo_off_screen_indicator():
    """Demo the off-screen indicator feature."""
    print("🎯 Off-Screen Indicator Demo")
    print("=" * 50)
    print("CONTROLS:")
    print("Player 1 (Red): Arrow Keys + Enter")
    print("Player 2 (Purple): WASD + Ctrl")
    print("")
    print("INSTRUCTIONS:")
    print("1. Move your player around using the controls")
    print("2. When the blue square goes off-screen, you'll see a small blue arrow")
    print("3. The arrow points in the direction of the blue square")
    print("4. Both players have independent off-screen indicators")
    print("5. Try hitting the blue square with projectiles to move it off-screen")
    print("")
    print("Starting demo...")

    app = QApplication(sys.argv)

    # Create game engine and set up interesting initial positions
    engine = GameEngine()
    engine.create_purple_dot()

    # Move blue square to an interesting position (off-screen from start)
    engine.blue_square.x = 600  # Far to the right
    engine.blue_square.y = -300  # And up

    # Move players to different positions
    engine.red_dot.virtual_x = 100
    engine.red_dot.virtual_y = 100

    engine.purple_dot.virtual_x = -100
    engine.purple_dot.virtual_y = -100

    # Create split-screen view
    view = SplitScreenView(engine)
    view.show()

    print("✅ Demo window opened!")
    print("Move around to see the off-screen indicators in action!")

    sys.exit(app.exec())


if __name__ == "__main__":
    demo_off_screen_indicator()
