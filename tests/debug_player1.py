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


def debug_player1_issue():
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

        # Only print every few frames to avoid spam
        if frame_count % 20 != 0:
            return

        gamepad_manager = split_screen.gamepad_manager
        gamepad_manager.update()

        print(f"\n=== Frame {frame_count} ===")
        print(f"Total gamepads: {gamepad_manager.gamepad_count}")
        print(f"GAMEPAD_1_INDEX = {GAMEPAD_1_INDEX} (Player 1)")
        print(f"GAMEPAD_2_INDEX = {GAMEPAD_2_INDEX} (Player 2)")

        # Check all connected gamepads
        for i in range(gamepad_manager.gamepad_count):
            if gamepad_manager.is_gamepad_connected(i):
                input_data = gamepad_manager.get_gamepad_input(i)
                print(
                    f"Gamepad {i}: X={input_data['left_stick_x']:.3f}, Y={input_data['left_stick_y']:.3f}"
                )

        # Check Player 1 assignment
        p1_gamepad_connected = gamepad_manager.is_gamepad_connected(GAMEPAD_1_INDEX)
        print(f"Player 1 using gamepad {GAMEPAD_1_INDEX}: {p1_gamepad_connected}")

        # Check red dot acceleration
        print(
            f"Red dot acceleration: X={game_engine.red_dot.acceleration_x:.3f}, Y={game_engine.red_dot.acceleration_y:.3f}"
        )

        # Check for the problem: All gamepads at zero but red dot has acceleration
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

        red_has_acceleration = (
            abs(game_engine.red_dot.acceleration_x) > 0.01
            or abs(game_engine.red_dot.acceleration_y) > 0.01
        )

        if all_gamepads_zero and red_has_acceleration:
            print(
                "🔴 PROBLEM DETECTED: All gamepads at zero but red dot has acceleration!"
            )
            print(
                f"   Red dot accel: X={game_engine.red_dot.acceleration_x:.3f}, Y={game_engine.red_dot.acceleration_y:.3f}"
            )

            # Debug the game engine logic
            print("🔍 Debugging game engine logic:")
            print(
                f"   Game engine has gamepad manager: {hasattr(game_engine, '_gamepad_manager') and game_engine._gamepad_manager is not None}"
            )
            if (
                hasattr(game_engine, "_gamepad_manager")
                and game_engine._gamepad_manager
            ):
                ge_connected = game_engine._gamepad_manager.is_gamepad_connected(
                    GAMEPAD_1_INDEX
                )
                print(
                    f"   Game engine sees gamepad {GAMEPAD_1_INDEX} connected: {ge_connected}"
                )
                if ge_connected:
                    ge_input = game_engine._gamepad_manager.get_gamepad_input(
                        GAMEPAD_1_INDEX
                    )
                    print(
                        f"   Game engine reads input: X={ge_input['left_stick_x']:.3f}, Y={ge_input['left_stick_y']:.3f}"
                    )

    debug_timer = QTimer()
    debug_timer.timeout.connect(debug_frame)
    debug_timer.start(16)  # Run at same rate as game

    split_screen.show()

    # Start game timer
    game_timer = QTimer()
    game_timer.timeout.connect(game_engine.update_game_state)
    game_timer.start(16)

    print("🎮 Player 1 Acceleration Debug Mode")
    print("💡 Move gamepad slightly then let go - watch for persistent acceleration")
    print(
        "🔍 Looking for cases where Player 1 accelerates when all gamepads are at zero"
    )
    print("Close the game window to exit.")

    sys.exit(app.exec())


if __name__ == "__main__":
    debug_player1_issue()
