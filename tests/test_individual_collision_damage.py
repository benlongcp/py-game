#!/usr/bin/env python3
"""
Test script to specifically verify that only the colliding player loses HP.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from game_engine import GameEngine
from config import *


def test_individual_collision_damage():
    """Test that only the colliding player takes damage."""
    print("=== Individual Collision Damage Test ===\n")

    game_engine = GameEngine()
    game_engine.create_purple_dot()

    # Test 1: Only red player collides with blue square
    print("Test 1: Red player collides with blue square")
    game_engine.red_player_hp = 10
    game_engine.purple_player_hp = 10
    game_engine.red_dot_collision_cooldown = 0
    game_engine.purple_dot_collision_cooldown = 0

    # Position red dot away from purple dot
    game_engine.red_dot.virtual_x = 100
    game_engine.red_dot.virtual_y = 100
    game_engine.purple_dot.virtual_x = 500
    game_engine.purple_dot.virtual_y = 500

    # Position blue square to only collide with red dot
    game_engine.blue_square.x = 100
    game_engine.blue_square.y = 100

    print(
        f"Before collision - Red HP: {game_engine.red_player_hp}, Purple HP: {game_engine.purple_player_hp}"
    )

    # Trigger collision detection
    game_engine._handle_collisions()

    print(
        f"After collision - Red HP: {game_engine.red_player_hp}, Purple HP: {game_engine.purple_player_hp}"
    )

    if game_engine.red_player_hp == 9 and game_engine.purple_player_hp == 10:
        print("✓ Only red player took damage from blue square collision\n")
    else:
        print("✗ Unexpected damage distribution\n")

    # Test 2: Only purple player collides with blue square
    print("Test 2: Purple player collides with blue square")
    game_engine.red_player_hp = 10
    game_engine.purple_player_hp = 10
    game_engine.red_dot_collision_cooldown = 0
    game_engine.purple_dot_collision_cooldown = 0

    # Position purple dot away from red dot
    game_engine.red_dot.virtual_x = 100
    game_engine.red_dot.virtual_y = 100
    game_engine.purple_dot.virtual_x = 500
    game_engine.purple_dot.virtual_y = 500

    # Position blue square to only collide with purple dot
    game_engine.blue_square.x = 500
    game_engine.blue_square.y = 500

    print(
        f"Before collision - Red HP: {game_engine.red_player_hp}, Purple HP: {game_engine.purple_player_hp}"
    )

    # Trigger collision detection
    game_engine._handle_collisions()

    print(
        f"After collision - Red HP: {game_engine.red_player_hp}, Purple HP: {game_engine.purple_player_hp}"
    )

    if game_engine.red_player_hp == 10 and game_engine.purple_player_hp == 9:
        print("✓ Only purple player took damage from blue square collision\n")
    else:
        print("✗ Unexpected damage distribution\n")

    # Test 3: Test projectile damage isolation
    print("Test 3: Red player projectile hits purple player only")
    game_engine.red_player_hp = 10
    game_engine.purple_player_hp = 10
    game_engine.red_dot_collision_cooldown = 0
    game_engine.purple_dot_collision_cooldown = 0
    game_engine.projectiles = []  # Clear projectiles

    # Give red dot velocity to create projectile
    game_engine.red_dot.velocity_x = 5.0
    game_engine.red_dot.velocity_y = 0.0

    # Position dots apart
    game_engine.red_dot.virtual_x = 100
    game_engine.red_dot.virtual_y = 100
    game_engine.purple_dot.virtual_x = 200
    game_engine.purple_dot.virtual_y = 100

    # Create projectile from red player
    game_engine.shoot_projectile_player1()

    if game_engine.projectiles:
        projectile = game_engine.projectiles[0]
        # Position projectile to hit purple dot only
        projectile.x = 200
        projectile.y = 100

        print(
            f"Before projectile hit - Red HP: {game_engine.red_player_hp}, Purple HP: {game_engine.purple_player_hp}"
        )

        # Trigger collision detection
        game_engine._handle_collisions()

        print(
            f"After projectile hit - Red HP: {game_engine.red_player_hp}, Purple HP: {game_engine.purple_player_hp}"
        )

        if game_engine.red_player_hp == 10 and game_engine.purple_player_hp == 9:
            print("✓ Only purple player took damage from projectile\n")
        else:
            print("✗ Unexpected damage distribution from projectile\n")
    else:
        print("✗ No projectile created\n")

    # Test 4: Boundary collision isolation
    print("Test 4: Only red player hits boundary")
    game_engine.red_player_hp = 10
    game_engine.purple_player_hp = 10
    game_engine.red_dot_collision_cooldown = 0
    game_engine.purple_dot_collision_cooldown = 0

    # Position red dot at boundary, purple dot safe
    game_engine.red_dot.virtual_x = GRID_RADIUS - game_engine.red_dot.radius + 1
    game_engine.red_dot.virtual_y = 0
    game_engine.purple_dot.virtual_x = 0
    game_engine.purple_dot.virtual_y = 0

    print(
        f"Before boundary check - Red HP: {game_engine.red_player_hp}, Purple HP: {game_engine.purple_player_hp}"
    )

    # Trigger boundary check
    game_engine._update_hit_points()

    print(
        f"After boundary check - Red HP: {game_engine.red_player_hp}, Purple HP: {game_engine.purple_player_hp}"
    )

    if game_engine.red_player_hp == 9 and game_engine.purple_player_hp == 10:
        print("✓ Only red player took damage from boundary collision\n")
    else:
        print("✗ Unexpected damage distribution from boundary\n")


def main():
    """Main function to run the individual collision tests."""
    app = QApplication(sys.argv)
    test_individual_collision_damage()
    sys.exit(0)


if __name__ == "__main__":
    main()
