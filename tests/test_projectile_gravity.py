#!/usr/bin/env python3
"""
Test script to demonstrate projectile gravity effects.
This test shows how projectiles now curve toward gravitational fields.
"""

import math
from objects import (
    Projectile,
    RedGravitationalDot,
    PurpleGravitationalDot,
    CentralGravitationalDot,
)
from config import *


def test_projectile_gravity():
    """Test that projectiles are affected by gravitational fields."""
    print("Testing Projectile Gravity Effects")
    print("==================================")

    # Create gravitational dots
    red_gravity = RedGravitationalDot()
    purple_gravity = PurpleGravitationalDot()
    central_gravity = CentralGravitationalDot()

    print(f"Red gravity dot at: ({red_gravity.x}, {red_gravity.y})")
    print(f"Purple gravity dot at: ({purple_gravity.x}, {purple_gravity.y})")
    print(f"Central gravity dot at: ({central_gravity.x}, {central_gravity.y})")
    print(f"Gravity strength: {red_gravity.strength}")
    print()

    # Test scenarios
    test_cases = [
        {
            "name": "Projectile fired horizontally near red gravity",
            "pos": (red_gravity.x - 200, red_gravity.y),
            "vel": (10.0, 0.0),
            "steps": 20,
        },
        {
            "name": "Projectile fired horizontally near purple gravity",
            "pos": (purple_gravity.x + 200, purple_gravity.y),
            "vel": (-10.0, 0.0),
            "steps": 20,
        },
        {
            "name": "Projectile fired vertically near center",
            "pos": (0, -200),
            "vel": (0.0, 8.0),
            "steps": 25,
        },
    ]

    for case in test_cases:
        print(f"Test: {case['name']}")
        print("-" * len(case["name"]))

        # Create projectile
        projectile = Projectile(
            case["pos"][0], case["pos"][1], case["vel"][0], case["vel"][1]
        )

        print(f"Initial position: ({projectile.x:.1f}, {projectile.y:.1f})")
        print(
            f"Initial velocity: ({projectile.velocity_x:.1f}, {projectile.velocity_y:.1f})"
        )

        # Simulate gravity effects for several steps
        for step in range(case["steps"]):
            # Apply gravity from all sources (like in game)
            red_gravity.apply_gravity_to_object(projectile)
            purple_gravity.apply_gravity_to_object(projectile)
            central_gravity.apply_gravity_to_object(projectile)

            # Update position (simplified - no boundary checks)
            projectile.x += projectile.velocity_x
            projectile.y += projectile.velocity_y

            # Show every 5th step
            if step % 5 == 0:
                speed = math.sqrt(projectile.velocity_x**2 + projectile.velocity_y**2)
                print(
                    f"  Step {step:2d}: pos=({projectile.x:6.1f}, {projectile.y:6.1f}) "
                    f"vel=({projectile.velocity_x:5.2f}, {projectile.velocity_y:5.2f}) "
                    f"speed={speed:5.2f}"
                )

        print()


def test_gravity_strength():
    """Test gravity effects at different distances."""
    print("Testing Gravity Strength at Different Distances")
    print("===============================================")

    red_gravity = RedGravitationalDot()

    # Test projectiles at different distances from red gravity
    distances = [50, 100, 200, 400, 800]

    for distance in distances:
        # Create projectile at specified distance
        projectile = Projectile(
            red_gravity.x + distance,
            red_gravity.y,
            0.0,
            0.0,  # Stationary to see pure gravity effect
        )

        initial_vel = (projectile.velocity_x, projectile.velocity_y)

        # Apply gravity once
        was_affected = red_gravity.apply_gravity_to_object(projectile)

        if was_affected:
            vel_change_x = projectile.velocity_x - initial_vel[0]
            vel_change_y = projectile.velocity_y - initial_vel[1]
            force_magnitude = math.sqrt(vel_change_x**2 + vel_change_y**2)

            print(f"Distance {distance:3d}: Force magnitude = {force_magnitude:.4f}")
        else:
            print(f"Distance {distance:3d}: No gravity effect (outside range)")

    print()


if __name__ == "__main__":
    test_projectile_gravity()
    test_gravity_strength()
    print("Projectile gravity tests completed!")
    print("\nIn-game effects:")
    print("- Projectiles will now curve toward the goal circles")
    print("- Shots near the center will be pulled slightly toward center")
    print("- Strategic positioning near gravity wells becomes more important")
    print("- Projectile trajectories are now more dynamic and unpredictable")
