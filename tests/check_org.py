#!/usr/bin/env python3
"""
Quick organization checker - verifies all test/debug/demo files are in tests/ folder.
This is a convenience script that calls the main organization checker.
"""

import subprocess
import sys
import os


def main():
    """Run the main organization checker."""
    print("🔍 Quick Organization Check")
    print("=" * 40)

    # Check if tests directory exists
    if not os.path.exists("tests"):
        print("❌ ERROR: tests/ directory not found!")
        print("   Run this script from the project root directory.")
        return 1

    # Check if the main organization checker exists
    checker_path = os.path.join("tests", "check_organization.py")
    if not os.path.exists(checker_path):
        print("❌ ERROR: tests/check_organization.py not found!")
        return 1

    # Run the main organization checker
    try:
        result = subprocess.run(
            [sys.executable, checker_path], capture_output=False, text=True
        )
        return result.returncode
    except Exception as e:
        print(f"❌ ERROR running organization checker: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
