#!/usr/bin/env python3
"""
Test script to verify that players start in their opponent's goal circles.
"""

import sys
import os
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from game_engine import GameEngine
from config import *


def test_player_starting_positions():
    """Test that players start in their opponent's goal circles."""
    print("🎯 Testing Player Starting Positions...")

    # Create game engine
    game_engine = GameEngine()
    game_engine.create_purple_dot()  # Ensure purple dot exists

    print(f"📍 Static Circle Positions:")
    print(
        f"   Red circle (red player's goal): ({STATIC_RED_CIRCLE_X}, {STATIC_RED_CIRCLE_Y})"
    )
    print(
        f"   Purple circle (purple player's goal): ({STATIC_PURPLE_CIRCLE_X}, {STATIC_PURPLE_CIRCLE_Y})"
    )

    print(f"\n🔴 Red Player Starting Position:")
    print(
        f"   Position: ({game_engine.red_dot.virtual_x}, {game_engine.red_dot.virtual_y})"
    )
    print(f"   Expected: ({RED_PLAYER_INITIAL_X}, {RED_PLAYER_INITIAL_Y})")
    print(f"   Should be in: Purple circle goal")

    # Check if red player is in purple circle
    red_dist_to_purple = math.sqrt(
        (game_engine.red_dot.virtual_x - STATIC_PURPLE_CIRCLE_X) ** 2
        + (game_engine.red_dot.virtual_y - STATIC_PURPLE_CIRCLE_Y) ** 2
    )
    print(f"   Distance to purple circle center: {red_dist_to_purple:.1f}")
    print(f"   Purple circle radius: {STATIC_CIRCLE_RADIUS:.1f}")

    if red_dist_to_purple <= STATIC_CIRCLE_RADIUS:
        print("   ✅ Red player starts inside purple circle goal")
    else:
        print("   ❌ Red player is NOT inside purple circle goal")

    print(f"\n🟣 Purple Player Starting Position:")
    print(
        f"   Position: ({game_engine.purple_dot.virtual_x}, {game_engine.purple_dot.virtual_y})"
    )
    print(f"   Expected: ({PURPLE_PLAYER_INITIAL_X}, {PURPLE_PLAYER_INITIAL_Y})")
    print(f"   Should be in: Red circle goal")

    # Check if purple player is in red circle
    purple_dist_to_red = math.sqrt(
        (game_engine.purple_dot.virtual_x - STATIC_RED_CIRCLE_X) ** 2
        + (game_engine.purple_dot.virtual_y - STATIC_RED_CIRCLE_Y) ** 2
    )
    print(f"   Distance to red circle center: {purple_dist_to_red:.1f}")
    print(f"   Red circle radius: {STATIC_CIRCLE_RADIUS:.1f}")

    if purple_dist_to_red <= STATIC_CIRCLE_RADIUS:
        print("   ✅ Purple player starts inside red circle goal")
    else:
        print("   ❌ Purple player is NOT inside red circle goal")

    print(f"\n🔵 Blue Square Starting Position:")
    print(f"   Position: ({game_engine.blue_square.x}, {game_engine.blue_square.y})")
    print(f"   Expected: ({INITIAL_SQUARE_X}, {INITIAL_SQUARE_Y})")
    print(f"   Should be at: Center of grid (central gravity point)")

    # Check if blue square is at center
    blue_dist_to_center = math.sqrt(
        game_engine.blue_square.x**2 + game_engine.blue_square.y**2
    )
    print(f"   Distance to center: {blue_dist_to_center:.1f}")

    if blue_dist_to_center < 1.0:  # Very close to center
        print("   ✅ Blue square starts at center")
    else:
        print("   ❌ Blue square is NOT at center")

    print(f"\n📏 Player Separation:")
    player_separation = math.sqrt(
        (game_engine.red_dot.virtual_x - game_engine.purple_dot.virtual_x) ** 2
        + (game_engine.red_dot.virtual_y - game_engine.purple_dot.virtual_y) ** 2
    )
    print(f"   Distance between players: {player_separation:.1f}")
    print(
        f"   Expected separation: {abs(STATIC_PURPLE_CIRCLE_X - STATIC_RED_CIRCLE_X):.1f}"
    )

    if abs(player_separation - abs(STATIC_PURPLE_CIRCLE_X - STATIC_RED_CIRCLE_X)) < 1.0:
        print("   ✅ Players are properly separated")
    else:
        print("   ❌ Player separation is incorrect")

    print(f"\n🎮 Strategic Analysis:")
    print("   - Each player starts in their opponent's goal")
    print("   - This creates immediate scoring opportunities")
    print("   - Players must either score quickly or move to defend their own goal")
    print("   - Blue square at center provides balanced access")
    print("   - Central gravity will pull blue square toward both players")

    print(f"\n🎉 Player starting position test completed!")


def main():
    """Main function to run the starting position test."""
    app = QApplication(sys.argv)
    test_player_starting_positions()
    sys.exit(0)


if __name__ == "__main__":
    main()
