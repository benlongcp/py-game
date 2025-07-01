#!/usr/bin/env python3
"""
Debug script to check what happens when A button is pressed.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from game_engine import GameEngine
from split_screen import SplitScreenView
from config import *


def debug_a_button():
    """Test what happens when A button is pressed."""
    app = QApplication(sys.argv)

    # Create game engine and split screen
    game_engine = GameEngine()
    game_engine.create_purple_dot()
    split_screen = SplitScreenView(game_engine)

    frame_count = 0
    prev_a_button = False

    def debug_frame():
        nonlocal frame_count, prev_a_button
        frame_count += 1

        gamepad_manager = split_screen.gamepad_manager

        # Only show frames where something changes or every 30 frames
        show_frame = frame_count % 30 == 0

        # Get current gamepad input
        current_a_button = False
        current_stick_x = 0
        current_stick_y = 0

        if gamepad_manager.is_gamepad_connected(GAMEPAD_1_INDEX):
            p1_input = gamepad_manager.get_gamepad_input(GAMEPAD_1_INDEX)
            current_a_button = p1_input["shoot_button"]
            current_stick_x = p1_input["left_stick_x"]
            current_stick_y = p1_input["left_stick_y"]

        # Check for A button press/release
        a_button_changed = current_a_button != prev_a_button

        # Check red dot state
        red_dot = game_engine.red_dot
        red_accel_x = red_dot.acceleration_x
        red_accel_y = red_dot.acceleration_y

        # Show frame if A button changed or regular interval
        if show_frame or a_button_changed:
            print(f"\n=== Frame {frame_count} ===")
            print(f"A button: {current_a_button} (was {prev_a_button})")
            print(f"Stick: X={current_stick_x:.3f}, Y={current_stick_y:.3f}")
            print(f"Red dot acceleration: X={red_accel_x:.3f}, Y={red_accel_y:.3f}")

            if a_button_changed:
                if current_a_button:
                    print("🔴 A BUTTON PRESSED!")
                else:
                    print("🔴 A BUTTON RELEASED!")
                print(
                    f"   Stick should be zero: X={current_stick_x:.3f}, Y={current_stick_y:.3f}"
                )
                print(
                    f"   Acceleration should match stick: X={red_accel_x:.3f}, Y={red_accel_y:.3f}"
                )

                # Calculate expected acceleration
                expected_x = current_stick_x * ANALOG_STICK_MULTIPLIER
                expected_y = current_stick_y * ANALOG_STICK_MULTIPLIER
                print(
                    f"   Expected acceleration: X={expected_x:.3f}, Y={expected_y:.3f}"
                )

                if (
                    abs(red_accel_x - expected_x) > 0.01
                    or abs(red_accel_y - expected_y) > 0.01
                ):
                    print("🚨 MISMATCH: Acceleration doesn't match expected values!")

        # Check for phantom acceleration (stick at zero but acceleration non-zero)
        stick_at_zero = abs(current_stick_x) < 0.01 and abs(current_stick_y) < 0.01
        accel_non_zero = abs(red_accel_x) > 0.01 or abs(red_accel_y) > 0.01

        if stick_at_zero and accel_non_zero:
            print(
                f"🔴 PHANTOM ACCELERATION: Stick at zero but accel: X={red_accel_x:.3f}, Y={red_accel_y:.3f}"
            )

        prev_a_button = current_a_button

    debug_timer = QTimer()
    debug_timer.timeout.connect(debug_frame)
    debug_timer.start(16)  # Run at same rate as game

    split_screen.show()

    # Start game timer
    game_timer = QTimer()
    game_timer.timeout.connect(game_engine.update_game_state)
    game_timer.start(16)

    print("🎮 A Button Debug Mode")
    print(
        "💡 Press the A button on Gamepad 0 (Player 1) without touching the analog stick"
    )
    print("🔍 Watching for phantom acceleration when A button is pressed")
    print("📝 The stick should remain at (0,0) and acceleration should be (0,0)")
    print("Close the game window to exit.")

    sys.exit(app.exec())


if __name__ == "__main__":
    debug_a_button()
