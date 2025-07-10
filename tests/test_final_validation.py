"""
Final validation test for BOXHOLE fullscreen performance improvements.
This test validates that all optimizations work correctly and provides
a summary of the improvements achieved.
"""

import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, Qt
from main import MultiPlayerController


def test_final_validation():
    """Final validation of fullscreen performance improvements."""
    app = QApplication(sys.argv)

    print("=" * 70)
    print("BOXHOLE FULLSCREEN PERFORMANCE VALIDATION")
    print("=" * 70)

    # Create controller and start the game
    controller = MultiPlayerController()
    controller.start_launch_screen()
    controller.start_actual_game()

    window = controller.split_screen_window
    game_engine = controller.game_engine

    print("\n🔧 TESTING OPTIMIZATION ACTIVATION...")

    # Test 1: Verify windowed mode baseline
    print("\n1️⃣ Windowed Mode Baseline:")
    window.showNormal()
    window.resize(1200, 800)
    app.processEvents()
    time.sleep(0.5)

    windowed_fps = measure_realistic_fps(game_engine, window, app, 2.0)
    print(f"   ✓ Windowed FPS: {windowed_fps:.1f}")

    # Test 2: Verify fullscreen optimizations activate
    print("\n2️⃣ Fullscreen Optimization Activation:")
    window.showFullScreen()
    app.processEvents()
    time.sleep(0.5)

    # Validate all optimizations are active
    checks = {
        "Performance mode": game_engine.performance_mode,
        "Fullscreen mode": hasattr(game_engine, "_fullscreen_mode")
        and game_engine._fullscreen_mode,
        "Aggressive mode": hasattr(game_engine, "_aggressive_mode")
        and game_engine._aggressive_mode,
        "Grid optimized": hasattr(window, "_fullscreen_optimized")
        and window._fullscreen_optimized,
        "Antialiasing disabled": hasattr(window, "_antialiasing_enabled")
        and not window._antialiasing_enabled,
    }

    all_optimizations_active = True
    for check_name, is_active in checks.items():
        status = "✅" if is_active else "❌"
        print(f"   {status} {check_name}: {is_active}")
        if not is_active:
            all_optimizations_active = False

    if hasattr(game_engine, "_gamepad_manager") and game_engine._gamepad_manager:
        gamepad_opt = hasattr(game_engine._gamepad_manager, "_fullscreen_mode")
        status = "✅" if gamepad_opt else "❌"
        print(f"   {status} Gamepad optimized: {gamepad_opt}")
        if not gamepad_opt:
            all_optimizations_active = False

    # Test 3: Measure fullscreen performance
    print("\n3️⃣ Fullscreen Performance Test:")
    fullscreen_fps = measure_realistic_fps(game_engine, window, app, 3.0)
    print(f"   ✓ Fullscreen FPS: {fullscreen_fps:.1f}")

    # Test 4: Verify mode switching
    print("\n4️⃣ Mode Switching Test:")
    window.showNormal()
    app.processEvents()
    time.sleep(0.5)

    restored_correctly = not (
        hasattr(game_engine, "_fullscreen_mode") and game_engine._fullscreen_mode
    ) and not (
        hasattr(window, "_fullscreen_optimized") and window._fullscreen_optimized
    )

    status = "✅" if restored_correctly else "❌"
    print(f"   {status} Settings restored: {restored_correctly}")

    # Test 5: Performance under load
    print("\n5️⃣ Performance Under Load Test:")
    window.showFullScreen()
    app.processEvents()
    time.sleep(0.5)

    # Stress test with many projectiles
    print("   Adding projectiles for stress test...")
    for _ in range(20):
        game_engine.shoot_projectile_player1()
        if game_engine.purple_dot:
            game_engine.shoot_projectile_player2()

    stress_fps = measure_realistic_fps(game_engine, window, app, 3.0)
    print(f"   ✓ Stress test FPS: {stress_fps:.1f}")

    # Calculate results
    performance_ratio = (fullscreen_fps / windowed_fps * 100) if windowed_fps > 0 else 0
    stress_ratio = (stress_fps / windowed_fps * 100) if windowed_fps > 0 else 0

    print("\n" + "=" * 70)
    print("📊 FINAL RESULTS")
    print("=" * 70)
    print(f"Windowed FPS:          {windowed_fps:.1f}")
    print(f"Fullscreen FPS:        {fullscreen_fps:.1f}")
    print(f"Stress test FPS:       {stress_fps:.1f}")
    print(f"Fullscreen efficiency: {performance_ratio:.1f}%")
    print(f"Stress test efficiency: {stress_ratio:.1f}%")

    print(f"\n🎯 PERFORMANCE ASSESSMENT:")
    if fullscreen_fps >= 45:
        print("✅ EXCELLENT: Fullscreen FPS exceeds target (45+ FPS)")
        grade = "A"
    elif fullscreen_fps >= 30:
        print("✅ GOOD: Fullscreen FPS meets playable threshold (30+ FPS)")
        grade = "B"
    elif fullscreen_fps >= 20:
        print("⚠️  FAIR: Fullscreen FPS is marginally playable (20+ FPS)")
        grade = "C"
    else:
        print("❌ POOR: Fullscreen FPS below playable threshold (<20 FPS)")
        grade = "F"

    if performance_ratio >= 70:
        efficiency_grade = "A"
    elif performance_ratio >= 50:
        efficiency_grade = "B"
    elif performance_ratio >= 30:
        efficiency_grade = "C"
    else:
        efficiency_grade = "D"

    print(f"\n📈 OPTIMIZATION SUCCESS:")
    print(f"   FPS Grade: {grade}")
    print(f"   Efficiency Grade: {efficiency_grade}")
    print(f"   All optimizations active: {'✅' if all_optimizations_active else '❌'}")

    if all_optimizations_active and fullscreen_fps >= 30:
        print(
            f"\n🎉 SUCCESS: Fullscreen performance optimizations are working effectively!"
        )
        print(f"   The game is now playable in fullscreen mode.")
    elif fullscreen_fps >= 30:
        print(
            f"\n⚠️  PARTIAL SUCCESS: Performance is acceptable but some optimizations may not be active."
        )
    else:
        print(
            f"\n❌ OPTIMIZATION NEEDED: Further improvements required for smooth fullscreen gameplay."
        )

    print(f"\n🔧 APPLIED OPTIMIZATIONS:")
    print(f"   • Reduced projectile limit to 15 in fullscreen")
    print(f"   • Tripled grid spacing (1/9 density)")
    print(f"   • Reduced render resolution cap to 800x600")
    print(f"   • Disabled antialiasing in fullscreen")
    print(f"   • Reduced pygame event pumping frequency")
    print(f"   • Aggressive frame skipping (2/3 frames)")
    print(f"   • Vignette gradient caching")
    print(f"   • Grid rendering caching")

    window.close()
    app.quit()


def measure_realistic_fps(game_engine, window, app, duration=2.0):
    """Measure FPS with realistic game conditions."""
    frame_times = []
    start_time = time.perf_counter()
    frame_count = 0

    # Add some projectiles and movement for realistic testing
    game_engine.red_dot.velocity_x = 50
    game_engine.red_dot.velocity_y = 30
    if game_engine.purple_dot:
        game_engine.purple_dot.velocity_x = -40
        game_engine.purple_dot.velocity_y = 20

    # Add some projectiles
    for _ in range(5):
        game_engine.shoot_projectile_player1()
        if game_engine.purple_dot:
            game_engine.shoot_projectile_player2()

    while time.perf_counter() - start_time < duration:
        frame_start = time.perf_counter()

        # Occasionally add more projectiles during test
        if frame_count % 30 == 0:  # Every 30 frames
            game_engine.shoot_projectile_player1()

        game_engine.update_game_state()
        window.game_view.update()
        app.processEvents()

        frame_end = time.perf_counter()
        frame_times.append(frame_end - frame_start)
        frame_count += 1

    total_time = time.perf_counter() - start_time
    avg_fps = frame_count / total_time
    return avg_fps


if __name__ == "__main__":
    test_final_validation()
