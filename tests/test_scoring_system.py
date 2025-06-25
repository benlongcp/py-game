#!/usr/bin/env python3
"""
Test script for the scoring system.
Tests that players can score points when the blue square overlaps static circles for 1.0 seconds.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from game_engine import GameEngine
from config import *
import math


class ScoringSystemTest:
    """Test the scoring system mechanics."""

    def __init__(self):
        self.game_engine = GameEngine()
        self.test_results = []

    def run_all_tests(self):
        """Run all scoring system tests."""
        print("=== Scoring System Tests ===\n")

        # Test 1: Blue square in red circle for 1.0 seconds
        self.test_red_circle_scoring()

        # Test 2: Blue square in purple circle for 1.0 seconds
        self.test_purple_circle_scoring()

        # Test 3: Blue square moves between circles (no scoring)
        self.test_no_scoring_when_moving()

        # Test 4: Respawn position after scoring
        self.test_respawn_position()

        # Print results
        self.print_results()

    def test_red_circle_scoring(self):
        """Test scoring when blue square is in red circle."""
        print("Test 1: Red circle scoring")

        # Reset game state
        self.game_engine.red_player_score = 0
        self.game_engine.purple_player_score = 0
        self.game_engine.red_circle_overlap_timer = 0
        self.game_engine.purple_circle_overlap_timer = 0

        # Position blue square inside red circle
        self.game_engine.blue_square.x = STATIC_RED_CIRCLE_X
        self.game_engine.blue_square.y = STATIC_RED_CIRCLE_Y
        self.game_engine.blue_square.velocity_x = 0
        self.game_engine.blue_square.velocity_y = 0

        initial_red_score = self.game_engine.red_player_score
        initial_purple_score = self.game_engine.purple_player_score

        # Simulate frames for just under 1.0 seconds (should not score)
        for frame in range(SCORE_OVERLAP_FRAMES - 1):
            self.game_engine._update_scoring()

        # Check no score yet
        if (
            self.game_engine.red_player_score == initial_red_score
            and self.game_engine.purple_player_score == initial_purple_score
        ):
            print("✓ No premature scoring before 1.0 seconds")
        else:
            print("✗ Premature scoring detected")
            self.test_results.append(False)
            return

        # Simulate one more frame (should trigger scoring)
        self.game_engine._update_scoring()

        # Check that red player scored
        if (
            self.game_engine.red_player_score == initial_red_score + 1
            and self.game_engine.purple_player_score == initial_purple_score
        ):
            print("✓ Red player scored after 1.0 seconds")
            self.test_results.append(True)
        else:
            print(
                f"✗ Expected red score {initial_red_score + 1}, got {self.game_engine.red_player_score}"
            )
            print(
                f"✗ Expected purple score {initial_purple_score}, got {self.game_engine.purple_player_score}"
            )
            self.test_results.append(False)

        print()

    def test_purple_circle_scoring(self):
        """Test scoring when blue square is in purple circle."""
        print("Test 2: Purple circle scoring")

        # Reset game state
        self.game_engine.red_player_score = 0
        self.game_engine.purple_player_score = 0
        self.game_engine.red_circle_overlap_timer = 0
        self.game_engine.purple_circle_overlap_timer = 0

        # Position blue square inside purple circle
        self.game_engine.blue_square.x = STATIC_PURPLE_CIRCLE_X
        self.game_engine.blue_square.y = STATIC_PURPLE_CIRCLE_Y
        self.game_engine.blue_square.velocity_x = 0
        self.game_engine.blue_square.velocity_y = 0

        initial_red_score = self.game_engine.red_player_score
        initial_purple_score = self.game_engine.purple_player_score

        # Simulate frames for exactly 1.0 seconds
        for frame in range(SCORE_OVERLAP_FRAMES):
            self.game_engine._update_scoring()

        # Check that purple player scored
        if (
            self.game_engine.purple_player_score == initial_purple_score + 1
            and self.game_engine.red_player_score == initial_red_score
        ):
            print("✓ Purple player scored after 1.0 seconds")
            self.test_results.append(True)
        else:
            print(
                f"✗ Expected purple score {initial_purple_score + 1}, got {self.game_engine.purple_player_score}"
            )
            print(
                f"✗ Expected red score {initial_red_score}, got {self.game_engine.red_player_score}"
            )
            self.test_results.append(False)

        print()

    def test_no_scoring_when_moving(self):
        """Test that no scoring occurs when blue square moves between circles."""
        print("Test 3: No scoring when moving between circles")

        # Reset game state
        self.game_engine.red_player_score = 0
        self.game_engine.purple_player_score = 0
        self.game_engine.red_circle_overlap_timer = 0
        self.game_engine.purple_circle_overlap_timer = 0

        initial_red_score = self.game_engine.red_player_score
        initial_purple_score = self.game_engine.purple_player_score

        # Move blue square between red and purple circles over time
        frames_to_simulate = SCORE_OVERLAP_FRAMES + 10
        for frame in range(frames_to_simulate):
            # Interpolate position between red and purple circles
            t = frame / frames_to_simulate
            self.game_engine.blue_square.x = (
                1 - t
            ) * STATIC_RED_CIRCLE_X + t * STATIC_PURPLE_CIRCLE_X
            self.game_engine.blue_square.y = (
                1 - t
            ) * STATIC_RED_CIRCLE_Y + t * STATIC_PURPLE_CIRCLE_Y
            self.game_engine._update_scoring()

        # Check that no scoring occurred
        if (
            self.game_engine.red_player_score == initial_red_score
            and self.game_engine.purple_player_score == initial_purple_score
        ):
            print("✓ No scoring when moving between circles")
            self.test_results.append(True)
        else:
            print(
                f"✗ Unexpected scoring: red {self.game_engine.red_player_score}, purple {self.game_engine.purple_player_score}"
            )
            self.test_results.append(False)

        print()

    def test_respawn_position(self):
        """Test that blue square respawns at grid center after scoring."""
        print("Test 4: Blue square respawn position")

        # Position blue square inside red circle
        self.game_engine.blue_square.x = STATIC_RED_CIRCLE_X
        self.game_engine.blue_square.y = STATIC_RED_CIRCLE_Y
        self.game_engine.blue_square.velocity_x = 10.0
        self.game_engine.blue_square.velocity_y = 15.0
        self.game_engine.blue_square.angular_velocity = 2.0

        # Trigger scoring
        self.game_engine.red_circle_overlap_timer = SCORE_OVERLAP_FRAMES
        self.game_engine._update_scoring()

        # Check respawn position and velocity reset
        if (
            abs(self.game_engine.blue_square.x - BLUE_SQUARE_RESPAWN_X) < 0.1
            and abs(self.game_engine.blue_square.y - BLUE_SQUARE_RESPAWN_Y) < 0.1
            and abs(self.game_engine.blue_square.velocity_x) < 0.1
            and abs(self.game_engine.blue_square.velocity_y) < 0.1
            and abs(self.game_engine.blue_square.angular_velocity) < 0.1
        ):
            print("✓ Blue square respawned at grid center with zero velocity")
            self.test_results.append(True)
        else:
            print(
                f"✗ Incorrect respawn: pos({self.game_engine.blue_square.x:.1f}, {self.game_engine.blue_square.y:.1f})"
            )
            print(f"✗ Expected pos({BLUE_SQUARE_RESPAWN_X}, {BLUE_SQUARE_RESPAWN_Y})")
            print(
                f"✗ Velocity: ({self.game_engine.blue_square.velocity_x:.1f}, {self.game_engine.blue_square.velocity_y:.1f})"
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
            print("🎉 All scoring system tests passed!")
        else:
            print("❌ Some scoring system tests failed.")

        print()
        print("Configuration:")
        print(
            f"- Score overlap time: {SCORE_OVERLAP_TIME} seconds ({SCORE_OVERLAP_FRAMES} frames)"
        )
        print(f"- Static circle radius: {STATIC_CIRCLE_RADIUS:.1f}")
        print(f"- Blue square size: {DOT_RADIUS * SQUARE_SIZE_MULTIPLIER}")
        print(f"- Respawn position: ({BLUE_SQUARE_RESPAWN_X}, {BLUE_SQUARE_RESPAWN_Y})")


def main():
    """Main function to run the scoring system tests."""
    app = QApplication(sys.argv)

    # Run tests
    test_runner = ScoringSystemTest()
    test_runner.run_all_tests()

    # No need to start event loop for these tests
    sys.exit(0)


if __name__ == "__main__":
    main()
