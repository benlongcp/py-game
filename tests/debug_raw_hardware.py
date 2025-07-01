#!/usr/bin/env python3
"""
Raw gamepad test to check if the issue is in our code or the hardware/driver.
"""

import pygame
import time
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import *


def test_raw_gamepad():
    pygame.init()
    pygame.joystick.init()

    gamepad_count = pygame.joystick.get_count()
    print(f"Found {gamepad_count} gamepad(s)")

    if gamepad_count == 0:
        print("No gamepads connected!")
        return

    # Initialize gamepad 0
    gamepad = pygame.joystick.Joystick(0)
    gamepad.init()
    print(f"Testing gamepad: {gamepad.get_name()}")

    print(f"\nInstructions:")
    print(f"1. Do NOT touch the analog stick")
    print(f"2. Press and release the A button (button 0)")
    print(f"3. Watch for stick values that should stay at 0.000")
    print(f"4. Press Ctrl+C to exit")
    print("=" * 60)

    prev_button = False

    try:
        while True:
            pygame.event.pump()

            # Get raw analog stick values (no processing)
            raw_x = gamepad.get_axis(0)
            raw_y = gamepad.get_axis(1)

            # Get A button
            button_a = gamepad.get_button(0)

            # Check for button state change
            if button_a != prev_button:
                if button_a:
                    print(f"🔴 A BUTTON PRESSED")
                else:
                    print(f"🔴 A BUTTON RELEASED")
                print(f"   Raw stick values: X={raw_x:+.6f}, Y={raw_y:+.6f}")

                # Check if stick values are suspiciously non-zero
                if abs(raw_x) > 0.01 or abs(raw_y) > 0.01:
                    print(f"🚨 PROBLEM: Stick not at center when button pressed!")
                    print(f"   This indicates hardware calibration or driver issue")
                else:
                    print(f"✅ Stick correctly at center")

                prev_button = button_a

            # Show periodic updates
            else:
                # Only show if values are non-zero or every 5 seconds
                if abs(raw_x) > 0.01 or abs(raw_y) > 0.01:
                    print(
                        f"Stick drift: X={raw_x:+.6f}, Y={raw_y:+.6f}, Button={button_a}"
                    )

            time.sleep(0.1)  # 10 times per second

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        pygame.quit()


if __name__ == "__main__":
    test_raw_gamepad()
