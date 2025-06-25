#!/usr/bin/env python3
"""
Simple debug test to check what's happening with player speed.
"""

import sys
import os
import math

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from game_engine import GameEngine
from config import *


def debug_speed():
    """Debug player speed calculation."""
    print("=== Debug Player Speed ===\n")

    game_engine = GameEngine()

    print(
        f"Initial red dot speed: {math.sqrt(game_engine.red_dot.velocity_x**2 + game_engine.red_dot.velocity_y**2):.6f}"
    )

    # Apply acceleration for exactly 1000 frames and see what happens
    for frame in range(1000):
        old_speed = math.sqrt(
            game_engine.red_dot.velocity_x**2 + game_engine.red_dot.velocity_y**2
        )

        # Reset acceleration (like game engine does)
        game_engine.red_dot.acceleration_x = 0
        game_engine.red_dot.acceleration_y = 0

        # Apply acceleration
        game_engine.red_dot.acceleration_x = ACCELERATION

        if frame < 10 or frame % 100 == 0:
            print(
                f"Frame {frame}: Before physics - Speed={old_speed:.6f}, Pos=({game_engine.red_dot.virtual_x:.1f}, {game_engine.red_dot.virtual_y:.1f}), Acc=({game_engine.red_dot.acceleration_x:.3f}, {game_engine.red_dot.acceleration_y:.3f})"
            )

        game_engine.red_dot.update_physics()

        new_speed = math.sqrt(
            game_engine.red_dot.velocity_x**2 + game_engine.red_dot.velocity_y**2
        )
        if frame < 10 or frame % 100 == 0:
            distance_from_center = math.sqrt(
                game_engine.red_dot.virtual_x**2 + game_engine.red_dot.virtual_y**2
            )
            print(
                f"Frame {frame}: After physics  - Speed={new_speed:.6f}, Pos=({game_engine.red_dot.virtual_x:.1f}, {game_engine.red_dot.virtual_y:.1f}), Distance={distance_from_center:.1f}"
            )

        # Check for equilibrium
        if frame > 100 and abs(new_speed - old_speed) < 0.000001:
            print(f"Equilibrium reached at frame {frame}, speed = {new_speed:.6f}")
            break

    print(f"Final speed: {new_speed:.6f}")
    print(
        f"Expected equilibrium: {ACCELERATION * DECELERATION / (1 - DECELERATION):.6f}"
    )


def main():
    """Main function."""
    app = QApplication(sys.argv)
    debug_speed()
    sys.exit(0)


if __name__ == "__main__":
    main()
