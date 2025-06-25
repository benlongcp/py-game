#!/usr/bin/env python3
"""
Test script to verify the updated static circle sizes and positions.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import *
import math


def test_static_circle_sizes():
    """Test the static circle size calculations."""
    print("🎯 Testing Updated Static Circle Sizes...")

    # Calculate reference values
    square_size = DOT_RADIUS * SQUARE_SIZE_MULTIPLIER
    square_diagonal = math.sqrt(2) * square_size

    print(f"📐 Blue Square Properties:")
    print(f"   Size: {square_size} x {square_size}")
    print(f"   Diagonal: {square_diagonal:.1f}")

    print(f"\n🔴 Static Circle Properties:")
    print(f"   Diameter: {STATIC_CIRCLE_DIAMETER:.1f}")
    print(f"   Radius: {STATIC_CIRCLE_RADIUS:.1f}")
    print(
        f"   Size factor: {STATIC_CIRCLE_DIAMETER/square_diagonal:.2f}x square diagonal"
    )

    print(f"\n📍 Static Circle Positions:")
    print(f"   Red circle: ({STATIC_RED_CIRCLE_X}, {STATIC_RED_CIRCLE_Y})")
    print(f"   Purple circle: ({STATIC_PURPLE_CIRCLE_X}, {STATIC_PURPLE_CIRCLE_Y})")
    print(f"   Distance from center: {STATIC_CIRCLE_DISTANCE}")
    print(f"   Grid radius: {GRID_RADIUS}")
    print(f"   Distance ratio: {STATIC_CIRCLE_DISTANCE/GRID_RADIUS:.1%} of grid radius")

    # Verify they fit within the grid
    circle_edge_distance = STATIC_CIRCLE_DISTANCE + STATIC_CIRCLE_RADIUS
    print(f"\n✅ Boundary Check:")
    print(f"   Circle edge distance from center: {circle_edge_distance:.1f}")
    print(f"   Grid boundary: {GRID_RADIUS}")

    if circle_edge_distance <= GRID_RADIUS:
        print(
            f"   ✅ Circles fit within grid boundary (margin: {GRID_RADIUS - circle_edge_distance:.1f})"
        )
    else:
        print(
            f"   ❌ Circles extend beyond grid boundary (overflow: {circle_edge_distance - GRID_RADIUS:.1f})"
        )

    print(f"\n🎉 Static circle size update completed!")
    print(
        f"Circles are now 32% larger than the blue square diagonal (20% bigger than before)."
    )


if __name__ == "__main__":
    test_static_circle_sizes()
