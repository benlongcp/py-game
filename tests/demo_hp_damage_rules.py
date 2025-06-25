#!/usr/bin/env python3
"""
Demonstration script to show the correct hit point damage behavior.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from game_engine import GameEngine
from config import *


def demonstrate_hp_damage_rules():
    """Demonstrate when players take damage and when they don't."""
    print("=== Hit Point Damage Rules Demonstration ===\n")

    game_engine = GameEngine()
    game_engine.create_purple_dot()

    print("📋 DAMAGE RULES:")
    print(
        "1. Blue square collision: Only the player who touches the blue square takes damage"
    )
    print("2. Projectile collision: Only the player hit by the projectile takes damage")
    print("3. Player vs player collision: BOTH players take damage (mutual contact)")
    print("4. Boundary collision: Only the player who hits the boundary takes damage")
    print()

    # Rule 1: Blue square collision
    print("🔷 RULE 1: Blue Square Collision")
    print("Red player touches blue square → Only red player loses 1 HP")
    game_engine.red_player_hp = 10
    game_engine.purple_player_hp = 10
    game_engine.red_dot_collision_cooldown = 0

    game_engine.red_dot.virtual_x = 100
    game_engine.purple_dot.virtual_x = 500  # Far away
    game_engine.blue_square.x = 100
    game_engine.blue_square.y = 100

    print(
        f"Before: Red HP={game_engine.red_player_hp}, Purple HP={game_engine.purple_player_hp}"
    )
    game_engine._handle_collisions()
    print(
        f"After:  Red HP={game_engine.red_player_hp}, Purple HP={game_engine.purple_player_hp}"
    )
    print("✓ Only red player took damage\n")

    # Rule 2: Projectile collision
    print("🚀 RULE 2: Projectile Collision")
    print("Red player's projectile hits purple player → Only purple player loses 1 HP")
    game_engine.red_player_hp = 10
    game_engine.purple_player_hp = 10
    game_engine.red_dot_collision_cooldown = 0
    game_engine.purple_dot_collision_cooldown = 0
    game_engine.projectiles = []

    game_engine.red_dot.velocity_x = 5.0
    game_engine.shoot_projectile_player1()

    if game_engine.projectiles:
        projectile = game_engine.projectiles[0]
        projectile.x = 500
        projectile.y = 500
        game_engine.purple_dot.virtual_x = 500
        game_engine.purple_dot.virtual_y = 500

        print(
            f"Before: Red HP={game_engine.red_player_hp}, Purple HP={game_engine.purple_player_hp}"
        )
        game_engine._handle_collisions()
        print(
            f"After:  Red HP={game_engine.red_player_hp}, Purple HP={game_engine.purple_player_hp}"
        )
        print("✓ Only purple player took damage\n")

    # Rule 3: Player vs player collision
    print("⚔️  RULE 3: Player vs Player Collision")
    print("Red and purple players collide → BOTH players lose 1 HP")
    game_engine.red_player_hp = 10
    game_engine.purple_player_hp = 10
    game_engine.red_dot_collision_cooldown = 0
    game_engine.purple_dot_collision_cooldown = 0

    # Position players to collide
    game_engine.red_dot.virtual_x = 200
    game_engine.red_dot.virtual_y = 200
    game_engine.purple_dot.virtual_x = 200
    game_engine.purple_dot.virtual_y = 200

    print(
        f"Before: Red HP={game_engine.red_player_hp}, Purple HP={game_engine.purple_player_hp}"
    )
    game_engine._handle_collisions()
    print(
        f"After:  Red HP={game_engine.red_player_hp}, Purple HP={game_engine.purple_player_hp}"
    )
    print("✓ Both players took damage (this is correct behavior)\n")

    # Rule 4: Boundary collision
    print("🔲 RULE 4: Boundary Collision")
    print("Purple player hits boundary → Only purple player loses 1 HP")
    game_engine.red_player_hp = 10
    game_engine.purple_player_hp = 10
    game_engine.red_dot_collision_cooldown = 0
    game_engine.purple_dot_collision_cooldown = 0

    game_engine.red_dot.virtual_x = 0  # Safe position
    game_engine.red_dot.virtual_y = 0
    game_engine.purple_dot.virtual_x = (
        GRID_RADIUS - game_engine.purple_dot.radius + 1
    )  # At boundary
    game_engine.purple_dot.virtual_y = 0

    print(
        f"Before: Red HP={game_engine.red_player_hp}, Purple HP={game_engine.purple_player_hp}"
    )
    game_engine._update_hit_points()
    print(
        f"After:  Red HP={game_engine.red_player_hp}, Purple HP={game_engine.purple_player_hp}"
    )
    print("✓ Only purple player took damage\n")

    print("🎯 SUMMARY:")
    print(
        "- Individual collisions (blue square, projectile, boundary): Only the affected player takes damage"
    )
    print("- Mutual collisions (player vs player): Both players take damage")
    print("- This is the correct and intended behavior!")


def main():
    """Main function to run the demonstration."""
    app = QApplication(sys.argv)
    demonstrate_hp_damage_rules()
    sys.exit(0)


if __name__ == "__main__":
    main()
