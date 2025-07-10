"""
Main entry point for the Topographical Plane application.
Creates a shared game engine and split-screen multi-player setup.
"""

import sys
import math
import pygame  # For sound effects
import os
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPainter, QFont, QColor, QRadialGradient, QBrush, QPen
from PyQt6.QtCore import QRectF
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QByteArray
from game_engine import GameEngine
from split_screen import SplitScreenView
from objects import SVG_RED_SHIP, SVG_BLUE_CUBE
from gamepad_manager import GamepadManager
from config import GAMEPAD_ENABLED


# --- Resource path helper for PyInstaller compatibility ---
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller bundle"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class LaunchScreen(QWidget):
    """Launch screen displaying BOXHOLE title with SVG elements."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("BOXHOLE")
        self.setFixedSize(1200, 800)
        self.setStyleSheet("background-color: black;")

        # Initialize pygame mixer for sound effects (only once, at app start)
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Preload global sound effects

        try:
            self.sfx_enemyalert = pygame.mixer.Sound(
                resource_path("sounds/enemyalert.wav")
            )
        except Exception:
            self.sfx_enemyalert = None
        try:
            self.sfx_landhit = pygame.mixer.Sound(resource_path("sounds/landhit.wav"))
        except Exception:
            self.sfx_landhit = None
        try:
            self.sfx_toggleswitch = pygame.mixer.Sound(
                resource_path("sounds/toggleswitch.wav")
            )
        except Exception:
            self.sfx_toggleswitch = None
        try:
            self.sfx_laserblast = pygame.mixer.Sound(
                resource_path("sounds/laserblast.wav")
            )
        except Exception:
            self.sfx_laserblast = None
        try:
            self.sfx_enemyblock = pygame.mixer.Sound(
                resource_path("sounds/enemyblock.wav")
            )
        except Exception:
            self.sfx_enemyblock = None
        try:
            self.sfx_selfdestruct = pygame.mixer.Sound(
                resource_path("sounds/selfdestruct.wav")
            )
        except Exception:
            self.sfx_selfdestruct = None
        try:
            self.sfx_defaulthit = pygame.mixer.Sound(
                resource_path("sounds/defaulthit.wav")
            )
        except Exception:
            self.sfx_defaulthit = None
        try:
            self.sfx_freeshield = pygame.mixer.Sound(
                resource_path("sounds/freeshield.wav")
            )
        except Exception:
            self.sfx_freeshield = None
        try:
            self.sfx_spaceship = pygame.mixer.Sound(
                resource_path("sounds/spaceship.wav")
            )
        except Exception:
            self.sfx_spaceship = None

        # Provide access to SFX for other modules
        import builtins

        builtins.SFX_ENEMYALERT = self.sfx_enemyalert
        builtins.SFX_LANDHIT = self.sfx_landhit
        builtins.SFX_TOGGLESWITCH = self.sfx_toggleswitch
        builtins.SFX_LASERBLAST = self.sfx_laserblast
        builtins.SFX_ENEMYBLOCK = self.sfx_enemyblock
        builtins.SFX_SELFDESTRUCT = self.sfx_selfdestruct
        builtins.SFX_DEFAULTHIT = self.sfx_defaulthit
        builtins.SFX_FREESHIELD = self.sfx_freeshield
        builtins.SFX_SPACESHIP = self.sfx_spaceship

        # Set up SVG renderers
        self.red_ship_renderer = QSvgRenderer(QByteArray(SVG_RED_SHIP.encode("utf-8")))
        self.blue_cube_renderer = QSvgRenderer(
            QByteArray(SVG_BLUE_CUBE.encode("utf-8"))
        )

        # Set up gamepad manager for input detection
        self.gamepad_manager = GamepadManager() if GAMEPAD_ENABLED else None

        # Enable focus and mouse tracking to capture all input
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(True)

        # Input detection timer
        self.input_timer = QTimer()
        self.input_timer.timeout.connect(self.check_gamepad_input)
        self.input_timer.start(16)  # Check gamepad input at 60fps

    def paintEvent(self, event):
        """Draw the launch screen with title and SVG elements."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()

        # Create black radial gradient background
        gradient = QRadialGradient(width // 2, height // 2, min(width, height) // 2)
        gradient.setColorAt(0.0, QColor(40, 40, 40))  # Dark gray center
        gradient.setColorAt(0.7, QColor(20, 20, 20))  # Darker
        gradient.setColorAt(1.0, QColor(0, 0, 0))  # Pure black at edges

        painter.fillRect(0, 0, width, height, QBrush(gradient))

        # Draw "BOXHOLE" title in big yellow letters with glow effect
        font = QFont("Arial", 72, QFont.Weight.Bold)
        painter.setFont(font)

        title_text = "BOXHOLE"
        font_metrics = painter.fontMetrics()
        text_width = font_metrics.horizontalAdvance(title_text)
        text_height = font_metrics.height()

        # Center the title horizontally, place in upper third
        title_x = (width - text_width) // 2
        title_y = height // 3

        # Draw glow effect (multiple yellow outlines with decreasing opacity)
        for i in range(3, 0, -1):
            glow_alpha = 60 // i  # 20, 30, 60
            painter.setPen(QPen(QColor(255, 255, 0, glow_alpha), i * 2))
            painter.drawText(title_x, title_y, title_text)

        # Draw main title text
        painter.setPen(QPen(QColor(255, 255, 0), 2))
        painter.drawText(title_x, title_y, title_text)

        # Draw red ship SVG (left side)
        ship_size = 120
        ship_x = width // 4 - ship_size // 2
        ship_y = height * 2 // 3 - ship_size // 2

        painter.save()
        painter.translate(ship_x + ship_size // 2, ship_y + ship_size // 2)
        painter.rotate(-30)  # Slight rotation for visual appeal
        ship_rect = QRectF(-ship_size // 2, -ship_size // 2, ship_size, ship_size)
        self.red_ship_renderer.render(painter, ship_rect)
        painter.restore()

        # Draw blue cube SVG (right side)
        cube_size = 100
        cube_x = width * 3 // 4 - cube_size // 2
        cube_y = height * 2 // 3 - cube_size // 2

        painter.save()
        painter.translate(cube_x + cube_size // 2, cube_y + cube_size // 2)
        painter.rotate(15)  # Slight rotation for visual appeal
        cube_rect = QRectF(-cube_size // 2, -cube_size // 2, cube_size, cube_size)
        self.blue_cube_renderer.render(painter, cube_rect)
        painter.restore()

        # Draw "Press any key to start" text
        start_font = QFont("Arial", 24)
        painter.setFont(start_font)
        painter.setPen(QPen(QColor(200, 200, 200), 1))  # Light gray

        start_text = "Press any key to start"
        start_metrics = painter.fontMetrics()
        start_width = start_metrics.horizontalAdvance(start_text)
        start_x = (width - start_width) // 2
        start_y = height - 100

        painter.drawText(start_x, start_y, start_text)

    def keyPressEvent(self, event):
        """Any key press starts the game."""
        self.start_game()

    def mousePressEvent(self, event):
        """Any mouse click starts the game."""
        self.start_game()

    def check_gamepad_input(self):
        """Check for any gamepad input to start the game."""
        if not self.gamepad_manager:
            return

        # Check both gamepads for any button press or stick movement
        for gamepad_index in [0, 1]:
            if self.gamepad_manager.is_gamepad_connected(gamepad_index):
                gamepad_input = self.gamepad_manager.get_gamepad_input(gamepad_index)
                if gamepad_input:
                    # Check if shoot button is pressed
                    if gamepad_input.get("shoot_button", False):
                        self.start_game()
                        return
                    # Check if any stick is moved significantly
                    left_x = gamepad_input.get("left_stick_x", 0.0)
                    left_y = gamepad_input.get("left_stick_y", 0.0)
                    if abs(left_x) > 0.1 or abs(left_y) > 0.1:
                        self.start_game()
                        return

    def start_game(self):
        """Start the actual game and close launch screen."""
        self.input_timer.stop()
        self.hide()
        self.controller.start_actual_game()


class MultiPlayerController:
    """Manages the split-screen multi-player game setup."""

    def __init__(self):
        self.game_engine = GameEngine()
        self.split_screen_window = None
        self.game_timer = None
        self.launch_screen = None

    def start_launch_screen(self):
        """Show the launch screen."""
        self.launch_screen = LaunchScreen(self)
        self.launch_screen.show()
        self.launch_screen.activateWindow()  # Bring to front
        self.launch_screen.raise_()  # Ensure it's on top
        self.launch_screen.setFocus()  # Give it keyboard focus

    def start_actual_game(self):
        """Initialize and start the multi-player game (called from launch screen)."""
        # Create the purple dot for player 2
        self.game_engine.create_purple_dot()

        # Create split-screen window
        self.split_screen_window = SplitScreenView(self.game_engine)
        self.split_screen_window.show()

        # Start the shared game loop
        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self.game_engine.update_game_state)
        self.game_timer.start(16)  # ~60 FPS

    def start_game(self):
        """Legacy method - now just shows launch screen."""
        self.start_launch_screen()


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
