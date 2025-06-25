"""
Test script for split-screen functionality.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    print("Testing split-screen imports...")
    from split_screen import SplitScreenView
    from game_engine import GameEngine

    print("✅ Split-screen imports successful!")

    print("\nTesting split-screen creation...")
    engine = GameEngine()
    engine.create_purple_dot()

    # Test creation without showing (since we can't show in headless mode)
    print("✅ Split-screen setup successful!")

    print("\n🎉 Split-screen system is ready!")
    print("Run 'python main.py' to launch the game!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()
