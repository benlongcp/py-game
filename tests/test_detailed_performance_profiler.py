"""
Detailed performance profiler for BOXHOLE game.
This script profiles different components of the game to identify specific bottlenecks.
"""

import sys
import os
import time
import cProfile
import pstats
import io
from contextlib import contextmanager

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from main import MultiPlayerController
from config import *


class PerformanceProfiler:
    def __init__(self):
        self.profiles = {}
        self.timing_data = {}

    @contextmanager
    def profile_section(self, name):
        """Context manager for profiling code sections."""
        pr = cProfile.Profile()
        start_time = time.perf_counter()
        pr.enable()
        try:
            yield
        finally:
            pr.disable()
            end_time = time.perf_counter()

            # Store timing data
            self.timing_data[name] = end_time - start_time

            # Store profile data
            s = io.StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
            ps.print_stats(10)  # Top 10 functions
            self.profiles[name] = s.getvalue()

    def print_results(self):
        """Print profiling results."""
        print("\n" + "=" * 80)
        print("DETAILED PERFORMANCE PROFILER RESULTS")
        print("=" * 80)

        # Print timing summary
        print("\nTIMING SUMMARY:")
        print("-" * 40)
        for name, duration in sorted(
            self.timing_data.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"{name:30s}: {duration*1000:8.2f} ms")

        # Print detailed profiles
        for name, profile_output in self.profiles.items():
            print(f"\n{name.upper()} DETAILED PROFILE:")
            print("-" * 50)
            print(profile_output)


