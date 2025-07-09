#!/usr/bin/env python3
"""
Test script to verify that black holes spawn on the edge of the elliptical boundary.
Creates multiple black holes and checks their distance from the ellipse center.
"""

import math
from objects import BlackHole
from config import GRID_RADIUS_X, GRID_RADIUS_Y


def test_black_hole_edge_spawning():
    """Test that black holes spawn near the edge of the elliptical boundary."""
    print("Black Hole Edge Spawning Test")
    print("=" * 40)
    print(f"Arena dimensions: {GRID_RADIUS_X} x {GRID_RADIUS_Y}")
    print(f"Expected edge factor: 95% of boundary")
    print()

    # Create multiple black holes to test positioning
    num_tests = 10
    positions = []

    for i in range(num_tests):
        black_hole = BlackHole()
        x, y = black_hole.x, black_hole.y
        positions.append((x, y))

        # Calculate distance from center as a proportion of the ellipse
        # For ellipse: (x/a)² + (y/b)² = 1 when on the boundary
        ellipse_value = (x / GRID_RADIUS_X) ** 2 + (y / GRID_RADIUS_Y) ** 2
        distance_from_center = math.sqrt(x**2 + y**2)

        print(f"Black Hole {i+1:2d}:")
        print(f"  Position: ({x:7.2f}, {y:7.2f})")
        print(f"  Distance from center: {distance_from_center:7.2f}")
        print(f"  Ellipse equation value: {ellipse_value:.3f} (1.0 = on boundary)")
        print(f"  Edge percentage: {ellipse_value * 100:.1f}%")

        # Check if it's close to the expected 95% edge factor
        expected_ellipse_value = 0.95**2  # Since we use 95% edge factor
        if abs(ellipse_value - expected_ellipse_value) < 0.01:
            print(f"  ✓ Correctly positioned near edge")
        else:
            print(
                f"  ⚠ Position may be incorrect (expected ~{expected_ellipse_value:.3f})"
            )
        print()

    # Calculate statistics
    ellipse_values = [
        (pos[0] / GRID_RADIUS_X) ** 2 + (pos[1] / GRID_RADIUS_Y) ** 2
        for pos in positions
    ]
    avg_ellipse_value = sum(ellipse_values) / len(ellipse_values)
    min_ellipse_value = min(ellipse_values)
    max_ellipse_value = max(ellipse_values)

    print("Statistics:")
    print(f"  Average ellipse value: {avg_ellipse_value:.3f}")
    print(f"  Min ellipse value: {min_ellipse_value:.3f}")
    print(f"  Max ellipse value: {max_ellipse_value:.3f}")
    print(f"  Expected value: {0.95**2:.3f} (95% of boundary)")
    print()

    # Verify they're all close to the edge (within reasonable tolerance)
    edge_spawns = sum(1 for val in ellipse_values if 0.85 < val < 1.0)
    print(f"Black holes spawned near edge (85-100%): {edge_spawns}/{num_tests}")

    if edge_spawns == num_tests:
        print("✅ SUCCESS: All black holes spawned near the edge!")
    else:
        print("❌ ISSUE: Some black holes did not spawn near the edge")

    print()
    print("Visual Reference:")
    print("- Ellipse value of 1.0 = exactly on boundary")
    print("- Ellipse value of 0.95² ≈ 0.903 = 95% to boundary (expected)")
    print("- Ellipse value of 0.5 = halfway to boundary")
    print("- Ellipse value of 0.0 = at center")


if __name__ == "__main__":
    test_black_hole_edge_spawning()
