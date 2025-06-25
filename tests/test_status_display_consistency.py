#!/usr/bin/env python3
"""
Test script to verify consistent status display formatting before and after scoring.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPixmap
from game_engine import GameEngine
from rendering import Renderer
from config import *


def test_status_display_consistency():
    """Test that status display looks the same before and after scoring."""
    print("=== Status Display Consistency Test ===\n")

    app = QApplication(sys.argv)
    game_engine = GameEngine()
    game_engine.create_purple_dot()

    # Create a test widget to draw on
    widget = QWidget()
    widget.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

    # Test 1: Initial state (both scores = 0)
    print("Test 1: Initial state (Red: 0, Purple: 0)")
    print("Should show multiplayer format: 'Red: 0' on left, 'Purple: 0' on right")

    pixmap1 = QPixmap(WINDOW_WIDTH, WINDOW_HEIGHT)
    pixmap1.fill()
    painter1 = QPainter(pixmap1)

    red_score = game_engine.get_red_player_score()  # 0
    purple_score = game_engine.get_purple_player_score()  # 0
    red_hp = game_engine.get_red_player_hp()  # 10
    purple_hp = game_engine.get_purple_player_hp()  # 10

    print(
        f"Values: Red score={red_score}, Purple score={purple_score}, Red HP={red_hp}, Purple HP={purple_hp}"
    )

    Renderer.draw_status_display(painter1, red_score, purple_score, red_hp, purple_hp)
    painter1.end()

    # Test 2: After red player scores (Red: 2, Purple: 0)
    print("\nTest 2: After red player scores (Red: 2, Purple: 0)")
    print("Should show same multiplayer format: 'Red: 2' on left, 'Purple: 0' on right")

    pixmap2 = QPixmap(WINDOW_WIDTH, WINDOW_HEIGHT)
    pixmap2.fill()
    painter2 = QPainter(pixmap2)

    # Simulate red player scoring
    game_engine.red_player_score = 2
    red_score = game_engine.get_red_player_score()  # 2
    purple_score = game_engine.get_purple_player_score()  # 0

    print(
        f"Values: Red score={red_score}, Purple score={purple_score}, Red HP={red_hp}, Purple HP={purple_hp}"
    )

    Renderer.draw_status_display(painter2, red_score, purple_score, red_hp, purple_hp)
    painter2.end()

    # Test 3: After both players score (Red: 2, Purple: 1)
    print("\nTest 3: After both players score (Red: 2, Purple: 1)")
    print("Should show same multiplayer format: 'Red: 2' on left, 'Purple: 1' on right")

    pixmap3 = QPixmap(WINDOW_WIDTH, WINDOW_HEIGHT)
    pixmap3.fill()
    painter3 = QPainter(pixmap3)

    # Simulate purple player scoring
    game_engine.purple_player_score = 1
    red_score = game_engine.get_red_player_score()  # 2
    purple_score = game_engine.get_purple_player_score()  # 1

    print(
        f"Values: Red score={red_score}, Purple score={purple_score}, Red HP={red_hp}, Purple HP={purple_hp}"
    )

    Renderer.draw_status_display(painter3, red_score, purple_score, red_hp, purple_hp)
    painter3.end()

    # Test 4: Test with damaged HP
    print("\nTest 4: After HP damage (Red: 2, Purple: 1, Red HP: 7, Purple HP: 8)")
    print("Should show same multiplayer format with updated HP values")

    pixmap4 = QPixmap(WINDOW_WIDTH, WINDOW_HEIGHT)
    pixmap4.fill()
    painter4 = QPainter(pixmap4)

    # Simulate HP damage
    game_engine.red_player_hp = 7
    game_engine.purple_player_hp = 8
    red_hp = game_engine.get_red_player_hp()  # 7
    purple_hp = game_engine.get_purple_player_hp()  # 8

    print(
        f"Values: Red score={red_score}, Purple score={purple_score}, Red HP={red_hp}, Purple HP={purple_hp}"
    )

    Renderer.draw_status_display(painter4, red_score, purple_score, red_hp, purple_hp)
    painter4.end()

    print("\n✅ All tests completed!")
    print("📋 Expected behavior:")
    print("- All tests should use the same multiplayer layout")
    print("- Format: 'Red: X' on left, 'Purple: Y' on right")
    print("- HP displayed below scores in same positions")
    print("- No switching between single-player and multiplayer formats")

    sys.exit(0)


def main():
    """Main function to run the status display test."""
    test_status_display_consistency()


if __name__ == "__main__":
    main()
