#!/usr/bin/env python3
"""
Test script for gamepad detection and input.
"""

import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gamepad_manager import GamepadManager


def test_gamepad_detection():
    """Test gamepad detection and input functionality."""
    print("🎮 Testing Gamepad Detection...")

    manager = GamepadManager()

    print(f"📍 Found {manager.gamepad_count} gamepad(s)")

    if manager.gamepad_count == 0:
        print("❌ No gamepads detected. Please connect a gamepad and try again.")
        print("💡 Make sure your gamepad is properly connected via USB or Bluetooth.")
        return

    # Show gamepad info
    gamepad_info = manager.get_gamepad_info()
    for info in gamepad_info:
        print(f"🎯 Gamepad {info['index']}: {info['name']}")
        print(f"   Axes: {info['axes']}, Buttons: {info['buttons']}")

    print(f"\n🔄 Testing gamepad input for 10 seconds...")
    print("📝 Instructions:")
    print("   - Move the LEFT analog stick")
    print("   - Press the A button (or button 0)")
    print("   - Movement and button presses will be displayed below")
    print()

    start_time = time.time()
    last_print_time = 0

    while time.time() - start_time < 10:
        manager.update()
        current_time = time.time()

        # Print updates every 0.1 seconds to avoid spam
        if current_time - last_print_time > 0.1:
            any_input = False

            for i in range(manager.gamepad_count):
                input_state = manager.get_gamepad_input(i)

                if (
                    abs(input_state["left_stick_x"]) > 0
                    or abs(input_state["left_stick_y"]) > 0
                    or input_state["shoot_button"]
                ):

                    print(
                        f"🎮 Gamepad {i}: X={input_state['left_stick_x']:6.2f}, "
                        f"Y={input_state['left_stick_y']:6.2f}, "
                        f"Shoot={'YES' if input_state['shoot_button'] else 'NO '}"
                    )
                    any_input = True

            if any_input:
                last_print_time = current_time

        time.sleep(0.01)  # Small delay to prevent excessive CPU usage

    print(f"\n✅ Test complete!")
    print(f"💡 If you saw input above, your gamepad is working correctly.")
    print(f"🎯 You can now use your gamepad in the split-screen game mode.")


def main():
    """Main function to run the gamepad test."""
    test_gamepad_detection()


if __name__ == "__main__":
    main()
