#!/usr/bin/env python3
"""
Project organization checker.
Ensures all test, debug, and demo scripts are in the tests/ folder.
"""

import os
import sys
from pathlib import Path


def show_organization_reminder():
    """Show a reminder about proper file organization."""
    print("💡 ORGANIZATION REMINDER:")
    print("=" * 50)
    print("📁 ALL test, debug, and demo scripts MUST go in tests/ folder")
    print()
    print("✅ CORRECT locations:")
    print("   tests/test_your_feature.py")
    print("   tests/debug_issue.py")
    print("   tests/demo_something.py")
    print()
    print("❌ WRONG locations:")
    print("   test_your_feature.py      (main directory)")
    print("   debug_issue.py           (main directory)")
    print("   demo_something.py        (main directory)")
    print()
    print("🚀 Quick start: cp tests/template_test.py tests/test_new.py")
    print("📚 See tests/CREATE_NEW_SCRIPT.md for detailed guidance")
    print("🔧 Run this script to check compliance anytime")
    print("=" * 50)
    print()


def check_project_organization():
    """Check if all test/debug/demo files are properly organized."""
    project_root = Path(__file__).parent.parent
    main_dir = project_root
    tests_dir = project_root / "tests"

    print("🔍 Checking project organization...")
    print(f"Project root: {project_root}")
    print(f"Tests directory: {tests_dir}")
    print()

    # Files that should be in tests/ folder
    test_patterns = ["test_*.py", "debug_*.py", "demo_*.py"]

    # Files that should stay in main directory
    core_files = [
        "main.py",
        "config.py",
        "game_engine.py",
        "physics.py",
        "rendering.py",
        "objects.py",
        "split_screen.py",
        "topographical_plane.py",
        "gamepad_manager.py",
        "rate_limiter.py",
        "rate_limiter_ui.py",
        "py-widget.py",
    ]

    misplaced_files = []
    properly_placed = []

    # Check main directory for files that should be in tests/
    for pattern in test_patterns:
        for file_path in main_dir.glob(pattern):
            if file_path.is_file():
                misplaced_files.append(file_path)

    # Check tests directory for properly placed files
    for pattern in test_patterns:
        for file_path in tests_dir.glob(pattern):
            if file_path.is_file():
                properly_placed.append(file_path)

    # Report results
    print("✅ PROPERLY ORGANIZED FILES:")
    if properly_placed:
        for file_path in sorted(properly_placed):
            print(f"   tests/{file_path.name}")
    else:
        print("   (No test/debug/demo files found in tests/)")

    print()
    print("❌ MISPLACED FILES (should be in tests/):")
    if misplaced_files:
        for file_path in sorted(misplaced_files):
            print(f"   {file_path.name} -> should move to tests/{file_path.name}")
    else:
        print("   (No misplaced files found)")

    print()
    print("📋 CORE FILES (correctly in main directory):")
    core_present = []
    for core_file in core_files:
        if (main_dir / core_file).exists():
            core_present.append(core_file)

    if core_present:
        for file_name in sorted(core_present):
            print(f"   {file_name}")

    print()
    if misplaced_files:
        print("🔧 RECOMMENDED ACTIONS:")
        print("Move the following files to tests/ folder:")
        for file_path in misplaced_files:
            print(f"   Move-Item '{file_path.name}' 'tests\\'")
        return False
    else:
        print("🎉 PROJECT ORGANIZATION: PERFECT!")
        print(
            "All test, debug, and demo files are properly organized in tests/ folder."
        )
        return True


def suggest_organization():
    """Suggest how to organize any new files."""
    print("\n📝 ORGANIZATION GUIDELINES:")
    print("For future files, follow these rules:")
    print()
    print("PUT IN tests/ FOLDER:")
    print("  • test_*.py - Testing scripts")
    print("  • debug_*.py - Debugging tools")
    print("  • demo_*.py - Feature demonstrations")
    print("  • Any experimental or prototype code")
    print()
    print("KEEP IN MAIN FOLDER:")
    print("  • main.py - Application entry point")
    print("  • Core game modules (game_engine.py, physics.py, etc.)")
    print("  • Configuration files (config.py)")
    print("  • Production code")
    print()
    print("See tests/ORGANIZATION_GUIDELINES.md for detailed rules.")


if __name__ == "__main__":
    show_organization_reminder()
    organized = check_project_organization()
    suggest_organization()

    if not organized:
        sys.exit(1)  # Exit with error if files need to be moved
    else:
        sys.exit(0)  # Exit successfully if well organized
