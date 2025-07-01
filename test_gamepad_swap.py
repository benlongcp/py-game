#!/usr/bin/env python3
"""
Test script to swap gamepad assignments and see if the problem moves.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from game_engine import GameEngine
from split_screen import SplitScreenView

# Temporarily swap the gamepad indices
GAMEPAD_1_INDEX_ORIGINAL = 0  # Player 1 normally uses gamepad 0
GAMEPAD_2_INDEX_ORIGINAL = 1  # Player 2 normally uses gamepad 1

# Swap them
GAMEPAD_1_INDEX_SWAPPED = 1  # Player 1 now uses gamepad 1
GAMEPAD_2_INDEX_SWAPPED = 0  # Player 2 now uses gamepad 0


def test_swapped_gamepads():
    """Test with swapped gamepad assignments."""
    app = QApplication(sys.argv)

    # Monkey patch the config to swap gamepad indices
    import config

    config.GAMEPAD_1_INDEX = GAMEPAD_1_INDEX_SWAPPED
    config.GAMEPAD_2_INDEX = GAMEPAD_2_INDEX_SWAPPED

    # Create game engine and split screen
    game_engine = GameEngine()
    game_engine.create_purple_dot()
    split_screen = SplitScreenView(game_engine)

    frame_count = 0

    def debug_frame():
        nonlocal frame_count
        frame_count += 1

        if frame_count % 30 != 0:  # Print every 30 frames
            return

        gamepad_manager = split_screen.gamepad_manager
        gamepad_manager.update()

        print(f"\n=== SWAPPED TEST Frame {frame_count} ===")
        print(
            f"🔄 SWAPPED: Player 1 using gamepad {GAMEPAD_1_INDEX_SWAPPED} (normally {GAMEPAD_1_INDEX_ORIGINAL})"
        )
        print(
            f"🔄 SWAPPED: Player 2 using gamepad {GAMEPAD_2_INDEX_SWAPPED} (normally {GAMEPAD_2_INDEX_ORIGINAL})"
        )

        for i in range(gamepad_manager.gamepad_count):
            if gamepad_manager.is_gamepad_connected(i):
                input_data = gamepad_manager.get_gamepad_input(i)
                print(
                    f"Gamepad {i}: X={input_data['left_stick_x']:.3f}, Y={input_data['left_stick_y']:.3f}"
                )

        print(
            f"Red dot (Player 1) acceleration: X={game_engine.red_dot.acceleration_x:.3f}, Y={game_engine.red_dot.acceleration_y:.3f}"
        )
        if game_engine.purple_dot:
            print(
                f"Purple dot (Player 2) acceleration: X={game_engine.purple_dot.acceleration_x:.3f}, Y={game_engine.purple_dot.acceleration_y:.3f}"
            )

    debug_timer = QTimer()
    debug_timer.timeout.connect(debug_frame)
    debug_timer.start(16)

    split_screen.show()

    # Start game timer
    game_timer = QTimer()
    game_timer.timeout.connect(game_engine.update_game_state)
    game_timer.start(16)

    print("🔄 GAMEPAD SWAP TEST")
    print(
        f"Player 1 (Red) now uses gamepad {GAMEPAD_1_INDEX_SWAPPED} instead of {GAMEPAD_1_INDEX_ORIGINAL}"
    )
    print(
        f"Player 2 (Purple) now uses gamepad {GAMEPAD_2_INDEX_SWAPPED} instead of {GAMEPAD_2_INDEX_ORIGINAL}"
    )
    print(
        "💡 If the problem now affects Player 2 instead of Player 1, it's a physical gamepad issue"
    )
    print("Close the game window to exit.")

    sys.exit(app.exec())


if __name__ == "__main__":
    test_swapped_gamepads()
