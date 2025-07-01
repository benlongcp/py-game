"""
Debug script to check raw gamepad analog stick values.
This will help determine if there's hardware drift or software issues.
"""

import pygame
import time
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import *


def main():
    pygame.init()
    pygame.joystick.init()

    gamepad_count = pygame.joystick.get_count()
    print(f"Found {gamepad_count} gamepad(s)")

    if gamepad_count == 0:
        print("No gamepads connected!")
        return

    # Initialize all gamepads
    gamepads = []
    for i in range(gamepad_count):
        gamepad = pygame.joystick.Joystick(i)
        gamepad.init()
        gamepads.append(gamepad)
        print(f"Gamepad {i}: {gamepad.get_name()}")

    print(f"\nCurrent deadzone setting: {GAMEPAD_DEADZONE}")
    print("Press Ctrl+C to exit")
    print("=" * 60)

    try:
        while True:
            pygame.event.pump()

            for i, gamepad in enumerate(gamepads):
                # Get raw values
                raw_x = gamepad.get_axis(0)
                raw_y = gamepad.get_axis(1)

                # Apply deadzone
                processed_x = raw_x if abs(raw_x) >= GAMEPAD_DEADZONE else 0.0
                processed_y = raw_y if abs(raw_y) >= GAMEPAD_DEADZONE else 0.0

                # Apply sensitivity
                final_x = processed_x * GAMEPAD_SENSITIVITY
                final_y = processed_y * GAMEPAD_SENSITIVITY

                print(
                    f"Gamepad {i}: Raw({raw_x:+.4f}, {raw_y:+.4f}) "
                    f"Processed({processed_x:+.4f}, {processed_y:+.4f}) "
                    f"Final({final_x:+.4f}, {final_y:+.4f})"
                )

            print("-" * 60)
            time.sleep(0.1)  # 10 updates per second

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
