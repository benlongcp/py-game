#!/usr/bin/env python3
"""
Quick test to see the black hole in action in the game.
This will spawn the game and you can see the black hole moving around.
"""

from objects import BlackHole
from config import *
import math


def test_black_hole_in_game():
    """Show information about the black hole in the current game."""
    hole = BlackHole()

    print("Black Hole Information")
    print("=====================")
    print(f"Initial Position: ({hole.x:.1f}, {hole.y:.1f})")
    print(f"Radius: {hole.radius:.1f} (compare to blue square size)")
    print(f"Gravity Strength: {hole.gravity_strength} (10x goal circles)")
    print(f"Gravity Range: {hole.max_gravity_distance:.1f}")
    print(f"Visual Gradient Radius: {hole.gradient_radius:.1f}")
    print()

    print("Gameplay Effects:")
    print("- Players will be pulled toward the black hole when nearby")
    print("- Projectiles will curve toward the black hole")
    print("- The blue cube will be strongly affected")
    print("- Creates unpredictable physics interactions")
    print("- The black hole moves slowly and randomly")
    print()

    print("Visual Appearance:")
    print("- Solid black circle in center")
    print("- Dark gradient fading to transparent")
    print("- About the size of the blue square/cube")
    print("- Moves around the elliptical play area")
    print()

    print("Tips for testing:")
    print("- Shoot projectiles near the black hole to see them curve")
    print("- Move your ship close to feel the gravitational pull")
    print("- Watch the blue cube get pulled around")
    print("- Notice how the black hole bounces off the arena edges")


if __name__ == "__main__":
    test_black_hole_in_game()
    print("\nThe game is now running with a black hole!")
    print("Look for the dark circular object moving around the arena.")
    print("Have fun experimenting with the new gravitational dynamics!")