def test_detailed_performance():
    """Run detailed performance profiling test."""
    app = QApplication(sys.argv)
    profiler = PerformanceProfiler()

    # Create controller and start the game
    controller = MultiPlayerController()
    controller.start_launch_screen()
    controller.start_actual_game()  # Skip launch screen for testing

    print("Starting detailed performance profiling...")
    print("Testing both windowed and fullscreen modes...")

    # Test windowed mode first
    print("\n1. Testing WINDOWED mode performance...")
    window = controller.split_screen_window
    window.show()
    app.processEvents()

    # Get game engine and split screen
    game_engine = controller.game_engine
    split_screen = controller.split_screen_window
    app.processEvents()
    time.sleep(0.5)  # Let it stabilize

    # Force windowed mode
    window.showNormal()
    window.resize(1200, 800)
    app.processEvents()
    time.sleep(0.5)  # Let it stabilize

    # Profile windowed mode components
    with profiler.profile_section("windowed_game_update"):
        # Simulate 100 game updates
        for _ in range(100):
            game_engine.update_game_state()
            app.processEvents()

    with profiler.profile_section("windowed_paint_event"):
        # Simulate 50 paint events
        for _ in range(50):
            # Force a repaint
            split_screen.game_view.update()
            app.processEvents()

    # Test fullscreen mode
    print("\n2. Testing FULLSCREEN mode performance...")
    window.showFullScreen()
    app.processEvents()
    time.sleep(1.0)  # Let it stabilize

    # Profile fullscreen mode components
    with profiler.profile_section("fullscreen_game_update"):
        # Simulate 100 game updates
        for _ in range(100):
            game_engine.update_game_state()
            app.processEvents()

    with profiler.profile_section("fullscreen_paint_event"):
        # Simulate 50 paint events
        for _ in range(50):
            # Force a repaint
            split_screen.game_view.update()
            app.processEvents()

    # Profile specific rendering components in fullscreen
    with profiler.profile_section("fullscreen_player_view_rendering"):
        from PyQt6.QtGui import QPainter, QPixmap
        from PyQt6.QtCore import QRect

        # Create a test painter on a large canvas (simulating fullscreen)
        test_pixmap = QPixmap(1920, 1080)
        test_painter = QPainter(test_pixmap)
        test_painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Render player views multiple times
        for _ in range(20):
            split_screen._draw_player_view(test_painter, 1, 0, 0, 960, 1080)
            split_screen._draw_player_view(test_painter, 2, 960, 0, 960, 1080)

        test_painter.end()

    # Profile grid caching specifically
    with profiler.profile_section("grid_caching_performance"):
        # Force grid cache invalidation and regeneration
        split_screen._grid_cache = [None, None]
        split_screen._grid_cache_params = [None, None]

        # Create test painter
        test_pixmap = QPixmap(1920, 1080)
        test_painter = QPainter(test_pixmap)

        # Render views to trigger grid cache regeneration
        for _ in range(10):
            split_screen._draw_player_view(test_painter, 1, 0, 0, 960, 1080)
            split_screen._draw_player_view(test_painter, 2, 960, 0, 960, 1080)

        test_painter.end()

    # Test actual frame rate in fullscreen
    print("\n3. Measuring actual FPS in fullscreen...")
    frame_times = []
    start_time = time.perf_counter()
    frame_count = 0

    while time.perf_counter() - start_time < 3.0:  # 3 second test
        frame_start = time.perf_counter()

        game_engine.update_game_state()
        split_screen.game_view.update()
        app.processEvents()

        frame_end = time.perf_counter()
        frame_times.append(frame_end - frame_start)
        frame_count += 1

    total_time = time.perf_counter() - start_time
    avg_fps = frame_count / total_time
    avg_frame_time = sum(frame_times) / len(frame_times)
    max_frame_time = max(frame_times)
    min_frame_time = min(frame_times)

    print(f"Fullscreen FPS Test Results:")
    print(f"  Average FPS: {avg_fps:.1f}")
    print(f"  Average frame time: {avg_frame_time*1000:.2f} ms")
    print(f"  Max frame time: {max_frame_time*1000:.2f} ms")
    print(f"  Min frame time: {min_frame_time*1000:.2f} ms")
    print(f"  Total frames: {frame_count}")

    # Get performance mode status
    perf_info = game_engine._get_performance_info()
    print(f"\nGame Engine Performance Status:")
    print(f"  Performance mode active: {perf_info['performance_mode']}")
    print(f"  Current FPS: {perf_info['fps']:.1f}")
    print(f"  Projectile count: {len(game_engine.projectiles)}")
    print(f"  Spatial partitioning cell size: {perf_info.get('cell_size', 'N/A')}")

    # Print final results
    profiler.print_results()

    # Recommendations
    print("\n" + "=" * 80)
    print("PERFORMANCE RECOMMENDATIONS")
    print("=" * 80)

    windowed_update = profiler.timing_data.get("windowed_game_update", 0) / 100
    fullscreen_update = profiler.timing_data.get("fullscreen_game_update", 0) / 100
    windowed_paint = profiler.timing_data.get("windowed_paint_event", 0) / 50
    fullscreen_paint = profiler.timing_data.get("fullscreen_paint_event", 0) / 50

    print(f"Average game update time:")
    print(f"  Windowed: {windowed_update*1000:.2f} ms")
    print(f"  Fullscreen: {fullscreen_update*1000:.2f} ms")
    print(f"  Fullscreen overhead: {((fullscreen_update/windowed_update)-1)*100:.1f}%")

    print(f"\nAverage paint event time:")
    print(f"  Windowed: {windowed_paint*1000:.2f} ms")
    print(f"  Fullscreen: {fullscreen_paint*1000:.2f} ms")
    print(f"  Fullscreen overhead: {((fullscreen_paint/windowed_paint)-1)*100:.1f}%")

    if avg_fps < 45:
        print(f"\n⚠️  CRITICAL: Fullscreen FPS is {avg_fps:.1f}, below target of 45 FPS")
        if fullscreen_paint > 16.67 / 1000:  # > 60 FPS threshold
            print("   → Primary bottleneck appears to be rendering/paint events")
            print("   → Consider reducing render resolution or complexity")
        if fullscreen_update > 16.67 / 1000:
            print("   → Game logic update is taking too long")
            print(
                "   → Consider further reducing projectile limits or physics complexity"
            )

    window.close()
    app.quit()


if __name__ == "__main__":
    test_detailed_performance()
