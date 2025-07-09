#!/usr/bin/env python3
"""
Visual test script to demonstrate projectile gravity in a simplified environment.
This shows curved trajectories as projectiles are influenced by gravity wells.
"""

import math
import matplotlib.pyplot as plt
import numpy as np
from objects import (
    Projectile,
    RedGravitationalDot,
    PurpleGravitationalDot,
    CentralGravitationalDot,
)
from config import *


def plot_projectile_trajectories():
    """Plot projectile trajectories with and without gravity."""
    # Create gravitational dots
    red_gravity = RedGravitationalDot()
    purple_gravity = PurpleGravitationalDot()
    central_gravity = CentralGravitationalDot()

    # Test cases
    test_cases = [
        {
            "name": "Shot toward red goal",
            "start": (-500, -100),
            "velocity": (15, 2),
            "color": "red",
        },
        {
            "name": "Shot toward purple goal",
            "start": (500, 100),
            "velocity": (-15, -2),
            "color": "purple",
        },
        {
            "name": "Shot across center",
            "start": (-300, 200),
            "velocity": (12, -8),
            "color": "green",
        },
    ]

    plt.figure(figsize=(12, 8))

    for case in test_cases:
        # Trajectory with gravity
        projectile_gravity = Projectile(
            case["start"][0], case["start"][1], case["velocity"][0], case["velocity"][1]
        )

        # Trajectory without gravity (for comparison)
        projectile_no_gravity = Projectile(
            case["start"][0], case["start"][1], case["velocity"][0], case["velocity"][1]
        )

        gravity_x, gravity_y = [], []
        no_gravity_x, no_gravity_y = [], []

        # Simulate 50 steps
        for step in range(50):
            # With gravity
            gravity_x.append(projectile_gravity.x)
            gravity_y.append(projectile_gravity.y)

            # Apply gravity
            red_gravity.apply_gravity_to_object(projectile_gravity)
            purple_gravity.apply_gravity_to_object(projectile_gravity)
            central_gravity.apply_gravity_to_object(projectile_gravity)

            # Update position
            projectile_gravity.x += projectile_gravity.velocity_x
            projectile_gravity.y += projectile_gravity.velocity_y

            # Without gravity (straight line)
            no_gravity_x.append(projectile_no_gravity.x)
            no_gravity_y.append(projectile_no_gravity.y)

            projectile_no_gravity.x += projectile_no_gravity.velocity_x
            projectile_no_gravity.y += projectile_no_gravity.velocity_y

            # Stop if out of bounds
            if (
                abs(projectile_gravity.x) > 2000
                or abs(projectile_gravity.y) > 1500
                or abs(projectile_no_gravity.x) > 2000
                or abs(projectile_no_gravity.y) > 1500
            ):
                break

        # Plot trajectories
        plt.plot(
            gravity_x,
            gravity_y,
            "-",
            color=case["color"],
            linewidth=2,
            label=f'{case["name"]} (with gravity)',
        )
        plt.plot(
            no_gravity_x,
            no_gravity_y,
            "--",
            color=case["color"],
            linewidth=1,
            alpha=0.6,
            label=f'{case["name"]} (no gravity)',
        )

    # Plot gravity wells
    circle_red = plt.Circle(
        (red_gravity.x, red_gravity.y),
        red_gravity.radius,
        color="red",
        alpha=0.3,
        label="Red gravity well",
    )
    circle_purple = plt.Circle(
        (purple_gravity.x, purple_gravity.y),
        purple_gravity.radius,
        color="purple",
        alpha=0.3,
        label="Purple gravity well",
    )
    circle_central = plt.Circle(
        (central_gravity.x, central_gravity.y),
        central_gravity.radius,
        color="gray",
        alpha=0.3,
        label="Central gravity well",
    )

    plt.gca().add_patch(circle_red)
    plt.gca().add_patch(circle_purple)
    plt.gca().add_patch(circle_central)

    # Plot elliptical boundary
    ellipse = plt.matplotlib.patches.Ellipse(
        (0, 0),
        GRID_RADIUS_X * 2,
        GRID_RADIUS_Y * 2,
        fill=False,
        edgecolor="black",
        linewidth=2,
        label="Play area boundary",
    )
    plt.gca().add_patch(ellipse)

    plt.xlim(-1600, 1600)
    plt.ylim(-1000, 1000)
    plt.grid(True, alpha=0.3)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.title("Projectile Trajectories: With vs Without Gravity")
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.axis("equal")
    plt.tight_layout()

    # Save the plot
    plt.savefig("projectile_gravity_demo.png", dpi=150, bbox_inches="tight")
    print("Trajectory plot saved as 'projectile_gravity_demo.png'")
    print("\nKey observations:")
    print("- Solid lines show curved trajectories affected by gravity")
    print("- Dashed lines show straight trajectories without gravity")
    print("- Projectiles curve toward the nearest gravity wells")
    print("- The effect is strongest when projectiles pass close to gravity sources")


if __name__ == "__main__":
    try:
        plot_projectile_trajectories()
    except ImportError:
        print("Matplotlib not available. Skipping visual demonstration.")
        print("Install with: pip install matplotlib")
        print("\nProjectile gravity is still active in the game!")
