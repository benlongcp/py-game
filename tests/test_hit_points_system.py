#!/usr/bin/env python3
"""
Test script for the hit points system.
Tests damage from collisions, boundary hits, and HP depletion scoring.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from game_engine import GameEngine
from config import *
import math


class HitPointsSystemTest:
    """Test the hit points system mechanics."""

    def __init__(self):
        self.game_engine = GameEngine()
        self.game_engine.create_purple_dot()
        self.test_results = []

    def run_all_tests(self):
        """Run all hit points system tests."""
        print("=== Hit Points System Tests ===\n")

        # Test 1: Initial HP values
        self.test_initial_hp()

        # Test 2: Blue square collision damage
        self.test_blue_square_damage()

        # Test 3: Projectile collision damage
        self.test_projectile_damage()

        # Test 4: Player vs player collision damage
        self.test_player_collision_damage()

        # Test 5: Boundary collision damage
        self.test_boundary_damage()

        # Test 6: HP depletion scoring
        self.test_hp_depletion_scoring()

        # Test 7: Static circle scoring (2 points)
        self.test_static_circle_scoring()

        # Print results
        self.print_results()

    def test_initial_hp(self):
        """Test that players start with correct HP."""
        print("Test 1: Initial hit points")

        if (
            self.game_engine.get_red_player_hp() == INITIAL_HIT_POINTS
            and self.game_engine.get_purple_player_hp() == INITIAL_HIT_POINTS
        ):
            print(f"✓ Both players start with {INITIAL_HIT_POINTS} HP")
            self.test_results.append(True)
        else:
            print(
                f"✗ Incorrect initial HP: Red {self.game_engine.get_red_player_hp()}, Purple {self.game_engine.get_purple_player_hp()}"
            )
            self.test_results.append(False)
        print()

    def test_blue_square_damage(self):
        """Test damage from blue square collision."""
        print("Test 2: Blue square collision damage")

        # Reset HP
        self.game_engine.red_player_hp = INITIAL_HIT_POINTS
        self.game_engine.red_dot_collision_cooldown = 0

        initial_hp = self.game_engine.get_red_player_hp()

        # Position blue square to collide with red dot
        self.game_engine.blue_square.x = self.game_engine.red_dot.virtual_x
        self.game_engine.blue_square.y = self.game_engine.red_dot.virtual_y

        # Trigger collision detection
        self.game_engine._handle_collisions()

        final_hp = self.game_engine.get_red_player_hp()

        if final_hp == initial_hp - HIT_POINT_DAMAGE:
            print(f"✓ Blue square collision deals {HIT_POINT_DAMAGE} damage")
            self.test_results.append(True)
        else:
            print(f"✗ Expected {initial_hp - HIT_POINT_DAMAGE} HP, got {final_hp}")
            self.test_results.append(False)
        print()

    def test_projectile_damage(self):
        """Test damage from projectile collision."""
        print("Test 3: Projectile collision damage")

        # Reset HP and cooldown
        self.game_engine.red_player_hp = INITIAL_HIT_POINTS
        self.game_engine.red_dot_collision_cooldown = 0

        initial_hp = self.game_engine.get_red_player_hp()

        # Give purple dot some velocity for projectile creation
        self.game_engine.purple_dot.velocity_x = 5.0
        self.game_engine.purple_dot.velocity_y = 0.0

        # Create a projectile near the red dot
        self.game_engine.shoot_projectile_player2()  # Purple shoots projectile
        if self.game_engine.projectiles:
            projectile = self.game_engine.projectiles[0]
            # Position projectile to hit red dot
            projectile.x = self.game_engine.red_dot.virtual_x
            projectile.y = self.game_engine.red_dot.virtual_y

            # Trigger collision detection
            self.game_engine._handle_collisions()

            final_hp = self.game_engine.get_red_player_hp()

            if final_hp == initial_hp - HIT_POINT_DAMAGE:
                print(f"✓ Projectile collision deals {HIT_POINT_DAMAGE} damage")
                self.test_results.append(True)
            else:
                print(f"✗ Expected {initial_hp - HIT_POINT_DAMAGE} HP, got {final_hp}")
                self.test_results.append(False)
        else:
            print("✗ No projectile created")
            self.test_results.append(False)
        print()

    def test_player_collision_damage(self):
        """Test damage from player vs player collision."""
        print("Test 4: Player vs player collision damage")

        # Reset HP
        self.game_engine.red_player_hp = INITIAL_HIT_POINTS
        self.game_engine.purple_player_hp = INITIAL_HIT_POINTS
        self.game_engine.red_dot_collision_cooldown = 0
        self.game_engine.purple_dot_collision_cooldown = 0

        initial_red_hp = self.game_engine.get_red_player_hp()
        initial_purple_hp = self.game_engine.get_purple_player_hp()

        # Position players to collide
        self.game_engine.purple_dot.virtual_x = self.game_engine.red_dot.virtual_x
        self.game_engine.purple_dot.virtual_y = self.game_engine.red_dot.virtual_y

        # Trigger collision detection
        self.game_engine._handle_collisions()

        final_red_hp = self.game_engine.get_red_player_hp()
        final_purple_hp = self.game_engine.get_purple_player_hp()

        if (
            final_red_hp == initial_red_hp - HIT_POINT_DAMAGE
            and final_purple_hp == initial_purple_hp - HIT_POINT_DAMAGE
        ):
            print(f"✓ Player collision deals {HIT_POINT_DAMAGE} damage to both players")
            self.test_results.append(True)
        else:
            print(f"✗ Expected both to lose {HIT_POINT_DAMAGE} HP")
            print(
                f"✗ Red: {initial_red_hp} → {final_red_hp}, Purple: {initial_purple_hp} → {final_purple_hp}"
            )
            self.test_results.append(False)
        print()

    def test_boundary_damage(self):
        """Test damage from boundary collision."""
        print("Test 5: Boundary collision damage")

        # Reset HP
        self.game_engine.red_player_hp = INITIAL_HIT_POINTS
        self.game_engine.red_dot_collision_cooldown = 0

        initial_hp = self.game_engine.get_red_player_hp()

        # Position red dot at boundary
        self.game_engine.red_dot.virtual_x = (
            GRID_RADIUS - self.game_engine.red_dot.radius + 1
        )
        self.game_engine.red_dot.virtual_y = 0

        # Trigger boundary check
        self.game_engine._update_hit_points()

        final_hp = self.game_engine.get_red_player_hp()

        if final_hp == initial_hp - HIT_POINT_DAMAGE:
            print(f"✓ Boundary collision deals {HIT_POINT_DAMAGE} damage")
            self.test_results.append(True)
        else:
            print(f"✗ Expected {initial_hp - HIT_POINT_DAMAGE} HP, got {final_hp}")
            self.test_results.append(False)
        print()

    def test_hp_depletion_scoring(self):
        """Test scoring when HP reaches 0."""
        print("Test 6: HP depletion scoring")

        # Reset scores
        self.game_engine.red_player_score = 0
        self.game_engine.purple_player_score = 0

        # Set red player to 1 HP
        self.game_engine.red_player_hp = 1
        self.game_engine.red_dot_collision_cooldown = 0

        initial_purple_score = self.game_engine.get_purple_player_score()

        # Trigger damage to deplete HP
        self.game_engine._damage_player("red", "test")
        self.game_engine._update_hit_points()

        final_purple_score = self.game_engine.get_purple_player_score()
        final_red_hp = self.game_engine.get_red_player_hp()

        if (
            final_purple_score == initial_purple_score + 1
            and final_red_hp == INITIAL_HIT_POINTS
        ):  # HP should be reset
            print("✓ HP depletion awards 1 point and resets HP")
            self.test_results.append(True)
        else:
            print(f"✗ Expected purple score +1 and red HP reset")
            print(f"✗ Purple score: {initial_purple_score} → {final_purple_score}")
            print(f"✗ Red HP: 0 → {final_red_hp}")
            self.test_results.append(False)
        print()

    def test_static_circle_scoring(self):
        """Test 2-point scoring from static circles."""
        print("Test 7: Static circle scoring (2 points)")

        # Reset game state
        self.game_engine.red_player_score = 0
        self.game_engine.red_circle_overlap_timer = 0
        self.game_engine.purple_circle_overlap_timer = 0

        # Position blue square inside red static circle
        self.game_engine.blue_square.x = STATIC_RED_CIRCLE_X
        self.game_engine.blue_square.y = STATIC_RED_CIRCLE_Y
        self.game_engine.blue_square.velocity_x = 0
        self.game_engine.blue_square.velocity_y = 0

        initial_score = self.game_engine.get_red_player_score()

        # Simulate the required overlap time
        for frame in range(SCORE_OVERLAP_FRAMES):
            self.game_engine._update_scoring()

        final_score = self.game_engine.get_red_player_score()

        if final_score == initial_score + STATIC_CIRCLE_SCORE_POINTS:
            print(f"✓ Static circle scoring awards {STATIC_CIRCLE_SCORE_POINTS} points")
            self.test_results.append(True)
        else:
            print(
                f"✗ Expected {initial_score + STATIC_CIRCLE_SCORE_POINTS} points, got {final_score}"
            )
            print(
                f"✗ Overlap timer reached: {self.game_engine.red_circle_overlap_timer}"
            )
            self.test_results.append(False)
        print()

    def print_results(self):
        """Print test results summary."""
        passed = sum(self.test_results)
        total = len(self.test_results)

        print("=== Test Results ===")
        print(f"Passed: {passed}/{total}")

        if passed == total:
            print("🎉 All hit points system tests passed!")
        else:
            print("❌ Some hit points system tests failed.")

        print()
        print("Configuration:")
        print(f"- Initial hit points: {INITIAL_HIT_POINTS}")
        print(f"- Damage per hit: {HIT_POINT_DAMAGE}")
        print(f"- Static circle points: {STATIC_CIRCLE_SCORE_POINTS}")
        print(f"- HP depletion points: 1")


def main():
    """Main function to run the hit points system tests."""
    app = QApplication(sys.argv)

    # Run tests
    test_runner = HitPointsSystemTest()
    test_runner.run_all_tests()

    # No need to start event loop for these tests
    sys.exit(0)


if __name__ == "__main__":
    main()
