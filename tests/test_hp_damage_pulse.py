#!/usr/bin/env python3
"""
Test script to verify the HP damage pulse effect.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from game_engine import GameEngine
from config import *


def test_hp_damage_pulse():
    """Test that players pulse yellow when taking HP damage."""
    print("=== HP Damage Pulse Effect Test ===\n")

    game_engine = GameEngine()
    game_engine.create_purple_dot()

    # Test 1: Red player HP damage pulse
    print("Test 1: Red player takes damage")
    print(
        f"Before damage - Red HP: {game_engine.red_player_hp}, Pulsing: {game_engine.red_dot.is_pulsing()}"
    )

    # Simulate damage
    game_engine._damage_player("red", "test")

    print(
        f"After damage - Red HP: {game_engine.red_player_hp}, Pulsing: {game_engine.red_dot.is_pulsing()}"
    )

    if game_engine.red_dot.is_pulsing():
        print("✓ Red dot is pulsing yellow after HP damage")
    else:
        print("✗ Red dot is not pulsing after HP damage")

    # Test 2: Purple player HP damage pulse
    print("\nTest 2: Purple player takes damage")
    print(
        f"Before damage - Purple HP: {game_engine.purple_player_hp}, Pulsing: {game_engine.purple_dot.is_pulsing()}"
    )

    # Simulate damage
    game_engine._damage_player("purple", "test")

    print(
        f"After damage - Purple HP: {game_engine.purple_player_hp}, Pulsing: {game_engine.purple_dot.is_pulsing()}"
    )

    if game_engine.purple_dot.is_pulsing():
        print("✓ Purple dot is pulsing yellow after HP damage")
    else:
        print("✗ Purple dot is not pulsing after HP damage")

    # Test 3: Pulse timer countdown
    print("\nTest 3: Pulse timer countdown")
    initial_timer = game_engine.red_dot.pulse_timer
    print(f"Initial pulse timer: {initial_timer}")

    # Update physics to decrement timer
    game_engine.red_dot.update_physics()

    final_timer = game_engine.red_dot.pulse_timer
    print(f"Final pulse timer: {final_timer}")

    if final_timer == initial_timer - 1:
        print("✓ Pulse timer decrements correctly")
    else:
        print("✗ Pulse timer not working properly")

    # Test 4: Collision cooldown prevents multiple pulses
    print("\nTest 4: Collision cooldown prevents multiple damage")
    initial_hp = game_engine.red_player_hp
    initial_timer = game_engine.red_dot.pulse_timer

    # Try to damage again while on cooldown
    game_engine._damage_player("red", "test")

    final_hp = game_engine.red_player_hp
    final_timer = game_engine.red_dot.pulse_timer

    if initial_hp == final_hp and initial_timer == final_timer:
        print("✓ Cooldown prevents multiple damage and pulse effects")
    else:
        print("✗ Cooldown not working properly")

    print("\n=== HP Damage Pulse Test Complete ===")
    print("Configuration:")
    print(f"- Pulse duration: {SQUARE_PULSE_DURATION} frames")
    print(f"- Pulse color: {HP_DAMAGE_PULSE_COLOR} (Yellow)")
    print(f"- Collision cooldown: {game_engine.collision_cooldown_frames} frames")


def main():
    """Main function to run the HP damage pulse test."""
    app = QApplication(sys.argv)
    test_hp_damage_pulse()
    sys.exit(0)


if __name__ == "__main__":
    main()
