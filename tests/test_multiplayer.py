"""
Quick test script to validate all imports and basic functionality.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    print("Testing imports...")
    from game_engine import GameEngine
    from topographical_plane import TopographicalPlane
    from objects import RedDot, BlueSquare, PurpleDot, Projectile
    from rendering import Renderer
    from physics import PhysicsEngine

    print("✅ All imports successful!")

    print("\nTesting GameEngine creation...")
    engine = GameEngine()
    print("✅ GameEngine created successfully!")

    print("\nTesting Purple Dot creation...")
    engine.create_purple_dot()
    print("✅ Purple Dot created successfully!")

    print("\nTesting game state update...")
    engine.update_game_state()
    print("✅ Game state update successful!")

    print("\n🎉 All tests passed! Multi-player system is ready!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()
