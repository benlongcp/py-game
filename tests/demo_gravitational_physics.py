#!/usr/bin/env python3
"""
Interactive demo showcasing the gravitational dots feature.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from split_screen import SplitScreenView
from game_engine import GameEngine


def demo_gravitational_physics():
    """Demo the gravitational physics in the split-screen view."""
    print("🌍 Gravitational Dots Demo")
    print("=" * 50)
    print("FEATURES:")
    print("- Transparent gravitational dots inside red and purple static circles")
    print("- Blue square gets pulled toward gravity dots when overlapping circles")
    print("- Gravitational force decreases with distance from center")
    print("")
    print("CONTROLS:")
    print("Player 1 (Red): Arrow Keys + Enter")
    print("Player 2 (Purple): WASD + Ctrl")
    print("")
    print("HOW TO TEST:")
    print("1. Use projectiles to hit the blue square toward the static circles")
    print("2. Watch the blue square get pulled toward the center when it overlaps")
    print("3. Notice the transparent gray dots in the center of each static circle")
    print("4. Experiment with different angles and speeds")
    print("")
    print("Starting demo...")

    app = QApplication(sys.argv)

    # Create game engine and add second player
    engine = GameEngine()
    engine.create_purple_dot()

    # Position blue square closer to one of the gravitational circles for testing
    engine.blue_square.x = -750  # Near the red gravitational circle
    engine.blue_square.y = 0

    # Create split-screen view
    window = SplitScreenView(engine)
    window.show()

    print("✅ Demo window opened!")
    print(
        "Shoot the blue square toward the static circles to see gravitational effects!"
    )

    return app.exec()


if __name__ == "__main__":
    demo_gravitational_physics()
