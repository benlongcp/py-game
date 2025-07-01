#!/usr/bin/env python3
"""
Debug script to investigate the Player 1 acceleration issue with dual gamepads.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from game_engine import GameEngine
from split_screen import SplitScreenView
from config import *


def debug_dual_in_game():
    """Test Player 1 acceleration issue in game context."""
    app = QApplication(sys.argv)

    # Create game engine and split screen
    game_engine = GameEngine()
    game_engine.create_purple_dot()
    split_screen = SplitScreenView(game_engine)

    frame_count = 0

    def debug_frame():
        nonlocal frame_count
        frame_count += 1

        gamepad_manager = split_screen.gamepad_manager
        # Don't call update() here - let the game engine handle it

        print(f"\n=== Frame {frame_count} ===")
        print(f"Total gamepads: {gamepad_manager.gamepad_count}")
        print(f"GAMEPAD_1_INDEX = {GAMEPAD_1_INDEX}")
        print(f"GAMEPAD_2_INDEX = {GAMEPAD_2_INDEX}")

        # Check all connected gamepads
        for i in range(gamepad_manager.gamepad_count):
            if gamepad_manager.is_gamepad_connected(i):
                input_data = gamepad_manager.get_gamepad_input(i)
                print(
                    f"Gamepad {i}: X={input_data['left_stick_x']:.3f}, Y={input_data['left_stick_y']:.3f}, Shoot={input_data['shoot_button']}"
                )

        # Check Player 1 configuration
        p1_gamepad_connected = gamepad_manager.is_gamepad_connected(GAMEPAD_1_INDEX)
        print(
            f"Player 1 gamepad (index {GAMEPAD_1_INDEX}) connected: {p1_gamepad_connected}"
        )

        if p1_gamepad_connected:
            p1_input = gamepad_manager.get_gamepad_input(GAMEPAD_1_INDEX)
            print(
                f"Player 1 input: X={p1_input['left_stick_x']:.3f}, Y={p1_input['left_stick_y']:.3f}"
            )

        # Check Player 2 configuration
        p2_gamepad_connected = gamepad_manager.is_gamepad_connected(GAMEPAD_2_INDEX)
        print(
            f"Player 2 gamepad (index {GAMEPAD_2_INDEX}) connected: {p2_gamepad_connected}"
        )

        if p2_gamepad_connected:
            p2_input = gamepad_manager.get_gamepad_input(GAMEPAD_2_INDEX)
            print(
                f"Player 2 input: X={p2_input['left_stick_x']:.3f}, Y={p2_input['left_stick_y']:.3f}"
            )

        # Check actual game engine state
        print(
            f"Game engine gamepad manager exists: {hasattr(game_engine, '_gamepad_manager') and game_engine._gamepad_manager is not None}"
        )

        if hasattr(game_engine, "_gamepad_manager") and game_engine._gamepad_manager:
            ge_p1_connected = game_engine._gamepad_manager.is_gamepad_connected(
                GAMEPAD_1_INDEX
            )
            print(f"Game engine sees Player 1 gamepad connected: {ge_p1_connected}")

            if ge_p1_connected:
                ge_p1_input = game_engine._gamepad_manager.get_gamepad_input(
                    GAMEPAD_1_INDEX
                )
                print(
                    f"Game engine Player 1 input: X={ge_p1_input['left_stick_x']:.3f}, Y={ge_p1_input['left_stick_y']:.3f}"
                )

        # Check red dot acceleration
        print(
            f"Red dot acceleration: X={game_engine.red_dot.acceleration_x:.3f}, Y={game_engine.red_dot.acceleration_y:.3f}"
        )

        # Check for problematic scenarios
        all_gamepads_zero = True
        for i in range(gamepad_manager.gamepad_count):
            if gamepad_manager.is_gamepad_connected(i):
                input_data = gamepad_manager.get_gamepad_input(i)
                if (
                    abs(input_data["left_stick_x"]) > 0.01
                    or abs(input_data["left_stick_y"]) > 0.01
                ):
                    all_gamepads_zero = False
                    break

        if all_gamepads_zero and (
            abs(game_engine.red_dot.acceleration_x) > 0.01
            or abs(game_engine.red_dot.acceleration_y) > 0.01
        ):
            print("🔴 PROBLEM: All gamepads at zero but red dot has acceleration!")
            print(
                f"   Red dot accel: X={game_engine.red_dot.acceleration_x:.3f}, Y={game_engine.red_dot.acceleration_y:.3f}"
            )

    debug_timer = QTimer()
    debug_timer.timeout.connect(debug_frame)
    debug_timer.start(500)  # Print every 500ms for readability

    split_screen.show()

    # Start game timer
    game_timer = QTimer()
    game_timer.timeout.connect(game_engine.update_game_state)
    game_timer.start(16)

    print("🎮 Dual Gamepad Player 1 Debug Mode")
    print("💡 Try moving either gamepad and observe Player 1 behavior")
    print("🔍 Looking for cases where Player 1 accelerates when it shouldn't")
    print("Close the game window to exit.")

    sys.exit(app.exec())


if __name__ == "__main__":
    debug_dual_in_game()
