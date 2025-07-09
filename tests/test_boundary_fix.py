#!/usr/bin/env python3
"""
Test script to verify elliptical boundary collision fixes.
This script creates objects at the boundary and tests their collision behavior.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from physics import PhysicsEngine
from config import GRID_RADIUS_X, GRID_RADIUS_Y, PROJECTILE_RADIUS, DOT_RADIUS


def test_elliptical_boundary():
    """Test the elliptical boundary collision detection."""
    print("Testing elliptical boundary collision detection...")
    print(f"Ellipse dimensions: {GRID_RADIUS_X} x {GRID_RADIUS_Y}")

    # Test cases: positions near the boundary
    test_cases = [
        # (x, y, radius, description)
        (GRID_RADIUS_X - 5, 0, DOT_RADIUS, "Red dot near right edge"),
        (0, GRID_RADIUS_Y - 5, DOT_RADIUS, "Red dot near top edge"),
        (GRID_RADIUS_X + 5, 0, DOT_RADIUS, "Red dot outside right edge"),
        (0, GRID_RADIUS_Y + 5, DOT_RADIUS, "Red dot outside top edge"),
        (GRID_RADIUS_X - 1, 0, PROJECTILE_RADIUS, "Projectile near right edge"),
        (GRID_RADIUS_X + 1, 0, PROJECTILE_RADIUS, "Projectile outside right edge"),
        # Corner tests
        (GRID_RADIUS_X * 0.7, GRID_RADIUS_Y * 0.7, DOT_RADIUS, "Red dot near corner"),
        (
            GRID_RADIUS_X * 0.9,
            GRID_RADIUS_Y * 0.9,
            DOT_RADIUS,
            "Red dot outside corner",
        ),
    ]

    for x, y, radius, desc in test_cases:
        is_outside, corrected_x, corrected_y, normal_x, normal_y = (
            PhysicsEngine.check_elliptical_boundary(
                x, y, radius, GRID_RADIUS_X, GRID_RADIUS_Y
            )
        )

        print(f"\n{desc}:")
        print(f"  Position: ({x:.1f}, {y:.1f}), Radius: {radius}")
        print(f"  Outside boundary: {is_outside}")
        if is_outside:
            print(f"  Corrected position: ({corrected_x:.1f}, {corrected_y:.1f})")
            print(f"  Normal vector: ({normal_x:.3f}, {normal_y:.3f})")

            # Verify the corrected position is actually safe
            effective_radius_x = max(0, GRID_RADIUS_X - radius)
            effective_radius_y = max(0, GRID_RADIUS_Y - radius)
            ellipse_val = (corrected_x / effective_radius_x) ** 2 + (
                corrected_y / effective_radius_y
            ) ** 2
            print(
                f"  Ellipse value at corrected position: {ellipse_val:.3f} (should be ≤ 1.0)"
            )

            if ellipse_val > 1.001:  # Small tolerance for floating point
                print(f"  WARNING: Corrected position is still outside boundary!")
        else:
            print(f"  Position is safe within boundary")


def test_bounce_simulation():
    """Simulate a bounce to ensure objects don't teleport."""
    print("\n" + "=" * 60)
    print("Testing bounce simulation...")

    # Simulate a red dot moving towards the right boundary
    x, y = GRID_RADIUS_X - 20, 0  # Start near right edge
    velocity_x, velocity_y = 10, 0  # Moving right
    radius = DOT_RADIUS

    print(f"Initial position: ({x:.1f}, {y:.1f})")
    print(f"Initial velocity: ({velocity_x:.1f}, {velocity_y:.1f})")

    for step in range(5):
        # Update position
        new_x = x + velocity_x
        new_y = y + velocity_y

        # Check boundary
        is_outside, corrected_x, corrected_y, normal_x, normal_y = (
            PhysicsEngine.check_elliptical_boundary(
                new_x, new_y, radius, GRID_RADIUS_X, GRID_RADIUS_Y
            )
        )

        if is_outside:
            # Apply correction and bounce
            x = corrected_x
            y = corrected_y

            # Bounce calculation
            dot_product = velocity_x * normal_x + velocity_y * normal_y
            velocity_x -= 2 * dot_product * normal_x * 0.8  # 0.8 is BOUNCE_FACTOR
            velocity_y -= 2 * dot_product * normal_y * 0.8

            print(f"Step {step + 1}: BOUNCED at ({x:.1f}, {y:.1f})")
            print(f"  New velocity: ({velocity_x:.1f}, {velocity_y:.1f})")
        else:
            x = new_x
            y = new_y
            print(f"Step {step + 1}: Normal move to ({x:.1f}, {y:.1f})")


if __name__ == "__main__":
    test_elliptical_boundary()
    test_bounce_simulation()
    print("\nBoundary collision test completed!")
