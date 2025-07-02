#!/usr/bin/env python3
"""
Simple dynamic scaling demonstration.
Shows a resizable split-screen game window.
"""

import sys
from PyQt6.QtWidgets import QApplication
from split_screen import SplitScreenView
from game_engine import GameEngine
from PyQt6.QtCore import QTimer


def main():
    """Run a simple dynamic scaling demo."""
    app = QApplication(sys.argv)
    
    print("Dynamic Scaling Demo")
    print("===================")
    print("• Window is now resizable!")
    print("• Drag corners/edges to resize")
    print("• Try maximizing the window")
    print("• Game content scales automatically")
    print("• Both player views remain proportional")
    print()
    print("Controls:")
    print("Player 1 (Red, right side): Arrow Keys + Enter")
    print("Player 2 (Purple, left side): WASD + Ctrl")
    
    # Create game engine and view
    game_engine = GameEngine()
    game_engine.create_purple_dot()
    
    # Create split screen view
    split_screen = SplitScreenView(game_engine)
    split_screen.show()
    
    # Start game loop
    game_timer = QTimer()
    game_timer.timeout.connect(game_engine.update_game_state)
    game_timer.start(16)  # ~60 FPS
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
