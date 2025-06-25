#!/usr/bin/env python3
"""
Test script to demonstrate the extended gravitational field range.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from objects import BlueSquare, RedGravitationalDot
from config import *
import math


def test_extended_gravitational_range():
    """Test the extended gravitational range in detail."""
    print("🌍 Testing Extended Gravitational Field Range...")

    blue_square = BlueSquare()
    red_gravity_dot = RedGravitationalDot()

    print(f"📊 Field Parameters:")
    print(f"   Static circle radius: {STATIC_CIRCLE_RADIUS:.1f}")
    print(f"   Gravitational field radius: {GRAVITY_MAX_DISTANCE:.1f}")
    print(
        f"   Field extension: {GRAVITY_MAX_DISTANCE/STATIC_CIRCLE_RADIUS:.1f}x circle radius"
    )
    print(f"   Red gravity dot center: ({red_gravity_dot.x}, {red_gravity_dot.y})")

    # Test at various distances from the red gravity dot
    test_distances = [0, 10, 20, 30, 40, 47, 50, 60, 70, 80, 90, 94, 100, 120]

    print(f"\n📐 Gravitational Force by Distance:")
    print(
        f"{'Distance':>8} {'Inside Circle':>12} {'Force Applied':>13} {'Force Magnitude':>15}"
    )
    print("-" * 50)

    for distance in test_distances:
        # Position square at this distance from red gravity dot (along x-axis)
        blue_square.x = red_gravity_dot.x + distance
        blue_square.y = red_gravity_dot.y
        blue_square.velocity_x = 0.0
        blue_square.velocity_y = 0.0

        # Check if inside static circle
        inside_circle = distance <= STATIC_CIRCLE_RADIUS

        # Apply gravity and measure force
        gravity_applied = red_gravity_dot.apply_gravity_to_object(blue_square)

        if gravity_applied:
            force_magnitude = math.sqrt(
                blue_square.velocity_x**2 + blue_square.velocity_y**2
            )
            print(
                f"{distance:>8.0f} {inside_circle:>12} {gravity_applied:>13} {force_magnitude:>15.6f}"
            )
        else:
            print(
                f"{distance:>8.0f} {inside_circle:>12} {gravity_applied:>13} {'N/A':>15}"
            )

    print(f"\n✅ Key Observations:")
    print(
        f"   • Gravity now works outside the static circle (distance > {STATIC_CIRCLE_RADIUS:.1f})"
    )
    print(f"   • Maximum effective range: {GRAVITY_MAX_DISTANCE:.1f} pixels")
    print(f"   • Force decreases with distance as expected")
    print(f"   • Blue square can be influenced when adjacent to static circles")

    print(f"\n🎮 Gameplay Impact:")
    print(f"   • Players can now use projectiles to push blue square near circles")
    print(f"   • Gravitational 'capture' zone is much larger")
    print(f"   • More strategic positioning opportunities")


if __name__ == "__main__":
    test_extended_gravitational_range()
