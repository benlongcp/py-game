#!/usr/bin/env python3
"""
Debug script to test the sticky acceleration issue after gamepad input stops.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from game_engine import GameEngine
from split_screen import SplitScreenView
from config import *


def debug_sticky_acceleration():
    """Test for sticky acceleration issue."""
    app = QApplication(sys.argv)

    # Create game engine and split screen
    game_engine = GameEngine()
    game_engine.create_purple_dot()
    split_screen = SplitScreenView(game_engine)

    # Track previous values to detect changes
    prev_red_accel_x = 0
    prev_red_accel_y = 0
    prev_gamepad_x = 0
    prev_gamepad_y = 0
    frame_count = 0

    def debug_frame():
        nonlocal prev_red_accel_x, prev_red_accel_y, prev_gamepad_x, prev_gamepad_y, frame_count
        frame_count += 1

        gamepad_manager = split_screen.gamepad_manager
        gamepad_manager.update()

        # Only print every 10 frames unless there's an issue
        should_print = frame_count % 10 == 0

        # Check Player 1 (Red) specifically
        if gamepad_manager.is_gamepad_connected(GAMEPAD_1_INDEX):
            gamepad1_input = gamepad_manager.get_gamepad_input(GAMEPAD_1_INDEX)
            current_gamepad_x = gamepad1_input["left_stick_x"]
            current_gamepad_y = gamepad1_input["left_stick_y"]

            # Calculate what acceleration should be
            expected_accel_x = current_gamepad_x * ANALOG_STICK_MULTIPLIER
            expected_accel_y = current_gamepad_y * ANALOG_STICK_MULTIPLIER

            # Get actual acceleration
            actual_accel_x = game_engine.red_dot.acceleration_x
            actual_accel_y = game_engine.red_dot.acceleration_y

            # Check for sticky acceleration (input is zero but acceleration is not)
            sticky_x = abs(current_gamepad_x) < 0.01 and abs(actual_accel_x) > 0.01
            sticky_y = abs(current_gamepad_y) < 0.01 and abs(actual_accel_y) > 0.01

            # Check for mismatch between expected and actual
            mismatch_x = abs(expected_accel_x - actual_accel_x) > 0.001
            mismatch_y = abs(expected_accel_y - actual_accel_y) > 0.001

            # Print if there's an issue or if it's time for regular update
            if should_print or sticky_x or sticky_y or mismatch_x or mismatch_y:
                print(f"\n=== Frame {frame_count} ===")
                print(
                    f"Gamepad input: X={current_gamepad_x:.3f}, Y={current_gamepad_y:.3f}"
                )
                print(
                    f"Expected accel: X={expected_accel_x:.3f}, Y={expected_accel_y:.3f}"
                )
                print(f"Actual accel:   X={actual_accel_x:.3f}, Y={actual_accel_y:.3f}")

                if sticky_x:
                    print(
                        f"🔴 STICKY X: Gamepad X is ~0 but accel X is {actual_accel_x:.3f}"
                    )
                if sticky_y:
                    print(
                        f"🔴 STICKY Y: Gamepad Y is ~0 but accel Y is {actual_accel_y:.3f}"
                    )
                if mismatch_x:
                    print(
                        f"⚠️  MISMATCH X: expected {expected_accel_x:.3f}, got {actual_accel_x:.3f}"
                    )
                if mismatch_y:
                    print(
                        f"⚠️  MISMATCH Y: expected {expected_accel_y:.3f}, got {actual_accel_y:.3f}"
                    )

            # Detect when stick returns to center
            if abs(prev_gamepad_x) > 0.1 and abs(current_gamepad_x) < 0.05:
                print(
                    f"📍 STICK RETURNED TO CENTER X: {prev_gamepad_x:.3f} → {current_gamepad_x:.3f}"
                )
                print(f"   Acceleration should now be ~0, but is: {actual_accel_x:.3f}")

            if abs(prev_gamepad_y) > 0.1 and abs(current_gamepad_y) < 0.05:
                print(
                    f"📍 STICK RETURNED TO CENTER Y: {prev_gamepad_y:.3f} → {current_gamepad_y:.3f}"
                )
                print(f"   Acceleration should now be ~0, but is: {actual_accel_y:.3f}")

            # Update previous values
            prev_gamepad_x = current_gamepad_x
            prev_gamepad_y = current_gamepad_y
            prev_red_accel_x = actual_accel_x
            prev_red_accel_y = actual_accel_y

    debug_timer = QTimer()
    debug_timer.timeout.connect(debug_frame)
    debug_timer.start(16)  # Run at same rate as game

    split_screen.show()

    # Start game timer
    game_timer = QTimer()
    game_timer.timeout.connect(game_engine.update_game_state)
    game_timer.start(16)

    print("🎮 Sticky Acceleration Debug Mode")
    print("💡 Move the left stick slightly and then let go to center position")
    print("🔍 Watch for sticky acceleration after stick returns to center")
    print("Close the game window to exit.")

    sys.exit(app.exec())


if __name__ == "__main__":
    debug_sticky_acceleration()
