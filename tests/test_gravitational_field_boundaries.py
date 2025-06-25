#!/usr/bin/env python3
"""
Test script to verify the gravitational field extends exactly one radius beyond the static circle boundary.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from objects import BlueSquare, RedGravitationalDot
from config import *
import math


def test_gravitational_field_boundaries():
    """Test that gravitational field extends exactly one radius beyond static circle boundary."""
    print("🎯 Testing Gravitational Field Boundary Extension...")

    blue_square = BlueSquare()
    red_gravity_dot = RedGravitationalDot()

    print(f"📊 Boundary Analysis:")
    print(f"   Static circle radius: {STATIC_CIRCLE_RADIUS:.1f} pixels")
    print(f"   Static circle boundary: {STATIC_CIRCLE_RADIUS:.1f} pixels from center")
    print(f"   Gravitational field radius: {GRAVITY_MAX_DISTANCE:.1f} pixels")
    print(
        f"   Field extension beyond boundary: {GRAVITY_MAX_DISTANCE - STATIC_CIRCLE_RADIUS:.1f} pixels"
    )
    print(f"   Expected extension (1 radius): {STATIC_CIRCLE_RADIUS:.1f} pixels")

    # Verify the extension is exactly one radius
    expected_extension = STATIC_CIRCLE_RADIUS
    actual_extension = GRAVITY_MAX_DISTANCE - STATIC_CIRCLE_RADIUS

    print(f"\n✅ Boundary Verification:")
    if abs(actual_extension - expected_extension) < 0.1:
        print(f"   ✅ PASS: Field extends exactly one radius beyond boundary")
        print(
            f"   ✅ Expected: {expected_extension:.1f}, Actual: {actual_extension:.1f}"
        )
    else:
        print(f"   ❌ FAIL: Field extension mismatch")
        print(
            f"   ❌ Expected: {expected_extension:.1f}, Actual: {actual_extension:.1f}"
        )

    # Test key boundary points
    print(f"\n🎯 Testing Key Boundary Points:")
    test_points = [
        ("Circle center", 0),
        ("Circle edge", STATIC_CIRCLE_RADIUS),
        ("Just outside circle", STATIC_CIRCLE_RADIUS + 1),
        ("Halfway to field edge", STATIC_CIRCLE_RADIUS + (STATIC_CIRCLE_RADIUS / 2)),
        ("Near field edge", GRAVITY_MAX_DISTANCE - 1),
        ("Field boundary", GRAVITY_MAX_DISTANCE),
        ("Just outside field", GRAVITY_MAX_DISTANCE + 1),
    ]

    for description, distance in test_points:
        # Position square at this distance from gravity dot
        blue_square.x = red_gravity_dot.x + distance
        blue_square.y = red_gravity_dot.y
        blue_square.velocity_x = 0.0
        blue_square.velocity_y = 0.0

        # Check gravitational effect
        gravity_applied = red_gravity_dot.apply_gravity_to_object(blue_square)

        inside_circle = distance <= STATIC_CIRCLE_RADIUS
        inside_field = distance <= GRAVITY_MAX_DISTANCE

        print(
            f"   {description:20} (d={distance:5.1f}): Circle={inside_circle:1} Field={inside_field:1} Gravity={gravity_applied:1}"
        )

    print(f"\n🌍 Gravitational Field Summary:")
    print(f"   • Total field radius: {GRAVITY_MAX_DISTANCE:.1f} pixels")
    print(f"   • Covers static circle + {actual_extension:.1f} pixel extension")
    print(
        f"   • Blue square affected from center to {GRAVITY_MAX_DISTANCE:.1f} pixels away"
    )
    print(f"   • Much larger 'capture zone' for strategic gameplay")


if __name__ == "__main__":
    test_gravitational_field_boundaries()
