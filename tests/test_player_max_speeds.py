#!/usr/bin/env python3
"""
Test script to verify that both players have the same maximum speed.
"""

import sys
import os
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from game_engine import GameEngine
from config import *


def test_player_max_speeds():
    """Test that both players have the same maximum speed."""
    print("=== Player Maximum Speed Test ===\n")

    game_engine = GameEngine()
    game_engine.create_purple_dot()

    print(f"Configured MAX_SPEED: {MAX_SPEED}")
    print(f"Configured ACCELERATION: {ACCELERATION}")
    print(f"Configured DECELERATION: {DECELERATION}\n")

    # Reset positions to true center to avoid boundary collisions
    game_engine.red_dot.virtual_x = 0
    game_engine.red_dot.virtual_y = 0
    game_engine.purple_dot.virtual_x = 0
    game_engine.purple_dot.virtual_y = 0

    # Test 1: Red player maximum speed
    print("Test 1: Red player maximum speed")

    # Reset velocities
    game_engine.red_dot.velocity_x = 0
    game_engine.red_dot.velocity_y = 0

    # Apply maximum acceleration for many frames to reach max speed
    game_engine.red_dot.acceleration_x = ACCELERATION
    game_engine.red_dot.acceleration_y = 0

    # Track speed over time to see equilibrium
    for frame in range(100):  # Shorter duration to avoid boundary hits
        old_speed = math.sqrt(
            game_engine.red_dot.velocity_x**2 + game_engine.red_dot.velocity_y**2
        )

        # IMPORTANT: Reset acceleration to 0 first (like game engine does each frame)
        game_engine.red_dot.acceleration_x = 0
        game_engine.red_dot.acceleration_y = 0

        # Then apply intended acceleration (simulating key press)
        game_engine.red_dot.acceleration_x = ACCELERATION

        # Debug: print acceleration before physics update
        if frame < 10 or frame % 20 == 0:
            distance = math.sqrt(
                game_engine.red_dot.virtual_x**2 + game_engine.red_dot.virtual_y**2
            )
            print(
                f"  Frame {frame}: Speed before = {old_speed:.6f}, Distance = {distance:.1f}"
            )

        game_engine.red_dot.update_physics()
        new_speed = math.sqrt(
            game_engine.red_dot.velocity_x**2 + game_engine.red_dot.velocity_y**2
        )

        # Print progress every 20 frames
        if frame % 20 == 0:
            distance = math.sqrt(
                game_engine.red_dot.virtual_x**2 + game_engine.red_dot.virtual_y**2
            )
            print(
                f"  Frame {frame}: Speed after = {new_speed:.6f}, Distance = {distance:.1f}"
            )

        # Check if we've reached equilibrium (speed not changing much)
        if frame > 50 and abs(new_speed - old_speed) < 0.001:
            print(f"  Equilibrium reached at frame {frame}")
            print(
                f"  Final velocity: ({game_engine.red_dot.velocity_x:.6f}, {game_engine.red_dot.velocity_y:.6f})"
            )
            print(f"  Final speed: {new_speed:.6f}")
            break

    # If we didn't break out, we didn't reach equilibrium
    if frame == 99:
        print("  No equilibrium reached in 100 frames")
        print(
            f"  Final velocity: ({game_engine.red_dot.velocity_x:.6f}, {game_engine.red_dot.velocity_y:.6f})"
        )
        print(f"  Final speed: {new_speed:.6f}")

    red_speed = math.sqrt(
        game_engine.red_dot.velocity_x**2 + game_engine.red_dot.velocity_y**2
    )

    print(f"Red player final speed: {red_speed:.6f}")
    print(
        f"Red player velocity: ({game_engine.red_dot.velocity_x:.6f}, {game_engine.red_dot.velocity_y:.6f})"
    )

    # Test 2: Purple player maximum speed
    print("\nTest 2: Purple player maximum speed")

    # Reset velocities
    game_engine.purple_dot.velocity_x = 0
    game_engine.purple_dot.velocity_y = 0

    # Apply maximum acceleration for many frames to reach max speed
    game_engine.purple_dot.acceleration_x = ACCELERATION
    game_engine.purple_dot.acceleration_y = 0

    for frame in range(100):  # Run for many more frames
        old_speed = math.sqrt(
            game_engine.purple_dot.velocity_x**2 + game_engine.purple_dot.velocity_y**2
        )

        # IMPORTANT: Reset acceleration to 0 first (like game engine does each frame)
        game_engine.purple_dot.acceleration_x = 0
        game_engine.purple_dot.acceleration_y = 0

        # Then apply intended acceleration (simulating key press)
        game_engine.purple_dot.acceleration_x = ACCELERATION

        game_engine.purple_dot.update_physics()
        new_speed = math.sqrt(
            game_engine.purple_dot.velocity_x**2 + game_engine.purple_dot.velocity_y**2
        )

        # Print progress every 20 frames
        if frame % 20 == 0:
            distance = math.sqrt(
                game_engine.purple_dot.virtual_x**2
                + game_engine.purple_dot.virtual_y**2
            )
            print(
                f"  Frame {frame}: Speed = {new_speed:.6f}, Distance = {distance:.1f}"
            )

        # Check if we've reached equilibrium
        if frame > 50 and abs(new_speed - old_speed) < 0.001:
            print(f"  Equilibrium reached at frame {frame}")
            break

    purple_speed = math.sqrt(
        game_engine.purple_dot.velocity_x**2 + game_engine.purple_dot.velocity_y**2
    )

    print(f"Purple player final speed: {purple_speed:.6f}")
    print(
        f"Purple player velocity: ({game_engine.purple_dot.velocity_x:.6f}, {game_engine.purple_dot.velocity_y:.6f})"
    )

    # Test 3: Comparison
    print("\nTest 3: Speed comparison")
    speed_difference = abs(red_speed - purple_speed)
    print(f"Speed difference: {speed_difference:.6f}")

    if speed_difference < 0.001:  # Allow for tiny floating point differences
        print("✓ Both players have the same maximum speed")
    else:
        print("✗ Players have different maximum speeds")

    # Test 4: Check equilibrium vs MAX_SPEED
    print(f"\nTest 4: Physics analysis")
    # At equilibrium: v = (v + a) * d
    # Solving: v = v*d + a*d, so v*(1-d) = a*d, thus v = a*d/(1-d)
    expected_equilibrium = (ACCELERATION * DECELERATION) / (1 - DECELERATION)
    print(f"Expected equilibrium speed: {expected_equilibrium:.2f}")
    print(f"Configured MAX_SPEED: {MAX_SPEED}")

    if expected_equilibrium < MAX_SPEED:
        print("ℹ️  Physics equilibrium is reached before MAX_SPEED limit")
        print("   This means MAX_SPEED is not the limiting factor")
    else:
        print("ℹ️  MAX_SPEED should be the limiting factor")

    # Test 5: Force high speed to test MAX_SPEED clamping
    print(f"\nTest 5: Force high speed to test MAX_SPEED clamping")

    # Manually set high velocity to test clamping
    game_engine.red_dot.velocity_x = MAX_SPEED * 2  # Set to double MAX_SPEED
    game_engine.red_dot.velocity_y = 0
    game_engine.red_dot.acceleration_x = 0  # No acceleration
    game_engine.red_dot.acceleration_y = 0

    print(
        f"Before physics: {math.sqrt(game_engine.red_dot.velocity_x**2 + game_engine.red_dot.velocity_y**2):.2f}"
    )
    game_engine.red_dot.update_physics()
    final_speed = math.sqrt(
        game_engine.red_dot.velocity_x**2 + game_engine.red_dot.velocity_y**2
    )
    print(f"After physics: {final_speed:.2f}")

    if abs(final_speed - MAX_SPEED) < 0.001:
        print("✓ MAX_SPEED clamping works correctly")
    else:
        print("✗ MAX_SPEED clamping not working")

    print(f"\n🎯 Summary:")
    print(f"- Both players use the same physics constants")
    print(f"- Equilibrium speed: {expected_equilibrium:.2f}")
    print(f"- MAX_SPEED limit: {MAX_SPEED}")
    print(f"- Speed difference: {speed_difference:.6f}")

    return speed_difference < 0.001  # Return whether players have same speed


def main():
    """Main function to run the max speed test."""
    app = QApplication(sys.argv)
    test_player_max_speeds()
    sys.exit(0)


if __name__ == "__main__":
    main()
