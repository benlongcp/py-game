"""
Main widget class for the Topographical Plane application.
Handles rendering and input for a single player view.
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor
from PyQt6.QtCore import Qt, QTimer
from config import *
from game_engine import GameEngine
from rendering import Renderer


class TopographicalPlane(QWidget):
    """Main widget that displays the topographical plane simulation for one player."""

    def __init__(
        self, game_engine, player_number=1, window_title="Topographical Plane View"
    ):
        super().__init__()
        self.game_engine = game_engine
        self.player_number = player_number  # 1 for red dot, 2 for purple dot
        self.window_title = window_title
        self._setup_window()
        self._setup_input()
        self._setup_timer()

    def _setup_window(self):
        """Initialize window properties."""
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowTitle(self.window_title)
        self.setStyleSheet("background-color: white;")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def _setup_input(self):
        """Initialize input handling."""
        # Input is now handled through the game engine
        pass

    def _setup_timer(self):
        """Setup the rendering timer."""
        self.render_timer = QTimer()
        self.render_timer.timeout.connect(self.update)  # Just trigger repaint
        self.render_timer.start(FRAME_TIME_MS)

    def paintEvent(self, event):
        """Handle painting of all visual elements."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Get camera position based on which player this window is following
        if self.player_number == 1:
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
        Renderer.draw_static_circles(
            painter, camera_x, camera_y, self.width(), self.height(), self.game_engine
        )
        Renderer.draw_gravitational_dots(painter, camera_x, camera_y)

        # Draw the black hole
        Renderer.draw_black_hole(
            painter,
            self.game_engine.black_hole,
            camera_x,
            camera_y,
            self.width(),
            self.height(),
        )

        Renderer.draw_blue_square(
            painter, self.game_engine.blue_square, camera_x, camera_y
        )
        Renderer.draw_projectiles(
            painter, self.game_engine.projectiles, camera_x, camera_y
        )

        # Draw the dot this window is following at center
        if self.player_number == 1:
            Renderer.draw_red_dot(painter, self.game_engine.red_dot)
        else:
            Renderer.draw_red_dot(
                painter, following_dot
            )  # Still use red dot renderer for center

        # Draw the other player's dot in world coordinates if it exists
        if self.player_number == 1 and self.game_engine.purple_dot is not None:
            Renderer.draw_purple_dot(
                painter, self.game_engine.purple_dot, camera_x, camera_y
            )
        elif self.player_number == 2 and self.game_engine.red_dot != following_dot:
            # Draw red dot in world coordinates when viewing from purple dot
            screen_x = self.game_engine.red_dot.virtual_x - (camera_x - WINDOW_CENTER_X)
            screen_y = self.game_engine.red_dot.virtual_y - (camera_y - WINDOW_CENTER_Y)

            if (
                screen_x + self.game_engine.red_dot.radius >= 0
                and screen_x - self.game_engine.red_dot.radius <= WINDOW_WIDTH
                and screen_y + self.game_engine.red_dot.radius >= 0
                and screen_y - self.game_engine.red_dot.radius <= WINDOW_HEIGHT
            ):

                painter.setPen(QPen(QColor(*DOT_COLOR), 2))
                painter.setBrush(QBrush(QColor(*DOT_COLOR)))
                painter.drawEllipse(
                    int(screen_x - self.game_engine.red_dot.radius),
                    int(screen_y - self.game_engine.red_dot.radius),
                    self.game_engine.red_dot.radius * 2,
                    self.game_engine.red_dot.radius * 2,
                )

        # Draw off-screen indicator for blue square if it's not visible
        Renderer.draw_off_screen_indicator(
            painter, self.game_engine.blue_square, camera_x, camera_y
        )

    def keyPressEvent(self, event):
        """Handle key press events."""
        key = event.key()

        if self.player_number == 1:
            # Player 1 controls (Arrow keys + Enter)
            if key in [
                Qt.Key.Key_Left,
                Qt.Key.Key_Right,
                Qt.Key.Key_Up,
                Qt.Key.Key_Down,
            ]:
                self.game_engine.set_player1_key(key, True)
            elif key == Qt.Key.Key_Return:  # Enter key
                self.game_engine.shoot_projectile_player1()
        else:
            # Player 2 controls (WASD + Left Ctrl)
            if key in [Qt.Key.Key_A, Qt.Key.Key_D, Qt.Key.Key_W, Qt.Key.Key_S]:
                self.game_engine.set_player2_key(key, True)
            elif key == Qt.Key.Key_Control:  # Left Ctrl
                self.game_engine.shoot_projectile_player2()

    def keyReleaseEvent(self, event):
        """Handle key release events."""
        key = event.key()

        if self.player_number == 1:
            # Player 1 controls
            if key in [
                Qt.Key.Key_Left,
                Qt.Key.Key_Right,
                Qt.Key.Key_Up,
                Qt.Key.Key_Down,
            ]:
                self.game_engine.set_player1_key(key, False)
        else:
            # Player 2 controls
            if key in [Qt.Key.Key_A, Qt.Key.Key_D, Qt.Key.Key_W, Qt.Key.Key_S]:
                self.game_engine.set_player2_key(key, False)
