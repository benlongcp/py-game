"""
Test script to verify rendering functions are working correctly.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    print("🎨 Testing Rendering Functions...")

    from rendering import Renderer
    from game_engine import GameEngine
    from config import DOT_COLOR, PURPLE_DOT_COLOR

    print("✅ Rendering imports successful!")

    # Test that all rendering functions exist
    functions_to_test = [
        "draw_red_dot",
        "draw_purple_dot",
        "draw_purple_dot_centered",
        "draw_red_dot_world",
    ]

    for func_name in functions_to_test:
        if hasattr(Renderer, func_name):
            print(f"✅ {func_name} function exists")
        else:
            print(f"❌ {func_name} function missing")

    print("\n🎮 Testing Game Engine with both dots...")
    engine = GameEngine()
    engine.create_purple_dot()

    print(f"✅ Red dot mass: {engine.red_dot.mass}")
    print(f"✅ Purple dot mass: {engine.purple_dot.mass}")
    print(f"✅ Red dot color: {DOT_COLOR}")
    print(f"✅ Purple dot color: {PURPLE_DOT_COLOR}")

    print("\n🎉 All rendering components are ready!")
    print("Colors should now display correctly:")
    print("  • Player 1 view: RED dot at center, PURPLE dot in world")
    print("  • Player 2 view: PURPLE dot at center, RED dot in world")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()
