#!/usr/bin/env python3
"""
Build script for BOXHOLE executable packaging.
Creates a standalone executable that can be distributed to other computers.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def clean_build():
    """Clean previous build artifacts."""
    print("🧹 Cleaning previous builds...")
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}/")

    # Remove .spec files
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"   Removed {spec_file}")


def create_executable():
    """Create the executable using PyInstaller."""
    print("📦 Building BOXHOLE executable...")

    # PyInstaller command with optimal settings
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window (GUI only)
        "--name",
        "BOXHOLE",  # Executable name
        "--icon",
        "bluecube.ico",  # Blue cube icon file
        "--add-data",
        "tests;tests",  # Include tests folder
        "--exclude-module",
        "tkinter",  # Exclude unused modules
        "--exclude-module",
        "matplotlib",
        "--exclude-module",
        "PIL",
        "--exclude-module",
        "numpy",  # Exclude if not needed
        "--hidden-import",
        "pygame",  # Ensure pygame is included
        "--collect-all",
        "pygame",  # Include all pygame components
        "--clean",  # Clean cache
        "main.py",  # Entry point
    ]

    # Remove icon option if icon file doesn't exist
    if not os.path.exists("bluecube.ico"):
        cmd.remove("--icon")
        cmd.remove("bluecube.ico")
        print("   ⚠️  No bluecube.ico found, building without icon")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("   ✅ Build successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Build failed: {e}")
        print(f"   Error output: {e.stderr}")
        return False


def create_installer_info():
    """Create installation instructions."""
    info_content = """
# BOXHOLE - Installation Instructions

## System Requirements
- Windows 10/11 (64-bit)
- 300MB free disk space (includes PyQt6 and pygame)
- DirectX compatible graphics card (for best performance)
- Xbox/compatible controllers for gamepad support (optional)

## Installation
1. Download BOXHOLE.exe
2. Run the executable - no installation required!
3. The game will start with the launch screen

## Controls
- Player 1 (Red): Arrow Keys + Enter
- Player 2 (Purple): WASD + Left Ctrl
- Gamepad support: Xbox controllers automatically detected

## Features
- Split-screen multiplayer
- Black holes with massive gravity fields
- Physics-based projectiles and collisions
- Powerup system for balanced gameplay
- 60 FPS performance optimization

## Troubleshooting
- If antivirus flags the executable, add it to exceptions
- For performance issues, try running as administrator
- Contact support if you encounter any problems

Enjoy BOXHOLE!
"""

    with open("dist/INSTALLATION.txt", "w") as f:
        f.write(info_content)
    print("   📄 Created installation instructions")


def main():
    """Main build process."""
    print("🎮 BOXHOLE Build Process")
    print("=" * 40)

    # Check if PyInstaller is installed
    try:
        subprocess.run(["pyinstaller", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ PyInstaller not found. Install with: pip install pyinstaller")
        return

    # Build process
    clean_build()

    if create_executable():
        create_installer_info()

        # Show results
        print("\n🎉 Build Complete!")
        print("=" * 40)
        print(f"📁 Executable location: dist/BOXHOLE.exe")

        if os.path.exists("dist/BOXHOLE.exe"):
            size_mb = os.path.getsize("dist/BOXHOLE.exe") / (1024 * 1024)
            print(f"📊 File size: {size_mb:.1f} MB")

        print("\n📋 Distribution Files:")
        print("   • BOXHOLE.exe - Main executable")
        print("   • INSTALLATION.txt - Setup instructions")

        print("\n🚀 Ready for distribution!")
        print("   Copy the dist/ folder contents to distribute your game.")
    else:
        print("\n❌ Build failed. Check error messages above.")


if __name__ == "__main__":
    main()
