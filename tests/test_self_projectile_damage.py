#!/usr/bin/env python3
"""
Test script to verify that players don't lose HP when firing their own projectiles.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from game_engine import GameEngine
from config import *


def test_self_projectile_damage():
    """Test that players don't damage themselves with their own projectiles."""
    print("=== Self-Projectile Damage Test ===\n")

    game_engine = GameEngine()
    game_engine.create_purple_dot()

    # Test 1: Red player fires projectile
    print("Test 1: Red player fires projectile")
    game_engine.red_player_hp = 10
    game_engine.red_dot_collision_cooldown = 0

    # Give red dot some velocity so it can fire
    game_engine.red_dot.velocity_x = 5.0
    game_engine.red_dot.velocity_y = 0.0

    initial_hp = game_engine.red_player_hp
    print(f"Initial red HP: {initial_hp}")

    # Fire projectile
    game_engine.shoot_projectile_player1()
    print(f"Projectiles created: {len(game_engine.projectiles)}")

    if game_engine.projectiles:
        projectile = game_engine.projectiles[0]
        print(f"Projectile owner: {projectile.owner_id}")
        print(f"Projectile position: ({projectile.x:.1f}, {projectile.y:.1f})")
        print(
            f"Red dot position: ({game_engine.red_dot.virtual_x:.1f}, {game_engine.red_dot.virtual_y:.1f})"
        )

    # Check for collisions immediately
    game_engine._handle_collisions()

    final_hp = game_engine.red_player_hp
    print(f"Final red HP: {final_hp}")

    if final_hp == initial_hp:
        print("✓ Red player did NOT lose HP from own projectile\n")
    else:
        print("✗ Red player lost HP from own projectile (BUG!)\n")

    # Test 2: Purple player fires projectile
    print("Test 2: Purple player fires projectile")
    game_engine.purple_player_hp = 10
    game_engine.purple_dot_collision_cooldown = 0
    game_engine.projectiles = []  # Clear previous projectiles

    # Give purple dot some velocity so it can fire
    game_engine.purple_dot.velocity_x = -5.0
    game_engine.purple_dot.velocity_y = 0.0

    initial_hp = game_engine.purple_player_hp
    print(f"Initial purple HP: {initial_hp}")

    # Fire projectile
    game_engine.shoot_projectile_player2()
    print(f"Projectiles created: {len(game_engine.projectiles)}")

    if game_engine.projectiles:
        projectile = game_engine.projectiles[0]
        print(f"Projectile owner: {projectile.owner_id}")
        print(f"Projectile position: ({projectile.x:.1f}, {projectile.y:.1f})")
        print(
            f"Purple dot position: ({game_engine.purple_dot.virtual_x:.1f}, {game_engine.purple_dot.virtual_y:.1f})"
        )

    # Check for collisions immediately
    game_engine._handle_collisions()

    final_hp = game_engine.purple_player_hp
    print(f"Final purple HP: {final_hp}")

    if final_hp == initial_hp:
        print("✓ Purple player did NOT lose HP from own projectile\n")
    else:
        print("✗ Purple player lost HP from own projectile (BUG!)\n")

    # Test 3: Cross-fire test - red projectile hits purple player
    print("Test 3: Red projectile hits purple player")
    game_engine.red_player_hp = 10
    game_engine.purple_player_hp = 10
    game_engine.red_dot_collision_cooldown = 0
    game_engine.purple_dot_collision_cooldown = 0
    game_engine.projectiles = []  # Clear projectiles

    # Position players apart
    game_engine.red_dot.virtual_x = 100
    game_engine.red_dot.virtual_y = 100
    game_engine.purple_dot.virtual_x = 200
    game_engine.purple_dot.virtual_y = 100

    # Give red dot velocity and fire
    game_engine.red_dot.velocity_x = 5.0
    game_engine.red_dot.velocity_y = 0.0
    game_engine.shoot_projectile_player1()

    if game_engine.projectiles:
        # Move the projectile to purple player's position
        projectile = game_engine.projectiles[0]
        projectile.x = game_engine.purple_dot.virtual_x
        projectile.y = game_engine.purple_dot.virtual_y

        print(f"Projectile owner: {projectile.owner_id}")
        print(f"Red HP before: {game_engine.red_player_hp}")
        print(f"Purple HP before: {game_engine.purple_player_hp}")

        # Check for collisions
        game_engine._handle_collisions()

        print(f"Red HP after: {game_engine.red_player_hp}")
        print(f"Purple HP after: {game_engine.purple_player_hp}")

        if game_engine.red_player_hp == 10 and game_engine.purple_player_hp == 9:
            print("✓ Only purple player took damage from red's projectile\n")
        else:
            print("✗ Unexpected damage distribution in cross-fire test\n")

    print("🎯 Test completed!")


def main():
    """Main function to run the self-projectile damage test."""
    app = QApplication(sys.argv)
    test_self_projectile_damage()
    sys.exit(0)


if __name__ == "__main__":
    main()
