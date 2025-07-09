#!/usr/bin/env python3
"""
Test script to demonstrate the new BlackHole object and its gravitational effects.
This shows how the black hole moves around and affects other objects.
"""

import math
from objects import BlackHole, Projectile, BlueSquare, RedDot
from config import *


def test_black_hole_creation():
    """Test black hole creation and basic properties."""
    print("Testing Black Hole Creation")
    print("===========================")

    # Create multiple black holes to see randomness
    for i in range(5):
        hole = BlackHole()
        print(f"Black Hole {i+1}:")
        print(f"  Position: ({hole.x:.1f}, {hole.y:.1f})")
        print(f"  Velocity: ({hole.velocity_x:.2f}, {hole.velocity_y:.2f})")
        print(f"  Radius: {hole.radius:.1f}")
        print(f"  Gravity Strength: {hole.gravity_strength}")
        print(f"  Gravity Range: {hole.max_gravity_distance:.1f}")
        print()


def test_black_hole_movement():
    """Test black hole movement and boundary bouncing."""
    print("Testing Black Hole Movement")
    print("===========================")

    hole = BlackHole()
    print(f"Initial position: ({hole.x:.1f}, {hole.y:.1f})")
    print(f"Initial velocity: ({hole.velocity_x:.2f}, {hole.velocity_y:.2f})")
    print()

    # Simulate movement for several frames
    for frame in range(0, 100, 10):
        hole.update_physics()
        speed = math.sqrt(hole.velocity_x**2 + hole.velocity_y**2)
        print(
            f"Frame {frame:2d}: pos=({hole.x:6.1f}, {hole.y:6.1f}) "
            f"vel=({hole.velocity_x:5.2f}, {hole.velocity_y:5.2f}) "
            f"speed={speed:5.2f}"
        )
    print()


def test_black_hole_gravity_strength():
    """Test black hole gravity effects on different objects."""
    print("Testing Black Hole Gravity Effects")
    print("==================================")

    hole = BlackHole()
    hole.x = 0.0  # Place at center for easy testing
    hole.y = 0.0

    print(f"Black Hole at center with gravity strength: {hole.gravity_strength}")
    print(f"Gravity range: {hole.max_gravity_distance:.1f}")
    print()

    # Test different objects at different distances
    test_objects = [
        ("Projectile", Projectile(100, 0, 0, 0)),
        ("Blue Square", BlueSquare(200, 0)),
        ("Red Player", RedDot(300, 0)),
    ]

    distances = [50, 100, 200, 400]

    for obj_name, obj in test_objects:
        print(f"{obj_name} gravity effects:")

        for distance in distances:
            # Position object at specified distance
            if hasattr(obj, "x"):
                obj.x = distance
                obj.y = 0
            else:  # RedDot uses virtual_x/virtual_y
                obj.virtual_x = distance
                obj.virtual_y = 0

            # Reset velocity
            obj.velocity_x = 0.0
            obj.velocity_y = 0.0

            # Apply gravity
            was_affected = hole.apply_gravity_to_object(obj)

            if was_affected:
                force_magnitude = math.sqrt(obj.velocity_x**2 + obj.velocity_y**2)
                print(f"  Distance {distance:3d}: Force = {force_magnitude:.4f}")
            else:
                print(f"  Distance {distance:3d}: No effect (outside range)")

        print()


def test_black_hole_vs_normal_gravity():
    """Compare black hole gravity to normal gravitational dots."""
    print("Comparing Black Hole vs Normal Gravity")
    print("======================================")

    # Black hole gravity
    hole = BlackHole()
    hole.x = 0.0
    hole.y = 0.0

    # Normal gravity (like goal circles)
    from objects import RedGravitationalDot

    normal_gravity = RedGravitationalDot()
    normal_gravity.x = 0.0
    normal_gravity.y = 0.0

    # Test projectile
    projectile = Projectile(100, 0, 0, 0)

    print(f"Black Hole gravity strength: {hole.gravity_strength}")
    print(f"Normal gravity strength: {normal_gravity.strength}")
    print(
        f"Black Hole is {hole.gravity_strength / normal_gravity.strength:.1f}x stronger"
    )
    print()

    # Test at same distance
    distance = 100

    # Test black hole
    projectile.velocity_x = 0.0
    projectile.velocity_y = 0.0
    hole_affected = hole.apply_gravity_to_object(projectile)
    hole_force = math.sqrt(projectile.velocity_x**2 + projectile.velocity_y**2)

    # Test normal gravity
    projectile.velocity_x = 0.0
    projectile.velocity_y = 0.0
    normal_affected = normal_gravity.apply_gravity_to_object(projectile)
    normal_force = math.sqrt(projectile.velocity_x**2 + projectile.velocity_y**2)

    print(f"At distance {distance}:")
    print(f"  Black Hole force: {hole_force:.4f}")
    print(f"  Normal gravity force: {normal_force:.4f}")

    if hole_force > 0 and normal_force > 0:
        print(
            f"  Black Hole is {hole_force / normal_force:.1f}x stronger at this distance"
        )
    print()


def test_black_hole_trajectory_effects():
    """Test how black hole affects projectile trajectories."""
    print("Testing Black Hole Trajectory Effects")
    print("=====================================")

    hole = BlackHole()
    hole.x = 0.0
    hole.y = 0.0

    # Projectile passing by black hole
    projectile = Projectile(-200, 50, 10, 0)  # Moving horizontally past hole

    print("Projectile trajectory near black hole:")
    print(f"Black Hole at: ({hole.x}, {hole.y})")
    print(
        f"Initial projectile: pos=({projectile.x}, {projectile.y}) vel=({projectile.velocity_x}, {projectile.velocity_y})"
    )
    print()

    for step in range(0, 50, 5):
        # Apply black hole gravity
        hole.apply_gravity_to_object(projectile)

        # Update position
        projectile.x += projectile.velocity_x
        projectile.y += projectile.velocity_y

        # Calculate distance and speed
        distance = math.sqrt(projectile.x**2 + projectile.y**2)
        speed = math.sqrt(projectile.velocity_x**2 + projectile.velocity_y**2)

        print(
            f"Step {step:2d}: pos=({projectile.x:6.1f}, {projectile.y:6.1f}) "
            f"vel=({projectile.velocity_x:5.2f}, {projectile.velocity_y:5.2f}) "
            f"dist={distance:5.1f} speed={speed:5.2f}"
        )
    print()


if __name__ == "__main__":
    test_black_hole_creation()
    test_black_hole_movement()
    test_black_hole_gravity_strength()
    test_black_hole_vs_normal_gravity()
    test_black_hole_trajectory_effects()

    print("Black Hole Tests Completed!")
    print("\nIn-game effects:")
    print("- A black hole will spawn randomly in the play area")
    print("- It moves slowly in random directions, bouncing off boundaries")
    print("- It emits 10x stronger gravity than goal circles")
    print("- All objects (players, projectiles, blue cube) are pulled toward it")
    print("- Creates dynamic and unpredictable gameplay scenarios")
    print("- The black hole's gravity field extends 3x its radius")
    print("- Visual: Black center with dark gradient fading to transparent")
