#!/usr/bin/env python3
"""
Debug script to test stick release behavior - checking for velocity persistence.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from game_engine import GameEngine
from split_screen import SplitScreenView
from config import *


def debug_stick_release():
    """Test what happens when stick is moved and then released."""
    app = QApplication(sys.argv)

    # Create game engine and split screen
    game_engine = GameEngine()
    game_engine.create_purple_dot()
    split_screen = SplitScreenView(game_engine)

    frame_count = 0
    prev_gamepad_x = 0
    prev_gamepad_y = 0

    def debug_frame():
        nonlocal frame_count, prev_gamepad_x, prev_gamepad_y
        frame_count += 1

        gamepad_manager = split_screen.gamepad_manager
        gamepad_manager.update()

        # Only show frames where something changes or every 30 frames
        show_frame = frame_count % 30 == 0

        # Get current gamepad input
        current_gamepad_x = 0
        current_gamepad_y = 0

        if gamepad_manager.is_gamepad_connected(GAMEPAD_1_INDEX):
            p1_input = gamepad_manager.get_gamepad_input(GAMEPAD_1_INDEX)
            current_gamepad_x = p1_input["left_stick_x"]
            current_gamepad_y = p1_input["left_stick_y"]

        # Check for input changes
        input_changed = (
            abs(current_gamepad_x - prev_gamepad_x) > 0.01
            or abs(current_gamepad_y - prev_gamepad_y) > 0.01
        )

        # Check red dot state
        red_dot = game_engine.red_dot
        red_accel_x = red_dot.acceleration_x
        red_accel_y = red_dot.acceleration_y
        red_vel_x = red_dot.velocity_x
        red_vel_y = red_dot.velocity_y

        # Detect stick return to center
        stick_returned_to_center = (
            abs(prev_gamepad_x) > 0.1 and abs(current_gamepad_x) < 0.05
        ) or (abs(prev_gamepad_y) > 0.1 and abs(current_gamepad_y) < 0.05)

        # Show frame if there's input change or stick returned to center
        if show_frame or input_changed or stick_returned_to_center:
            print(f"\n=== Frame {frame_count} ===")
            print(f"Gamepad 0: X={current_gamepad_x:.3f}, Y={current_gamepad_y:.3f}")
            print(f"Red dot acceleration: X={red_accel_x:.3f}, Y={red_accel_y:.3f}")
            print(f"Red dot velocity: X={red_vel_x:.3f}, Y={red_vel_y:.3f}")

            if stick_returned_to_center:
                print("📍 STICK RETURNED TO CENTER!")
                print(
                    f"   Previous stick: X={prev_gamepad_x:.3f}, Y={prev_gamepad_y:.3f}"
                )
                print(
                    f"   Current stick:  X={current_gamepad_x:.3f}, Y={current_gamepad_y:.3f}"
                )
                print(
                    f"   Acceleration should be ~0: X={red_accel_x:.3f}, Y={red_accel_y:.3f}"
                )
                print(
                    f"   But velocity might persist: X={red_vel_x:.3f}, Y={red_vel_y:.3f}"
                )

        # Check for problematic scenario: no input but high velocity
        no_input = abs(current_gamepad_x) < 0.05 and abs(current_gamepad_y) < 0.05
        no_accel = abs(red_accel_x) < 0.05 and abs(red_accel_y) < 0.05
        has_velocity = abs(red_vel_x) > 0.1 or abs(red_vel_y) > 0.1

        if no_input and no_accel and has_velocity:
            print(
                f"🟡 VELOCITY PERSISTENCE: No input/accel but velocity: X={red_vel_x:.3f}, Y={red_vel_y:.3f}"
            )

        # Check for problematic scenario: no input but has acceleration
        if no_input and not no_accel:
            print(
                f"🔴 ACCELERATION PROBLEM: No input but acceleration: X={red_accel_x:.3f}, Y={red_accel_y:.3f}"
            )

        prev_gamepad_x = current_gamepad_x
        prev_gamepad_y = current_gamepad_y

    debug_timer = QTimer()
    debug_timer.timeout.connect(debug_frame)
    debug_timer.start(16)  # Run at same rate as game

    split_screen.show()

    # Start game timer
    game_timer = QTimer()
    game_timer.timeout.connect(game_engine.update_game_state)
    game_timer.start(16)

    print("🎮 Stick Release Debug Mode")
    print("💡 Move Gamepad 0 (Player 1) stick and then release it back to center")
    print("🔍 Watching for velocity persistence after stick release")
    print("📝 Note: Velocity should decay over time due to deceleration")
    print("Close the game window to exit.")

    sys.exit(app.exec())


if __name__ == "__main__":
    debug_stick_release()
