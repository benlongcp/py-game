"""
Main widget class for the Topographical Plane application.
Handles the main game loop, input, and coordinates all the components.
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt, QTimer
from config import *
from objects import RedDot, BlueSquare
from rendering import Renderer


class TopographicalPlane(QWidget):
    """Main widget that orchestrates the topographical plane simulation."""

    def __init__(self):
        super().__init__()
        self._setup_window()
        self._create_objects()
        self._setup_input()
        self._setup_timer()

    def _setup_window(self):
        """Initialize window properties."""
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowTitle("Topographical Plane View")
        self.setStyleSheet("background-color: white;")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def _create_objects(self):
        """Create game objects."""
        self.red_dot = RedDot()
        self.blue_square = BlueSquare()
        self.projectiles = []  # List to hold active projectiles

    def _setup_input(self):
        """Initialize input handling."""
        self.keys_pressed = set()

    def _setup_timer(self):
        """Setup the main game loop timer."""
        self.movement_timer = QTimer()
        self.movement_timer.timeout.connect(self.update_game_state)
        self.movement_timer.start(FRAME_TIME_MS)

    def paintEvent(self, event):
        """Handle painting of all visual elements."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Get camera position (follows red dot)
        camera_x = self.red_dot.virtual_x
        camera_y = self.red_dot.virtual_y  # Draw all elements in order
        Renderer.draw_triangular_grid(painter, camera_x, camera_y)
        Renderer.draw_vignette_gradient(painter, camera_x, camera_y)
        Renderer.draw_blue_square(painter, self.blue_square, camera_x, camera_y)
        Renderer.draw_projectiles(painter, self.projectiles, camera_x, camera_y)
        Renderer.draw_red_dot(painter, self.red_dot)

    def update_game_state(self):
        """Main game loop - updates physics and triggers repaint."""
        self._handle_input()
        self._update_physics()
        self._handle_collisions()
        self.update()  # Trigger repaint

    def _handle_input(self):
        """Process current input state and update red dot acceleration."""
        self.red_dot.acceleration_x = 0.0
        self.red_dot.acceleration_y = 0.0

        if Qt.Key.Key_Left in self.keys_pressed:
            self.red_dot.acceleration_x = -ACCELERATION
        if Qt.Key.Key_Right in self.keys_pressed:
            self.red_dot.acceleration_x = ACCELERATION
        if Qt.Key.Key_Up in self.keys_pressed:
            self.red_dot.acceleration_y = -ACCELERATION
        if Qt.Key.Key_Down in self.keys_pressed:
            self.red_dot.acceleration_y = ACCELERATION

    def _update_physics(self):
        """Update physics for all objects."""
        self.red_dot.update_physics()
        self.blue_square.update_physics()

        # Update projectile physics
        for projectile in self.projectiles[
            :
        ]:  # Use slice copy to safely modify during iteration
            projectile.update_physics()
            if not projectile.is_active:
                self.projectiles.remove(projectile)

    def _handle_collisions(self):
        """Check and resolve collisions between objects."""
        self.blue_square.check_collision_with_dot(self.red_dot)

        # Handle projectile collisions with blue square and red dot
        for projectile in self.projectiles:
            if projectile.is_active:
                projectile.check_collision_with_square(self.blue_square)
                projectile.check_collision_with_dot(self.red_dot)

    def _shoot_projectile(self):
        """Create and add a new projectile if possible."""
        # Limit the number of projectiles on screen
        if len(self.projectiles) >= PROJECTILE_MAX_COUNT:
            return

        new_projectile = self.red_dot.shoot_projectile()
        if new_projectile:
            self.projectiles.append(new_projectile)

    def keyPressEvent(self, event):
        """Handle key press events."""
        # Handle space bar for shooting (only on press, not hold)
        if event.key() == Qt.Key.Key_Space:
            self._shoot_projectile()
        else:
            # Add other keys to the set for continuous input
            self.keys_pressed.add(event.key())
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        """Handle key release events."""
        self.keys_pressed.discard(event.key())
        super().keyReleaseEvent(event)
