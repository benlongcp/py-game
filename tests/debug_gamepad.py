#!/usr/bin/env python3
"""
Debug script to test gamepad input within the game context.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from game_engine import GameEngine
from split_screen import SplitScreenView
from gamepad_manager import GamepadManager
from config import *


def debug_gamepad_in_game():
    """Test gamepad input in the actual game context."""
    app = QApplication(sys.argv)

    # Create game engine and split screen
    game_engine = GameEngine()
    game_engine.create_purple_dot()
    split_screen = SplitScreenView(game_engine)

    # Create a debug timer to print gamepad input
    def debug_gamepad():
        gamepad_manager = split_screen.gamepad_manager
        gamepad_manager.update()

        print(f"Gamepad enabled: {GAMEPAD_ENABLED}")
        print(f"Gamepad count: {gamepad_manager.gamepad_count}")

        if gamepad_manager.is_gamepad_connected(0):
            input_data = gamepad_manager.get_gamepad_input(0)
            if (
                abs(input_data["left_stick_x"]) > 0.1
                or abs(input_data["left_stick_y"]) > 0.1
                or input_data["shoot_button"]
            ):
                print(
                    f"🎮 Input: X={input_data['left_stick_x']:.2f}, "
                    f"Y={input_data['left_stick_y']:.2f}, "
                    f"Shoot={input_data['shoot_button']}"
                )

                # Check if red dot acceleration is being set
                red_dot = game_engine.red_dot
                print(
                    f"Red dot accel: X={red_dot.acceleration_x:.2f}, Y={red_dot.acceleration_y:.2f}"
                )
        else:
            print("No gamepad connected on index 0")

    debug_timer = QTimer()
    debug_timer.timeout.connect(debug_gamepad)
    debug_timer.start(500)  # Print every 500ms

    split_screen.show()

    # Start game timer
    game_timer = QTimer()
    game_timer.timeout.connect(game_engine.update_game_state)
    game_timer.start(16)

    print(
        "🎮 Debug mode started. Move gamepad stick or press A button to see debug output."
    )
    print("Close the game window to exit.")

    sys.exit(app.exec())


if __name__ == "__main__":
    debug_gamepad_in_game()
