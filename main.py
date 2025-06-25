"""
Main entry point for the Topographical - Move: Arrow keys
- Shoot: Enterane application.
Creates a shared game engine and split-screen multi-player setup.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer
from game_engine import GameEngine
from split_screen import SplitScreenView


class MultiPlayerController:
    """Manages the split-screen multi-player game setup."""

    def __init__(self):
        self.game_engine = GameEngine()
        self.split_screen_window = None
        self.game_timer = None

    def start_game(self):
        """Initialize and start the multi-player game."""
        # Create the purple dot for player 2
        self.game_engine.create_purple_dot()

        # Create split-screen window
        self.split_screen_window = SplitScreenView(self.game_engine)
        self.split_screen_window.show()

        # Start the shared game loop
        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self.game_engine.update_game_state)
        self.game_timer.start(16)  # ~60 FPS

        # Show instructions
        self.show_instructions()

    def show_instructions(self):
        """Show game instructions to the user."""
        instructions = """
Split-Screen Multi-Player Topographical Plane Game

CONTROLS:
Player 1 (Red Dot - Left Screen):
- Move: Arrow Keys
- Shoot: Spacebar

Player 2 (Purple Dot - Right Screen):  
- Move: WASD Keys
- Shoot: Left Ctrl

GAMEPLAY:
- Left screen follows the red dot
- Right screen follows the purple dot
- All objects interact with each other
- Hit the blue square to make it move and spin
- Players can collide with each other
- Projectiles affect all objects

Both players can play simultaneously on the same keyboard!

Have fun!
        """

        msg = QMessageBox()
        msg.setWindowTitle("Split-Screen Game Instructions")
        msg.setText(instructions)
        msg.exec()


def main():
    """Create and run the application."""
    # Create QApplication instance
    app = QApplication(sys.argv)

    # Create and start the multi-player controller
    controller = MultiPlayerController()
    controller.start_game()

    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
