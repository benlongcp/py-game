#!/usr/bin/env python3
"""
Test script comparing the original vs enhanced black hole gravitational field.
Shows the difference in gravitational range and effect area.
"""

import math
from objects import BlackHole
from config import DOT_RADIUS, SQUARE_SIZE_MULTIPLIER


def test_black_hole_field_comparison():
    """Compare original vs enhanced black hole gravitational fields."""

    print("Black Hole Gravitational Field Comparison")
    print("=========================================")

    # Create a black hole to get current parameters
    black_hole = BlackHole()

    # Current enhanced values
    current_radius = black_hole.radius
    current_gravity_radius = black_hole.gravity_radius
    current_gravity_strength = black_hole.gravity_strength

    # Calculate what the original values would have been
    original_gravity_radius = current_radius * 3.0  # Original was 3x
    enhanced_gravity_radius = current_radius * 9.0  # Enhanced is 9x

    print(f"Black Hole Physical Radius: {current_radius:.1f}")
    print(f"Original Gravity Field Radius: {original_gravity_radius:.1f}")
    print(f"Enhanced Gravity Field Radius: {enhanced_gravity_radius:.1f}")
    print(f"Gravity Strength: {current_gravity_strength:.1f}")
    print()

    # Calculate field areas
    original_area = math.pi * (original_gravity_radius**2)
    enhanced_area = math.pi * (enhanced_gravity_radius**2)
    area_increase = enhanced_area / original_area

    print("Gravitational Field Coverage:")
    print(f"Original Field Area: {original_area:,.0f} square units")
    print(f"Enhanced Field Area: {enhanced_area:,.0f} square units")
    print(
        f"Area Increase: {area_increase:.1f}x larger ({(area_increase-1)*100:.0f}% increase)"
    )
    print()

    # Test gravity effects at various distances
    print("Gravity Force at Different Distances:")
    print("Distance | Original Range | Enhanced Range | Force")
    print("---------|----------------|----------------|-------")

    test_distances = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]

    for distance in test_distances:
        # Calculate if within range
        in_original_range = distance <= original_gravity_radius
        in_enhanced_range = distance <= enhanced_gravity_radius

        # Calculate gravity force (using inverse square law)
        if in_enhanced_range:
            force = current_gravity_strength / (distance**2)
        else:
            force = 0.0

        original_status = "✓" if in_original_range else "✗"
        enhanced_status = "✓" if in_enhanced_range else "✗"
        force_str = f"{force:.4f}" if force > 0 else "No effect"

        print(
            f"{distance:8d} |      {original_status}         |        {enhanced_status}       | {force_str}"
        )

    print()
    print("Impact on Gameplay:")
    print("- Objects are now affected from much greater distances")
    print("- Projectiles will curve toward black holes from farther away")
    print("- Players will feel the pull sooner when approaching")
    print("- Blue cube will be influenced across more of the arena")
    print("- Creates more dramatic and noticeable gravitational effects")
    print()
    print("The 200% increase in field size creates 9x larger coverage area!")


if __name__ == "__main__":
    test_black_hole_field_comparison()
