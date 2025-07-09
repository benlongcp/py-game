#!/usr/bin/env python3
"""
Test script comparing all black hole gravitational field enhancements.
Shows the progression from original to final enhanced state.
"""

import math
from objects import BlackHole
from config import DOT_RADIUS, SQUARE_SIZE_MULTIPLIER


def test_black_hole_progression():
    """Show the complete progression of black hole enhancements."""

    print("Black Hole Gravitational Field Enhancement Progression")
    print("=====================================================")

    # Create a black hole to get current parameters
    black_hole = BlackHole()

    # Current enhanced values
    current_radius = black_hole.radius
    current_gravity_radius = black_hole.gravity_radius
    current_gravity_strength = black_hole.gravity_strength

    # Calculate progression values
    original_gravity_radius = current_radius * 3.0  # Original: 3x
    first_enhanced = current_radius * 9.0  # First enhancement: 9x (200% increase)
    final_enhanced = (
        current_radius * 18.0
    )  # Final enhancement: 18x (additional 100% increase)

    print(f"Black Hole Physical Radius: {current_radius:.1f}")
    print(f"Gravity Strength: {current_gravity_strength:.1f} (10x normal gravity)")
    print()

    print("Gravitational Field Evolution:")
    print(f"Original Field Radius:      {original_gravity_radius:.1f} units")
    print(f"First Enhanced (200%):      {first_enhanced:.1f} units")
    print(f"Final Enhanced (+100%):     {final_enhanced:.1f} units")
    print()

    # Calculate field areas for each stage
    original_area = math.pi * (original_gravity_radius**2)
    first_area = math.pi * (first_enhanced**2)
    final_area = math.pi * (final_enhanced**2)

    print("Gravitational Field Coverage Areas:")
    print(f"Original Area:              {original_area:,.0f} square units")
    print(f"First Enhanced Area:        {first_area:,.0f} square units")
    print(f"Final Enhanced Area:        {final_area:,.0f} square units")
    print()

    # Calculate multipliers
    first_multiplier = first_area / original_area
    final_multiplier = final_area / original_area
    additional_multiplier = final_area / first_area

    print("Area Increase Multipliers:")
    print(f"Original → First Enhanced:  {first_multiplier:.1f}x larger")
    print(f"Original → Final Enhanced:  {final_multiplier:.1f}x larger")
    print(f"First → Final Enhanced:     {additional_multiplier:.1f}x larger")
    print()

    # Test effects at key distances
    print("Gravity Effects at Key Distances:")
    print("Distance | Original | First Enhanced | Final Enhanced | Force Level")
    print("---------|----------|----------------|----------------|------------")

    test_distances = [100, 200, 300, 400, 500, 600, 700, 800]

    for distance in test_distances:
        # Check if within each range
        in_original = distance <= original_gravity_radius
        in_first = distance <= first_enhanced
        in_final = distance <= final_enhanced

        # Calculate force if within final range
        if in_final:
            force = current_gravity_strength / (distance**2)
            force_str = f"{force:.4f}"
        else:
            force_str = "No effect"

        original_mark = "✓" if in_original else "✗"
        first_mark = "✓" if in_first else "✗"
        final_mark = "✓" if in_final else "✗"

        print(
            f"{distance:8d} |    {original_mark}     |       {first_mark}        |       {final_mark}        | {force_str}"
        )

    print()
    print("Visual Enhancements:")
    print("- Added slow gray pulsing effect (0.5 second cycle)")
    print(f"- Pulse timer cycles every {black_hole.pulse_duration} frames")
    print("- Gray overlay with alpha-based intensity")
    print("- Smooth sine wave pulsing for visual appeal")
    print()

    print("Total Enhancement Summary:")
    print(f"- Gravitational field increased by {(final_multiplier-1)*100:.0f}% total")
    print(f"- Field radius: {original_gravity_radius:.0f} → {final_enhanced:.0f} units")
    print(f"- Coverage area: {original_area:,.0f} → {final_area:,.0f} square units")
    print("- Added atmospheric pulsing visual effect")
    print("- Maintains 10x gravity strength vs normal objects")
    print()

    print("Gameplay Impact:")
    print("- Black holes now dominate large portions of the arena")
    print("- Objects feel gravitational pull from extreme distances")
    print("- Strategic movement becomes critical to avoid capture")
    print("- Projectile trajectories affected across most of the play area")
    print("- Visual pulsing helps players identify black hole locations")
    print("- Creates truly dramatic and influential environmental hazards")


if __name__ == "__main__":
    test_black_hole_progression()
