#!/usr/bin/env python3
"""
Comprehensive test to demonstrate the teleportation fix.
This test shows before/after behavior and simulates real collision scenarios.
"""

import sys
import os
import math

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from physics import PhysicsEngine
from config import GRID_RADIUS_X, GRID_RADIUS_Y, DOT_RADIUS


def old_boundary_check(x, y, radius, radius_x, radius_y):
    """The OLD method that caused teleportation."""
    effective_radius_x = max(0, radius_x - radius)
    effective_radius_y = max(0, radius_y - radius)

    if effective_radius_x <= 0 or effective_radius_y <= 0:
        return True, 0, 0, 0, 0

    ellipse_val = (x / effective_radius_x) ** 2 + (y / effective_radius_y) ** 2

    if ellipse_val > 1.0:
        # OLD METHOD: Project by angle (causes teleportation)
        angle = math.atan2(y, x)
        boundary_x = effective_radius_x * math.cos(angle)
        boundary_y = effective_radius_y * math.sin(angle)

        normal_x = 2 * boundary_x / (effective_radius_x**2)
        normal_y = 2 * boundary_y / (effective_radius_y**2)
        norm = math.sqrt(normal_x**2 + normal_y**2)
        if norm > 0:
            normal_x /= norm
            normal_y /= norm
            normal_x = -normal_x
            normal_y = -normal_y
        else:
            normal_x, normal_y = 0, 0

        return True, boundary_x, boundary_y, normal_x, normal_y

    return False, x, y, 0, 0


def test_teleportation_fix():
    """Test that shows the teleportation fix in action."""
    print("TELEPORTATION FIX DEMONSTRATION")
    print("=" * 60)

    # Test cases that would show significant teleportation
    problem_cases = [
        (850, 400, "Near corner - diagonal approach"),
        (950, 200, "Right side - angled approach"),
        (600, 470, "Top side - steep angle"),
        (750, 450, "Corner area - worst case"),
    ]

    for x, y, description in problem_cases:
        print(f"\n{description}:")
        print(f"Object at position: ({x}, {y})")

        # OLD method
        old_outside, old_x, old_y, old_nx, old_ny = old_boundary_check(
            x, y, DOT_RADIUS, GRID_RADIUS_X, GRID_RADIUS_Y
        )

        # NEW method
        new_outside, new_x, new_y, new_nx, new_ny = (
            PhysicsEngine.check_elliptical_boundary(
                x, y, DOT_RADIUS, GRID_RADIUS_X, GRID_RADIUS_Y
            )
        )

        if old_outside and new_outside:
            # Calculate movement distance
            old_distance = math.sqrt((old_x - x) ** 2 + (old_y - y) ** 2)
            new_distance = math.sqrt((new_x - x) ** 2 + (new_y - y) ** 2)

            print(
                f"  OLD correction: ({old_x:.1f}, {old_y:.1f}) - moved {old_distance:.1f} units"
            )
            print(
                f"  NEW correction: ({new_x:.1f}, {new_y:.1f}) - moved {new_distance:.1f} units"
            )
            print(
                f"  Improvement: {old_distance - new_distance:.1f} units less movement"
            )

            # Show angle difference
            old_angle = math.degrees(math.atan2(old_y, old_x))
            new_angle = math.degrees(math.atan2(new_y, new_x))
            orig_angle = math.degrees(math.atan2(y, x))

            print(f"  Original angle: {orig_angle:.1f}°")
            print(
                f"  OLD angle: {old_angle:.1f}° (diff: {abs(old_angle - orig_angle):.1f}°)"
            )
            print(
                f"  NEW angle: {new_angle:.1f}° (diff: {abs(new_angle - orig_angle):.1f}°)"
            )


def simulate_realistic_collision():
    """Simulate a realistic collision scenario."""
    print("\n" + "=" * 60)
    print("REALISTIC COLLISION SIMULATION")
    print("Simulating a red dot moving diagonally toward the boundary...")

    # Start position and velocity
    x, y = 700, 300
    velocity_x, velocity_y = 15, 10  # Moving toward top-right

    print(f"Initial: pos=({x}, {y}), vel=({velocity_x}, {velocity_y})")

    for step in range(8):
        # Update position
        new_x = x + velocity_x
        new_y = y + velocity_y

        # Check boundary with NEW method
        is_outside, corrected_x, corrected_y, normal_x, normal_y = (
            PhysicsEngine.check_elliptical_boundary(
                new_x, new_y, DOT_RADIUS, GRID_RADIUS_X, GRID_RADIUS_Y
            )
        )

        if is_outside:
            # Apply correction and bounce
            x = corrected_x
            y = corrected_y

            # Calculate bounce
            dot_product = velocity_x * normal_x + velocity_y * normal_y
            velocity_x -= 2 * dot_product * normal_x * 0.8  # bounce factor
            velocity_y -= 2 * dot_product * normal_y * 0.8

            movement = math.sqrt(
                (corrected_x - (new_x - velocity_x)) ** 2
                + (corrected_y - (new_y - velocity_y)) ** 2
            )

            print(
                f"Step {step + 1}: BOUNCE - pos=({x:.1f}, {y:.1f}), new_vel=({velocity_x:.1f}, {velocity_y:.1f})"
            )
            print(f"           Correction movement: {movement:.1f} units")
        else:
            x = new_x
            y = new_y
            print(f"Step {step + 1}: Normal - pos=({x:.1f}, {y:.1f})")

        # Stop if velocity is too low
        speed = math.sqrt(velocity_x**2 + velocity_y**2)
        if speed < 1:
            print(f"Step {step + 1}: Stopped (low velocity)")
            break


if __name__ == "__main__":
    test_teleportation_fix()
    simulate_realistic_collision()
    print(f"\nTest completed! The new method should show much smaller corrections.")
