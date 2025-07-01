#!/usr/bin/env python3
"""
Debug script to test dual gamepad input and check for drift.
"""

import sys
import time
from gamepad_manager import GamepadManager
from config import *


def debug_dual_gamepad():
    """Test both gamepads for input drift and values."""
    print("🎮 Testing Dual Gamepad Input...")

    manager = GamepadManager()

    print(f"📍 Found {manager.gamepad_count} gamepad(s)")

    if manager.gamepad_count < 2:
        print("❌ Need at least 2 gamepads for dual gamepad test.")
        return

    print(f"\n🔍 Testing for stick drift and default values...")
    print("📝 Make sure NO sticks are being moved and NO buttons are pressed!")
    print("   This will test for default/drift values...")
    print()

    # Test with no input for 5 seconds
    start_time = time.time()
    drift_samples = []

    while time.time() - start_time < 5:
        manager.update()

        # Check both gamepads
        for gamepad_index in range(2):
            if manager.is_gamepad_connected(gamepad_index):
                input_data = manager.get_gamepad_input(gamepad_index)

                # Record any non-zero values (potential drift)
                if (
                    abs(input_data["left_stick_x"]) > 0.01
                    or abs(input_data["left_stick_y"]) > 0.01
                    or input_data["shoot_button"]
                ):

                    drift_samples.append(
                        {
                            "gamepad": gamepad_index,
                            "x": input_data["left_stick_x"],
                            "y": input_data["left_stick_y"],
                            "button": input_data["shoot_button"],
                            "time": time.time() - start_time,
                        }
                    )

        time.sleep(0.1)

    # Analyze drift
    print(f"\n📊 Drift Analysis:")
    if not drift_samples:
        print("✅ No drift detected - both gamepads are clean")
    else:
        print(f"⚠️  Detected {len(drift_samples)} drift samples:")
        for sample in drift_samples[:10]:  # Show first 10 samples
            print(
                f"   Gamepad {sample['gamepad']}: X={sample['x']:.3f}, Y={sample['y']:.3f}, "
                f"Button={sample['button']} at {sample['time']:.1f}s"
            )

        if len(drift_samples) > 10:
            print(f"   ... and {len(drift_samples) - 10} more samples")

    # Test deadzone effectiveness
    print(f"\n🎯 Testing deadzone (current: {GAMEPAD_DEADZONE}):")
    manager.update()

    for gamepad_index in range(2):
        if manager.is_gamepad_connected(gamepad_index):
            input_data = manager.get_gamepad_input(gamepad_index)
            raw_x = manager.gamepads[gamepad_index].get_axis(0)
            raw_y = manager.gamepads[gamepad_index].get_axis(1)

            print(f"   Gamepad {gamepad_index}:")
            print(f"     Raw values: X={raw_x:.6f}, Y={raw_y:.6f}")
            print(
                f"     After deadzone: X={input_data['left_stick_x']:.6f}, Y={input_data['left_stick_y']:.6f}"
            )

            if abs(raw_x) > 0 and abs(input_data["left_stick_x"]) == 0:
                print(f"     ✅ X deadzone working (filtered {raw_x:.6f})")
            elif abs(raw_x) > GAMEPAD_DEADZONE:
                print(f"     ⚠️  X value above deadzone threshold")

            if abs(raw_y) > 0 and abs(input_data["left_stick_y"]) == 0:
                print(f"     ✅ Y deadzone working (filtered {raw_y:.6f})")
            elif abs(raw_y) > GAMEPAD_DEADZONE:
                print(f"     ⚠️  Y value above deadzone threshold")

    print(f"\n🔧 Recommendations:")
    if drift_samples:
        max_drift_x = max(abs(s["x"]) for s in drift_samples)
        max_drift_y = max(abs(s["y"]) for s in drift_samples)
        recommended_deadzone = max(max_drift_x, max_drift_y) + 0.05
        print(f"   Consider increasing GAMEPAD_DEADZONE to {recommended_deadzone:.2f}")
    else:
        print(f"   Current deadzone of {GAMEPAD_DEADZONE} appears sufficient")


if __name__ == "__main__":
    debug_dual_gamepad()
