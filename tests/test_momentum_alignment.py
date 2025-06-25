"""
Test script to verify momentum indicator consistency between red and purple dots.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from objects import RedDot, PurpleDot
from config import *
import math


def test_momentum_indicators():
    """Test that red and purple dots generate identical momentum info."""
    print("🔺 Testing Momentum Indicator Consistency...")

    # Create both dots with identical states
    red_dot = RedDot(100, 100)
    purple_dot = PurpleDot(200, 200)

    # Set identical velocities
    red_dot.velocity_x = 5.0
    red_dot.velocity_y = 3.0
    purple_dot.velocity_x = 5.0
    purple_dot.velocity_y = 3.0

    # Get momentum info from both
    red_momentum = red_dot.get_momentum_info()
    purple_momentum = purple_dot.get_momentum_info()

    print(f"\n📊 Red Dot Momentum Info:")
    print(
        f"  Angle: {red_momentum['angle']:.4f} radians ({math.degrees(red_momentum['angle']):.1f}°)"
    )
    print(f"  Size: {red_momentum['size']:.2f}")
    print(f"  Speed: {red_momentum['speed']:.2f}")

    print(f"\n📊 Purple Dot Momentum Info:")
    print(
        f"  Angle: {purple_momentum['angle']:.4f} radians ({math.degrees(purple_momentum['angle']):.1f}°)"
    )
    print(f"  Size: {purple_momentum['size']:.2f}")
    print(f"  Speed: {purple_momentum['speed']:.2f}")

    # Check if they match
    angle_match = abs(red_momentum["angle"] - purple_momentum["angle"]) < 0.0001
    size_match = abs(red_momentum["size"] - purple_momentum["size"]) < 0.01
    speed_match = abs(red_momentum["speed"] - purple_momentum["speed"]) < 0.01

    print(f"\n✅ Consistency Check:")
    print(f"  Angle Match: {'✅' if angle_match else '❌'}")
    print(f"  Size Match: {'✅' if size_match else '❌'}")
    print(f"  Speed Match: {'✅' if speed_match else '❌'}")

    if angle_match and size_match and speed_match:
        print(f"\n🎉 SUCCESS: Both dots generate identical momentum indicators!")
        print(
            f"The purple momentum triangle should now behave exactly like the red one."
        )
    else:
        print(f"\n❌ ISSUE: Momentum indicators don't match")

    # Test different speeds
    print(f"\n🏃 Testing Different Speed Ranges:")
    test_speeds = [0.5, 2.0, 10.0, 30.0, 60.0]  # From slow to max speed

    for speed in test_speeds:
        red_dot.velocity_x = speed
        red_dot.velocity_y = 0
        red_info = red_dot.get_momentum_info()

        if red_info:
            expected_size = min(
                MOMENTUM_MAX_SIZE,
                max(
                    MOMENTUM_MIN_SIZE,
                    MOMENTUM_MIN_SIZE
                    + (speed / MAX_SPEED) * (MOMENTUM_MAX_SIZE - MOMENTUM_MIN_SIZE),
                ),
            )
            print(
                f"  Speed {speed:4.1f}: Triangle size {red_info['size']:4.1f} (expected {expected_size:4.1f})"
            )
        else:
            print(f"  Speed {speed:4.1f}: No indicator (too slow)")


if __name__ == "__main__":
    test_momentum_indicators()
