"""
Split-screen widget for dual-player topographical plane game.
Displays two views side-by-side in a single window.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor
from PyQt6.QtCore import Qt, QTimer
from config import *
from game_engine import GameEngine
from rendering import Renderer


class SplitScreenView(QWidget):
    """Single window with two side-by-side player views."""

    def __init__(self, game_engine):
        super().__init__()
        self.game_engine = game_engine
        self._setup_window()
        self._setup_timer()

    def _setup_window(self):
        """Initialize window properties."""
        # Make window twice as wide to fit both views
        self.setFixedSize(WINDOW_WIDTH * 2 + 20, WINDOW_HEIGHT)  # +20 for divider
        self.setWindowTitle("Multi-Player Topographical Plane - Split Screen")
        self.setStyleSheet("background-color: white;")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def _setup_timer(self):
        """Setup the rendering timer."""
        self.render_timer = QTimer()
        self.render_timer.timeout.connect(self.update)  # Just trigger repaint
        self.render_timer.start(FRAME_TIME_MS)

    def paintEvent(self, event):
        """Handle painting of both player views."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw Player 2 view (left side - Purple)
        self._draw_player_view(painter, 2, 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Draw divider line
        painter.setPen(QPen(QColor(100, 100, 100), 3))
        painter.drawLine(WINDOW_WIDTH, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Draw Player 1 view (right side - Red)
        self._draw_player_view(
            painter, 1, WINDOW_WIDTH + 20, 0, WINDOW_WIDTH, WINDOW_HEIGHT
        )

    def _draw_player_view(
        self, painter, player_number, x_offset, y_offset, width, height
    ):
        """Draw a single player's view."""
        # Set clipping rectangle for this view
        painter.save()
        painter.setClipRect(x_offset, y_offset, width, height)

        # Translate painter to the view's coordinate system
        painter.translate(x_offset, y_offset)

        # Get camera position based on which player this view is following
        if player_number == 1:
            camera_x = self.game_engine.red_dot.virtual_x
            camera_y = self.game_engine.red_dot.virtual_y
            following_dot = self.game_engine.red_dot
        else:
            if self.game_engine.purple_dot is not None:
                camera_x = self.game_engine.purple_dot.virtual_x
                camera_y = self.game_engine.purple_dot.virtual_y
                following_dot = self.game_engine.purple_dot
            else:
                # Fallback to red dot if purple doesn't exist yet
                camera_x = self.game_engine.red_dot.virtual_x
                camera_y = self.game_engine.red_dot.virtual_y
                following_dot = self.game_engine.red_dot

        # Draw all elements in order
        Renderer.draw_triangular_grid(painter, camera_x, camera_y)
        Renderer.draw_vignette_gradient(painter, camera_x, camera_y)
        Renderer.draw_static_circles(painter, camera_x, camera_y)
        Renderer.draw_gravitational_dots(painter, camera_x, camera_y)
        Renderer.draw_blue_square(
            painter, self.game_engine.blue_square, camera_x, camera_y
        )
        Renderer.draw_projectiles(
            painter, self.game_engine.projectiles, camera_x, camera_y
        )

        # Draw the dot this view is following at center
        if player_number == 1:
            Renderer.draw_red_dot(painter, self.game_engine.red_dot)
        else:
            # For player 2 view, draw purple dot at center in purple color
            Renderer.draw_purple_dot_centered(painter, following_dot)

        # Draw the other player's dot in world coordinates if it exists
        if player_number == 1 and self.game_engine.purple_dot is not None:
            Renderer.draw_purple_dot(
                painter, self.game_engine.purple_dot, camera_x, camera_y
            )
        elif player_number == 2:
            # Draw red dot in world coordinates when viewing from purple dot
            Renderer.draw_red_dot_world(
                painter, self.game_engine.red_dot, camera_x, camera_y
            )

        # Draw off-screen indicator for blue square if it's not visible
        Renderer.draw_off_screen_indicator(
            painter, self.game_engine.blue_square, camera_x, camera_y, width, height
        )

        # Draw player labels
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        if player_number == 1:
            painter.drawText(10, 25, "Player 1 (Red) - Arrow Keys + Enter")
        else:
            painter.drawText(10, 25, "Player 2 (Purple) - WASD + Ctrl")

        # Draw status display (score and hit points)
        red_score = self.game_engine.get_red_player_score()
        purple_score = self.game_engine.get_purple_player_score()
        red_hp = self.game_engine.get_red_player_hp()
        purple_hp = self.game_engine.get_purple_player_hp()
        Renderer.draw_status_display(
            painter, red_score, purple_score, red_hp, purple_hp, width, height
        )

        painter.restore()

    def keyPressEvent(self, event):
        """Handle key press events for both players."""
        key = event.key()

        # Player 1 controls (Arrow keys + Enter)
        if key in [Qt.Key.Key_Left, Qt.Key.Key_Right, Qt.Key.Key_Up, Qt.Key.Key_Down]:
            self.game_engine.set_player1_key(key, True)
        elif key == Qt.Key.Key_Return:  # Enter key
            self.game_engine.shoot_projectile_player1()

        # Player 2 controls (WASD + Left Ctrl)
        elif key in [Qt.Key.Key_A, Qt.Key.Key_D, Qt.Key.Key_W, Qt.Key.Key_S]:
            self.game_engine.set_player2_key(key, True)
        elif key == Qt.Key.Key_Control:  # Left Ctrl
            self.game_engine.shoot_projectile_player2()

    def keyReleaseEvent(self, event):
        """Handle key release events for both players."""
        key = event.key()

        # Player 1 controls
        if key in [Qt.Key.Key_Left, Qt.Key.Key_Right, Qt.Key.Key_Up, Qt.Key.Key_Down]:
            self.game_engine.set_player1_key(key, False)

        # Player 2 controls
        elif key in [Qt.Key.Key_A, Qt.Key.Key_D, Qt.Key.Key_W, Qt.Key.Key_S]:
            self.game_engine.set_player2_key(key, False)
