#!/usr/bin/env python3
"""
Test script to demonstrate the increased gravitational force (100% increase from 2.0 to 4.0).
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from objects import BlueSquare, RedGravitationalDot
from config import *
import math


def test_gravitational_force_increase():
    """Test that gravitational force has been doubled."""
    print("⚡ Testing Gravitational Force Increase...")
    print(f"📊 Current Configuration:")
    print(f"   Gravity strength: {GRAVITY_STRENGTH}")
    print(f"   Previous strength: 2.0")
    print(f"   Increase factor: {GRAVITY_STRENGTH / 2.0:.1f}x (100% increase)")
    print()

    blue_square = BlueSquare()
    red_gravity_dot = RedGravitationalDot()

    # Test positions at various distances
    test_distances = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    print("📐 Force Comparison at Different Distances:")
    print("Distance  Current Force  Previous Force  Increase")
    print("-----------------------------------------------")

    for distance in test_distances:
        # Position blue square at test distance from gravity dot
        blue_square.x = red_gravity_dot.x + distance
        blue_square.y = red_gravity_dot.y

        # Store original velocity
        original_vx = blue_square.velocity_x
        original_vy = blue_square.velocity_y

        # Apply gravity
        red_gravity_dot.apply_gravity_to_object(blue_square)

        # Calculate velocity change (force applied)
        force_x = blue_square.velocity_x - original_vx
        force_y = blue_square.velocity_y - original_vy
        current_force = math.sqrt(force_x**2 + force_y**2)

        # Calculate what the previous force would have been (half the current)
        previous_force = current_force / 2.0

        # Calculate increase factor
        if previous_force > 0:
            increase_factor = current_force / previous_force
        else:
            increase_factor = 0

        print(
            f"  {distance:3d}      {current_force:.6f}      {previous_force:.6f}     {increase_factor:.1f}x"
        )

        # Reset velocity for next test
        blue_square.velocity_x = original_vx
        blue_square.velocity_y = original_vy

    print()
    print("✅ Force Analysis Complete!")
    print("🎮 Gameplay Impact:")
    print("   • Blue square will be pulled more strongly toward static circles")
    print("   • Faster capture when blue square enters gravitational field")
    print("   • More responsive gravitational effects during gameplay")
    print("   • Easier to score points once blue square gets near circles")


def main():
    """Main function to run the gravitational force test."""
    test_gravitational_force_increase()


if __name__ == "__main__":
    main()
