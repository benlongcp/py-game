#!/usr/bin/env python3
"""
Targeted performance test to identify specific lag sources.
"""

import sys
import os
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from game_engine import GameEngine
from split_screen import SplitScreenView
from config import *


def test_performance_scenarios():
    """Test different scenarios that might cause lag."""
    print("🎯 Testing Performance Scenarios")
    print("=" * 40)

    app = QApplication(sys.argv)

    # Test 1: Basic setup
    print("\n1️⃣ Testing basic game setup...")
    game_engine = GameEngine()
    game_engine.create_purple_dot()
    split_screen = SplitScreenView(game_engine)

    # Measure FPS for baseline
    baseline_fps = measure_fps(split_screen, game_engine, 3, "Baseline")

    # Test 2: Many projectiles
    print("\n2️⃣ Testing with many projectiles...")
    for i in range(15):  # Spawn near max projectiles
        game_engine.shoot_projectile_player1()
        if i % 2 == 0:
            game_engine.shoot_projectile_player2()

    projectile_fps = measure_fps(split_screen, game_engine, 3, "Many Projectiles")

    # Test 3: Window resizing impact (if dynamic scaling is working)
    print("\n3️⃣ Testing window resize impact...")
    original_size = split_screen.size()
    if hasattr(split_screen, "resize"):
        split_screen.resize(2400, 1200)  # 50% larger
        resize_fps = measure_fps(split_screen, game_engine, 3, "Large Window")
        split_screen.resize(original_size.width(), original_size.height())
    else:
        resize_fps = baseline_fps
        print("   Window is fixed size")

    # Test 4: Fast movement
    print("\n4️⃣ Testing with fast movement...")
    game_engine.red_dot.velocity_x = MAX_SPEED * 0.8
    game_engine.red_dot.velocity_y = MAX_SPEED * 0.8
    if game_engine.purple_dot:
        game_engine.purple_dot.velocity_x = -MAX_SPEED * 0.8
        game_engine.purple_dot.velocity_y = -MAX_SPEED * 0.8

    movement_fps = measure_fps(split_screen, game_engine, 3, "Fast Movement")

    # Results summary
    print("\n📊 PERFORMANCE COMPARISON")
    print("=" * 40)
    print(f"Baseline:        {baseline_fps:.1f} FPS")
    print(f"Many Projectiles: {projectile_fps:.1f} FPS")
    print(f"Large Window:    {resize_fps:.1f} FPS")
    print(f"Fast Movement:   {movement_fps:.1f} FPS")

    # Identify issues
    issues = []
    if projectile_fps < baseline_fps * 0.9:
        issues.append("🚀 Projectile rendering/physics causing lag")
    if resize_fps < baseline_fps * 0.9:
        issues.append("🖼️ Large window size causing lag")
    if movement_fps < baseline_fps * 0.9:
        issues.append("🏃 Fast movement causing lag")

    if issues:
        print("\n⚠️ PERFORMANCE ISSUES DETECTED:")
        for issue in issues:
            print(f"   • {issue}")
        print("\n🔧 RECOMMENDED FIXES:")
        suggest_fixes(baseline_fps, projectile_fps, resize_fps, movement_fps)
    else:
        print("\n✅ No significant performance issues detected")

    app.quit()


def measure_fps(split_screen, game_engine, duration_seconds, test_name):
    """Measure FPS for a specific duration."""
    print(f"   Measuring {test_name} for {duration_seconds} seconds...")

    frame_count = 0
    start_time = time.time()
    last_fps_time = start_time

    split_screen.show()

    # Process events for the duration
    while time.time() - start_time < duration_seconds:
        # Update game state
        game_engine.update_game_state()

        # Trigger repaint
        split_screen.update()

        # Process Qt events
        QApplication.processEvents()

        frame_count += 1

        # Small delay to prevent 100% CPU usage
        time.sleep(0.001)

    elapsed = time.time() - start_time
    fps = frame_count / elapsed

    print(f"   {test_name}: {fps:.1f} FPS ({frame_count} frames in {elapsed:.1f}s)")
    return fps


def suggest_fixes(baseline, projectiles, resize, movement):
    """Suggest specific fixes based on performance results."""

    if projectiles < baseline * 0.9:
        print("   🚀 Projectile Performance:")
        print("      - Reduce PROJECTILE_MAX_COUNT in config.py")
        print("      - Implement projectile pooling")
        print("      - Optimize collision detection")

    if resize < baseline * 0.9:
        print("   🖼️ Window Size Performance:")
        print("      - Check if dynamic scaling is properly implemented")
        print("      - Consider fixed internal resolution with scaling")
        print("      - Optimize grid dot culling for large windows")

    if movement < baseline * 0.9:
        print("   🏃 Movement Performance:")
        print("      - Check grid dot generation efficiency")
        print("      - Optimize camera calculations")
        print("      - Consider reducing GRID_RADIUS for better performance")

    # General optimizations
    print("   ⚙️ General Optimizations:")
    print("      - Disable FPS counter (set SHOW_FPS_COUNTER = False)")
    print("      - Increase FRAME_TIME_MS to 20 (50 FPS target)")
    print("      - Reduce grid detail (increase GRID_SPACING)")
    print("      - Check for unnecessary repaints")


def check_configuration_issues():
    """Check for configuration that might cause performance issues."""
    print("\n🔍 CONFIGURATION ANALYSIS")
    print("=" * 40)

    issues = []
    warnings = []

    # Check grid settings
    grid_area = math.pi * GRID_RADIUS**2
    dots_per_row = GRID_RADIUS * 2 / GRID_SPACING
    estimated_dots = (dots_per_row**2) * 0.7  # Approximate for triangular pattern

    if estimated_dots > 10000:
        issues.append(f"🔴 Too many grid dots (~{estimated_dots:.0f})")
    elif estimated_dots > 5000:
        warnings.append(f"🟡 Many grid dots (~{estimated_dots:.0f})")

    # Check frame timing
    if FRAME_TIME_MS < 16:
        warnings.append(f"🟡 Very high target FPS ({1000/FRAME_TIME_MS:.0f})")

    # Check projectile settings
    if PROJECTILE_MAX_COUNT > 15:
        warnings.append(f"🟡 High projectile limit ({PROJECTILE_MAX_COUNT})")

    # Check window size
    total_window_area = (WINDOW_WIDTH * 2 + 20) * WINDOW_HEIGHT
    if total_window_area > 2000000:  # 2M pixels
        warnings.append(
            f"🟡 Large window size ({WINDOW_WIDTH * 2 + 20}x{WINDOW_HEIGHT})"
        )

    if issues:
        print("CRITICAL ISSUES:")
        for issue in issues:
            print(f"   {issue}")

    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"   {warning}")

    if not issues and not warnings:
        print("✅ Configuration looks reasonable for performance")

    print(f"\nCurrent Settings:")
    print(f"   Grid: {GRID_RADIUS}px radius, {GRID_SPACING}px spacing")
    print(f"   Target: {1000/FRAME_TIME_MS:.0f} FPS ({FRAME_TIME_MS}ms per frame)")
    print(f"   Window: {WINDOW_WIDTH * 2 + 20}x{WINDOW_HEIGHT}")
    print(f"   Projectiles: {PROJECTILE_MAX_COUNT} max")


if __name__ == "__main__":
    import math

    check_configuration_issues()
    test_performance_scenarios()
