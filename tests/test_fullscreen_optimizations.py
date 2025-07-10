"""
Test the new fullscreen performance optimizations.
This script tests the optimizations applied specifically for fullscreen mode.
"""

import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, Qt
from main import MultiPlayerController


def test_fullscreen_optimizations():
    """Test the new fullscreen performance optimizations."""
    app = QApplication(sys.argv)

    # Create controller and start the game
    controller = MultiPlayerController()
    controller.start_launch_screen()
    controller.start_actual_game()  # Skip launch screen for testing

    print("Testing new fullscreen performance optimizations...")

    window = controller.split_screen_window
    game_engine = controller.game_engine
    split_screen = controller.split_screen_window

    # Test windowed mode first
    print("\n1. Testing WINDOWED mode baseline...")
    window.showNormal()
    window.resize(1200, 800)
    app.processEvents()
    time.sleep(1.0)  # Let it stabilize

    # Measure windowed FPS
    windowed_fps = measure_fps(game_engine, split_screen, app, duration=2.0)
    print(f"   Windowed FPS: {windowed_fps:.1f}")

    # Test fullscreen mode with optimizations
    print("\n2. Testing FULLSCREEN mode with optimizations...")
    window.showFullScreen()
    app.processEvents()
    time.sleep(1.0)  # Let optimizations take effect

    # Check that optimizations were applied
    print("   Checking optimization status:")
    print(f"   - Performance mode: {game_engine.performance_mode}")
    print(f"   - Fullscreen mode: {hasattr(game_engine, '_fullscreen_mode')}")
    print(f"   - Grid optimized: {hasattr(split_screen, '_fullscreen_optimized')}")

    # Check gamepad manager optimization
    if hasattr(game_engine, "_gamepad_manager") and game_engine._gamepad_manager:
        has_gamepad_opt = hasattr(game_engine._gamepad_manager, "_fullscreen_mode")
        print(f"   - Gamepad optimized: {has_gamepad_opt}")

    # Measure fullscreen FPS
    fullscreen_fps = measure_fps(game_engine, split_screen, app, duration=3.0)
    print(f"   Fullscreen FPS: {fullscreen_fps:.1f}")

    # Calculate improvement
    improvement = ((fullscreen_fps / windowed_fps) * 100) if windowed_fps > 0 else 0
    print(f"   Fullscreen performance: {improvement:.1f}% of windowed")

    # Test mode switching
    print("\n3. Testing mode switching...")
    window.showNormal()
    app.processEvents()
    time.sleep(0.5)

    # Check that optimizations were disabled
    print("   Optimization status after returning to windowed:")
    print(
        f"   - Fullscreen mode: {hasattr(game_engine, '_fullscreen_mode') and game_engine._fullscreen_mode}"
    )
    print(
        f"   - Grid optimized: {hasattr(split_screen, '_fullscreen_optimized') and split_screen._fullscreen_optimized}"
    )

    # Performance assessment
    print("\n" + "=" * 60)
    print("PERFORMANCE ASSESSMENT")
    print("=" * 60)

    if fullscreen_fps >= 45:
        print("✅ EXCELLENT: Fullscreen FPS meets target (45+ FPS)")
    elif fullscreen_fps >= 30:
        print("⚠️  ACCEPTABLE: Fullscreen FPS is playable (30-45 FPS)")
    else:
        print("❌ POOR: Fullscreen FPS below playable threshold (<30 FPS)")

    if improvement >= 70:
        print("✅ GOOD: Fullscreen performance is within 30% of windowed")
    elif improvement >= 50:
        print("⚠️  FAIR: Fullscreen has noticeable but acceptable slowdown")
    else:
        print("❌ BAD: Fullscreen has significant performance degradation")

    print(f"\nFinal Results:")
    print(f"  Windowed FPS: {windowed_fps:.1f}")
    print(f"  Fullscreen FPS: {fullscreen_fps:.1f}")
    print(f"  Performance ratio: {improvement:.1f}%")

    # Recommendations
    if fullscreen_fps < 30:
        print(f"\n📋 RECOMMENDATIONS:")
        print(f"  - Consider further reducing projectile limits in fullscreen")
        print(f"  - Disable antialiasing in fullscreen mode")
        print(f"  - Reduce render resolution cap further")
        print(f"  - Implement level-of-detail (LOD) for distant objects")

    window.close()
    app.quit()


def measure_fps(game_engine, split_screen, app, duration=2.0):
    """Measure FPS over a specified duration."""
    frame_times = []
    start_time = time.perf_counter()
    frame_count = 0

    # Add some projectiles to make it more realistic
    for _ in range(10):
        game_engine.shoot_projectile_player1()
        if game_engine.purple_dot:
            game_engine.shoot_projectile_player2()

    while time.perf_counter() - start_time < duration:
        frame_start = time.perf_counter()

        game_engine.update_game_state()
        split_screen.game_view.update()
        app.processEvents()

        frame_end = time.perf_counter()
        frame_times.append(frame_end - frame_start)
        frame_count += 1

    total_time = time.perf_counter() - start_time
    avg_fps = frame_count / total_time
    return avg_fps


if __name__ == "__main__":
    test_fullscreen_optimizations()
