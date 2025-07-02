#!/usr/bin/env python3
"""
Performance optimization script that adjusts config settings for better FPS.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config


def apply_performance_optimizations():
    """Apply performance optimizations to the configuration."""
    print("🚀 Applying Performance Optimizations...")
    print("=" * 50)

    original_settings = {}
    optimizations = []

    # 1. Reduce projectile count
    if config.PROJECTILE_MAX_COUNT > 10:
        original_settings["PROJECTILE_MAX_COUNT"] = config.PROJECTILE_MAX_COUNT
        config.PROJECTILE_MAX_COUNT = 10
        optimizations.append(
            f"Reduced projectile limit: {original_settings['PROJECTILE_MAX_COUNT']} → {config.PROJECTILE_MAX_COUNT}"
        )

    # 2. Increase grid spacing (fewer dots)
    if config.GRID_SPACING < 40:
        original_settings["GRID_SPACING"] = config.GRID_SPACING
        config.GRID_SPACING = 40
        optimizations.append(
            f"Increased grid spacing: {original_settings['GRID_SPACING']} → {config.GRID_SPACING}"
        )

    # 3. Reduce grid radius
    if config.GRID_RADIUS > 800:
        original_settings["GRID_RADIUS"] = config.GRID_RADIUS
        config.GRID_RADIUS = 800
        optimizations.append(
            f"Reduced grid radius: {original_settings['GRID_RADIUS']} → {config.GRID_RADIUS}"
        )

    # 4. Adjust frame timing for stable 50 FPS instead of 60
    if config.FRAME_TIME_MS < 20:
        original_settings["FRAME_TIME_MS"] = config.FRAME_TIME_MS
        original_settings["FPS"] = config.FPS
        config.FRAME_TIME_MS = 20
        config.FPS = 50
        optimizations.append(
            f"Reduced target FPS: {original_settings['FPS']} → {config.FPS} ({original_settings['FRAME_TIME_MS']}ms → {config.FRAME_TIME_MS}ms)"
        )

    # 5. Disable FPS counter during gameplay (can add overhead)
    if config.SHOW_FPS_COUNTER:
        original_settings["SHOW_FPS_COUNTER"] = config.SHOW_FPS_COUNTER
        config.SHOW_FPS_COUNTER = False
        optimizations.append("Disabled FPS counter overlay for better performance")

    if optimizations:
        print("Applied optimizations:")
        for opt in optimizations:
            print(f"  ✅ {opt}")
        print("\n📊 Performance impact estimate: +10-20% FPS improvement")
        print("🎮 Gameplay should feel smoother now")
    else:
        print("✅ Configuration is already optimized for performance")

    return original_settings


def restore_original_settings(original_settings):
    """Restore original configuration settings."""
    print("\n🔄 Restoring original settings...")
    for setting, value in original_settings.items():
        setattr(config, setting, value)
        print(f"  Restored {setting} = {value}")


def test_optimized_performance():
    """Test performance with optimizations applied."""
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import QTimer
    from game_engine import GameEngine
    from split_screen import SplitScreenView
    import time

    print("\n🎯 Testing optimized performance...")

    app = QApplication(sys.argv)

    # Create game
    game_engine = GameEngine()
    game_engine.create_purple_dot()
    split_screen = SplitScreenView(game_engine)

    # Add some projectiles for stress test
    for i in range(5):
        game_engine.shoot_projectile_player1()
        if i % 2 == 0:
            game_engine.shoot_projectile_player2()

    # Measure performance
    frame_count = 0
    start_time = time.time()
    test_duration = 5

    split_screen.show()

    while time.time() - start_time < test_duration:
        game_engine.update_game_state()
        split_screen.update()
        QApplication.processEvents()
        frame_count += 1
        time.sleep(0.001)  # Small delay

    elapsed = time.time() - start_time
    fps = frame_count / elapsed

    print(f"📈 Optimized performance: {fps:.1f} FPS")
    print(f"📊 Target: {config.FPS} FPS")

    if fps >= config.FPS * 0.95:
        print("✅ Performance target achieved!")
    else:
        print("⚠️ Still below target - may need additional optimizations")

    app.quit()
    return fps


def create_performance_config():
    """Create a separate high-performance config file."""
    performance_config = """# High-Performance Configuration
# This configuration prioritizes smooth gameplay over visual quality

# Reduced grid for better performance
GRID_SPACING = 40  # Fewer grid dots
GRID_RADIUS = 800  # Smaller visible area
GRID_DOT_RADIUS = 1  # Smaller dots

# Lower target FPS for stable performance
FPS = 50
FRAME_TIME_MS = 20

# Reduced projectile count
PROJECTILE_MAX_COUNT = 10

# Disable performance overhead features
SHOW_FPS_COUNTER = False

# Other optimizations
# Consider disabling vignette gradient if still experiencing lag
# Consider reducing WINDOW_WIDTH/HEIGHT for smaller render area
"""

    config_path = "config_performance.py"
    with open(config_path, "w") as f:
        f.write(performance_config)

    print(f"📁 Created performance config: {config_path}")
    print("💡 To use: rename to config.py or copy settings manually")


if __name__ == "__main__":
    print("🎯 Performance Optimization Tool")
    print("=" * 40)
    print("This tool will optimize the game configuration for better performance")
    print("\nOptions:")
    print("1. Apply temporary optimizations and test")
    print("2. Create performance config file")
    print("3. Just show current performance bottlenecks")

    choice = input("\nEnter choice (1, 2, or 3): ").strip()

    if choice == "1":
        original = apply_performance_optimizations()
        if original:
            test_optimized_performance()
            restore_original_settings(original)
        else:
            print("No optimizations needed - testing current performance...")
            test_optimized_performance()

    elif choice == "2":
        create_performance_config()

    else:
        # Analyze current config
        import math

        print("\n🔍 CURRENT PERFORMANCE ANALYSIS")
        print("=" * 40)

        # Calculate grid complexity
        dots_per_row = config.GRID_RADIUS * 2 / config.GRID_SPACING
        estimated_dots = (dots_per_row**2) * 0.7

        print(f"Grid complexity: ~{estimated_dots:.0f} dots")
        print(f"Target FPS: {config.FPS} ({config.FRAME_TIME_MS}ms per frame)")
        print(f"Max projectiles: {config.PROJECTILE_MAX_COUNT}")
        print(f"Window size: {config.WINDOW_WIDTH * 2 + 20}x{config.WINDOW_HEIGHT}")
        print(f"FPS counter: {'Enabled' if config.SHOW_FPS_COUNTER else 'Disabled'}")

        if estimated_dots > 3000:
            print("\n⚠️ Grid may be too complex for smooth 60 FPS")
        if config.PROJECTILE_MAX_COUNT > 15:
            print("⚠️ High projectile count may cause lag")
        if config.FRAME_TIME_MS < 17:
            print("⚠️ Very high FPS target may be difficult to maintain")
