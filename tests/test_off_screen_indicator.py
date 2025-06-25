#!/usr/bin/env python3
"""
Test script for the off-screen indicator feature.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import GameEngine
from objects import BlueSquare
from rendering import Renderer
from config import *


def test_off_screen_indicator():
    """Test the off-screen indicator functionality."""
    print("🎯 Testing Off-Screen Indicator Feature...")

    # Create test objects
    blue_square = BlueSquare(500, 500)  # Position square far from center

    # Test various camera positions
    test_scenarios = [
        ("Square far right", 0, 0, 500, 500),
        ("Square far left", 0, 0, -500, 0),
        ("Square far up", 0, 0, 0, -500),
        ("Square far down", 0, 0, 0, 500),
        ("Square diagonal", 0, 0, 300, 300),
        ("Square visible", 0, 0, 50, 50),  # Should be visible, no indicator
    ]

    for scenario_name, camera_x, camera_y, square_x, square_y in test_scenarios:
        print(f"\n📍 {scenario_name}:")

        # Set square position
        blue_square.x = square_x
        blue_square.y = square_y

        # Check visibility
        is_visible = blue_square.is_visible(camera_x, camera_y)
        screen_x, screen_y = blue_square.get_screen_position(camera_x, camera_y)

        print(f"   Square world pos: ({square_x}, {square_y})")
        print(f"   Camera pos: ({camera_x}, {camera_y})")
        print(f"   Square screen pos: ({screen_x:.1f}, {screen_y:.1f})")
        print(f"   Is visible: {is_visible}")

        if not is_visible:
            # Calculate direction for indicator
            dx = square_x - camera_x
            dy = square_y - camera_y
            import math

            angle = math.atan2(dy, dx)
            angle_degrees = math.degrees(angle)

            print(
                f"   Direction to square: {angle_degrees:.1f}° (angle: {angle:.2f} rad)"
            )
            print(f"   ✅ Off-screen indicator should appear")
        else:
            print(f"   ❌ No off-screen indicator needed")

    print(f"\n🎉 Off-screen indicator test completed!")
    print(f"The blue arrows should point toward the blue square when it's off-screen.")


if __name__ == "__main__":
    test_off_screen_indicator()
