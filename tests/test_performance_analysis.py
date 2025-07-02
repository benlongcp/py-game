#!/usr/bin/env python3
"""
Performance analysis script to identify bottlenecks causing gameplay lag.
"""

import sys
import os
import time
import cProfile
import pstats
from io import StringIO

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from game_engine import GameEngine
from split_screen import SplitScreenView
from config import *


class PerformanceAnalyzer:
    """Analyze performance bottlenecks in the game."""

    def __init__(self):
        self.frame_times = []
        self.update_times = []
        self.render_times = []
        self.fps_samples = []
        self.last_time = time.time()

    def start_frame(self):
        """Mark the start of a frame."""
        self.last_time = time.time()

    def end_frame(self):
        """Mark the end of a frame and record timing."""
        frame_time = time.time() - self.last_time
        self.frame_times.append(frame_time)
        fps = 1.0 / frame_time if frame_time > 0 else 0
        self.fps_samples.append(fps)

    def analyze_performance(self):
        """Analyze collected performance data."""
        if not self.frame_times:
            return

        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        avg_fps = sum(self.fps_samples) / len(self.fps_samples)
        min_fps = min(self.fps_samples)
        max_fps = max(self.fps_samples)

        print("\n📊 PERFORMANCE ANALYSIS")
        print("=" * 50)
        print(f"🎯 Target FPS: {FPS}")
        print(f"📈 Average FPS: {avg_fps:.1f}")
        print(f"📉 Minimum FPS: {min_fps:.1f}")
        print(f"📊 Maximum FPS: {max_fps:.1f}")
        print(f"⏱️  Average frame time: {avg_frame_time*1000:.2f}ms")
        print(f"🎮 Target frame time: {FRAME_TIME_MS}ms")

        if avg_fps < FPS * 0.9:  # If below 90% of target
            print("\n⚠️  PERFORMANCE ISSUES DETECTED:")
            self._suggest_optimizations(avg_fps)
        else:
            print("\n✅ Performance is within acceptable range")

    def _suggest_optimizations(self, current_fps):
        """Suggest specific optimizations based on performance."""
        performance_ratio = current_fps / FPS

        print(f"   • Performance is {(1-performance_ratio)*100:.1f}% below target")
        print("\n🔧 POTENTIAL OPTIMIZATIONS:")

        # Check specific areas
        print("1. Grid Rendering:")
        print("   • Consider reducing GRID_RADIUS in config.py")
        print("   • Try increasing GRID_SPACING to draw fewer dots")
        print("   • Implement level-of-detail for distant grid dots")

        print("\n2. Physics Updates:")
        print("   • Review projectile count - consider PROJECTILE_MAX_COUNT")
        print("   • Check gravitational force calculations")
        print("   • Optimize collision detection algorithms")

        print("\n3. Rendering Optimizations:")
        print("   • Reduce anti-aliasing if enabled")
        print("   • Consider disabling vignette gradient")
        print("   • Implement viewport culling for off-screen objects")

        print("\n4. Timer Configuration:")
        print("   • Current FRAME_TIME_MS:", FRAME_TIME_MS)
        print("   • Consider increasing to 20ms (50 FPS) if needed")


def profile_game_performance():
    """Profile the game to identify performance bottlenecks."""
    print("🔍 Starting Performance Analysis...")
    print("This will run the game for 10 seconds and measure performance")

    app = QApplication(sys.argv)
    analyzer = PerformanceAnalyzer()

    # Create game with full setup
    game_engine = GameEngine()
    game_engine.create_purple_dot()
    split_screen = SplitScreenView(game_engine)

    # Add some projectiles to stress test
    for i in range(5):
        game_engine.shoot_projectile_player1()
        game_engine.shoot_projectile_player2()

    frame_count = 0
    start_time = time.time()

    def measure_frame():
        nonlocal frame_count
        analyzer.start_frame()

        # Simulate game update
        update_start = time.time()
        game_engine.update_game_state()
        update_time = time.time() - update_start

        # Trigger repaint
        render_start = time.time()
        split_screen.update()
        render_time = time.time() - render_start

        analyzer.end_frame()
        frame_count += 1

        # Stop after 10 seconds
        if time.time() - start_time > 10:
            analyzer.analyze_performance()
            print(
                f"\n📊 Measured {frame_count} frames over {time.time() - start_time:.1f} seconds"
            )

            # Additional diagnostics
            print("\n🔍 SYSTEM DIAGNOSTICS:")
            print(f"   • Window size: {split_screen.width()}x{split_screen.height()}")
            print(f"   • Grid radius: {GRID_RADIUS}")
            print(f"   • Grid spacing: {GRID_SPACING}")
            print(f"   • Max projectiles: {PROJECTILE_MAX_COUNT}")
            print(f"   • Current projectiles: {len(game_engine.projectiles)}")
            print(f"   • FPS counter enabled: {SHOW_FPS_COUNTER}")

            app.quit()

    # Setup timer for measurement
    measure_timer = QTimer()
    measure_timer.timeout.connect(measure_frame)
    measure_timer.start(FRAME_TIME_MS)

    split_screen.show()
    sys.exit(app.exec())


def profile_with_cprofile():
    """Use cProfile to get detailed function-level profiling."""
    print("🔬 Running detailed function profiling...")

    pr = cProfile.Profile()
    pr.enable()

    # Run a simplified version
    app = QApplication(sys.argv)
    game_engine = GameEngine()
    game_engine.create_purple_dot()

    # Simulate several update cycles
    for i in range(100):
        game_engine.update_game_state()

    pr.disable()

    # Analyze results
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
    ps.print_stats(20)  # Top 20 functions

    print("\n🔬 TOP PERFORMANCE BOTTLENECKS:")
    print("=" * 50)
    print(s.getvalue())


if __name__ == "__main__":
    print("🎯 Game Performance Analysis Tool")
    print("=" * 40)
    print("This tool will help identify performance bottlenecks")
    print("Choose analysis type:")
    print("1. Real-time performance measurement (recommended)")
    print("2. Detailed function profiling")

    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == "2":
        profile_with_cprofile()
    else:
        profile_game_performance()
