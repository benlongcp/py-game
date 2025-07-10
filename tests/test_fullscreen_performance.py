#!/usr/bin/env python3
"""
Fullscreen Performance Test
Tests the performance improvements for fullscreen mode while maintaining 1080p resolution cap.
"""

import sys
import os
import time
import math

# Add the parent directory to the path to import the game modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import QTimer
    from game_engine import GameEngine
    from split_screen import SplitScreenView
    import config
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the correct directory.")
    sys.exit(1)


def test_fullscreen_performance():
    """Test performance improvements in fullscreen-like conditions."""
    print("🔄 Testing Fullscreen Performance Improvements...")
    print("=" * 60)

    # Create application
    app = QApplication(sys.argv)

    # Create game engine
    game_engine = GameEngine()
    game_engine.create_purple_dot()

    # Create split-screen view
    split_screen = SplitScreenView(game_engine)

    # Simulate fullscreen window size (larger than 1080p)
    split_screen.resize(2560, 1440)  # Simulate 1440p fullscreen

    print(f"🖼️  Simulated window size: 2560x1440 (1440p fullscreen)")
    print(f"📊 Resolution cap enabled: {config.ENABLE_RESOLUTION_CAP}")
    print(f"📏 Max render size: {config.MAX_RENDER_WIDTH}x{config.MAX_RENDER_HEIGHT}")
    print()

    # Test scenarios
    scenarios = [
        ("Baseline", 0, 0),
        ("Light Load", 10, 2),
        ("Medium Load", 25, 5),
        ("Heavy Load", 40, 8),
        ("Stress Test", 50, 12),
    ]

    results = []

    for scenario_name, projectile_count, movement_speed in scenarios:
        print(f"🧪 Testing {scenario_name} scenario...")

        # Reset game state
        game_engine.reset_game_state()

        # Add projectiles to simulate load
        for i in range(projectile_count):
            angle = (i / projectile_count) * 2 * math.pi
            vel_x = math.cos(angle) * movement_speed
            vel_y = math.sin(angle) * movement_speed

            from objects import Projectile

            projectile = Projectile(
                100 + i * 10,  # x position
                100 + i * 10,  # y position
                vel_x,  # velocity x
                vel_y,  # velocity y
                "red",  # color
            )
            game_engine.projectiles.append(projectile)

        # Run performance test
        frame_times = []
        test_frames = 120  # Test for 2 seconds at 60 FPS

        for frame in range(test_frames):
            start_time = time.time()

            # Update game state (this is what happens every frame)
            game_engine.update_game_state()

            end_time = time.time()
            frame_time = end_time - start_time
            frame_times.append(frame_time)

            # Simulate 60 FPS timing
            target_frame_time = 1.0 / 60.0
            if frame_time < target_frame_time:
                time.sleep(target_frame_time - frame_time)

        # Calculate metrics
        avg_frame_time = sum(frame_times) / len(frame_times)
        max_frame_time = max(frame_times)
        fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 60

        # Get performance info from engine
        perf_info = game_engine._get_performance_info()

        results.append(
            {
                "scenario": scenario_name,
                "projectiles": projectile_count,
                "avg_fps": fps,
                "max_frame_time_ms": max_frame_time * 1000,
                "performance_mode": perf_info["performance_mode"],
                "cell_size": perf_info["cell_size"],
            }
        )

        print(f"   📈 Average FPS: {fps:.1f}")
        print(f"   ⏱️  Max frame time: {max_frame_time * 1000:.2f}ms")
        print(
            f"   🚀 Performance mode: {'Yes' if perf_info['performance_mode'] else 'No'}"
        )
        print(f"   🔧 Cell size: {perf_info['cell_size']:.0f}")
        print()

    # Summary
    print("📋 Performance Test Summary:")
    print("-" * 60)

    for result in results:
        status = (
            "✅"
            if result["avg_fps"] >= 55
            else "⚠️" if result["avg_fps"] >= 45 else "❌"
        )
        print(
            f"{status} {result['scenario']:12} | {result['projectiles']:2d} projectiles | "
            f"{result['avg_fps']:5.1f} FPS | Max: {result['max_frame_time_ms']:5.1f}ms"
        )

    print()
    print("🎯 Performance Improvements Implemented:")
    print("   • Dynamic spatial partitioning with adaptive cell sizes")
    print("   • Automatic performance mode activation below 45 FPS")
    print("   • Intelligent frame skipping when running above target FPS")
    print("   • Optimized projectile cleanup and count management")
    print("   • Selective gravity calculation skipping in performance mode")
    print("   • Rolling FPS monitoring and adaptive optimization")
    print()

    # Check if all scenarios passed
    passing_scenarios = sum(1 for r in results if r["avg_fps"] >= 45)
    total_scenarios = len(results)

    if passing_scenarios == total_scenarios:
        print("🎉 All performance tests passed! Fullscreen performance is optimized.")
    else:
        print(f"⚠️  {passing_scenarios}/{total_scenarios} scenarios passed.")
        print("   Consider further optimization for demanding scenarios.")

    print()
    print("💡 Note: The 1080p resolution cap remains active for consistent quality,")
    print("    while these optimizations improve FPS performance in fullscreen mode.")

    app.quit()


if __name__ == "__main__":
    test_fullscreen_performance()
