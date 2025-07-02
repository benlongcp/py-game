"""
Split-screen widget for dual-player topographical plane game.
Displays two views side-by-side in a single window.
Supports both keyboard and gamepad input.
"""

import time
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QPixmap
from PyQt6.QtCore import Qt, QTimer
from config import *
from game_engine import GameEngine
from rendering import Renderer
from gamepad_manager import GamepadManager
from rate_limiter_ui import RateLimiterUI, StatusDisplay


class SplitScreenView(QWidget):
    """Single window with two side-by-side player views."""

    def _init_game_over_state(self):
        self.game_over = False
        self.game_over_winner = None  # 1 or 2
        self._flash_timer = 0
        self._flash_on = False

    def _start_game_over(self, winner):
        self.game_over = True
        self.game_over_winner = winner
        self._flash_timer = 0
        self._flash_on = False
        self._show_game_over_dialog()

    def _show_game_over_dialog(self):
        from PyQt6.QtWidgets import QMessageBox

        winner = "Player 1 (Red)" if self.game_over_winner == 1 else "Player 2 (Purple)"
        loser = "Player 2 (Purple)" if self.game_over_winner == 1 else "Player 1 (Red)"
        msg = QMessageBox(self)
        msg.setWindowTitle("Game Over")
        msg.setText(f"{winner} wins!\n\n{loser} loses.\n\nReset the game?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes)
        msg.setDefaultButton(QMessageBox.StandardButton.Yes)
        msg.setModal(True)
        ret = msg.exec()
        if ret == QMessageBox.StandardButton.Yes:
            self._reset_game()

    def _reset_game(self):
        self.game_engine.reset_game_state()
        self._init_game_over_state()
        self.update()

    def __init__(self, game_engine):
        super().__init__()
        self.game_engine = game_engine

        # Initialize gamepad manager
        self.gamepad_manager = GamepadManager()

        # Set gamepad manager reference in game engine
        self.game_engine.set_gamepad_manager(self.gamepad_manager)

        # FPS tracking
        self.fps_counter = 0
        self.fps_display = 0.0
        self.last_fps_time = time.time()

        self._setup_window()
        self._setup_timer()
        self._setup_gamepad_timer()
        self._init_game_over_state()

    def _init_grid_cache(self):
        """Initialize the grid cache for both player views."""
        self._grid_cache = [None, None]  # One for each player view
        self._grid_cache_params = [
            None,
            None,
        ]  # Store (camera_x, camera_y, width, height, spacing)

    def _setup_window(self):
        """Initialize window properties."""
        # Enable dynamic resizing with minimum size constraints
        min_width = (WINDOW_WIDTH * 2) + 20  # +20 for divider
        min_height = WINDOW_HEIGHT
        self.setMinimumSize(min_width, min_height)
        self.resize(min_width, min_height)  # Initial size, but resizable

        self.setWindowTitle("Multi-Player Topographical Plane - Split Screen")
        self.setStyleSheet("background-color: black;")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Initialize grid cache
        self._init_grid_cache()

    def _setup_timer(self):
        """Setup the rendering timer."""
        self.render_timer = QTimer()
        self.render_timer.timeout.connect(self.update)  # Just trigger repaint
        self.render_timer.start(FRAME_TIME_MS)

    def _setup_gamepad_timer(self):
        """Setup the gamepad input timer."""
        # Note: We no longer use a separate gamepad timer
        # Gamepad input is now handled directly in the game engine's update cycle
        pass

    def update_gamepad_input(self):
        """Update gamepad input each frame."""
        # Note: Gamepad input is now handled directly in the game engine's _handle_input() method
        # This method is kept for backward compatibility but does nothing
        pass

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Update FPS counter
        self._update_fps()

        # Calculate dynamic view dimensions
        window_width = self.width()
        window_height = self.height()
        divider_width = 20
        view_width = (window_width - divider_width) // 2
        view_height = window_height

        # --- Game Over Check ---
        if not self.game_over:
            red_score = self.game_engine.get_red_player_score()
            purple_score = self.game_engine.get_purple_player_score()
            if red_score >= 3:
                self._start_game_over(1)
            elif purple_score >= 3:
                self._start_game_over(2)
        # --- Flashing Effect ---
        flash_color1 = None
        flash_color2 = None
        if self.game_over:
            self._flash_timer += 1
            if self._flash_timer % 20 == 0:
                self._flash_on = not self._flash_on
            if self._flash_on:
                if self.game_over_winner == 1:
                    flash_color1 = QColor(0, 255, 0, 120)  # Green overlay
                    flash_color2 = QColor(255, 0, 0, 120)  # Red overlay
                else:
                    flash_color1 = QColor(255, 0, 0, 120)
                    flash_color2 = QColor(0, 255, 0, 120)

        # Draw Player 2 view (left side - Purple)
        self._draw_player_view(
            painter, 2, 0, 0, view_width, view_height, overlay_color=flash_color2
        )

        # Draw divider line
        painter.setPen(QPen(QColor(100, 100, 100), 3))
        divider_x = view_width + divider_width // 2
        painter.drawLine(divider_x, 0, divider_x, view_height)

        # Draw Player 1 view (right side - Red)
        self._draw_player_view(
            painter,
            1,
            view_width + divider_width,
            0,
            view_width,
            view_height,
            overlay_color=flash_color1,
        )

        # Draw FPS counter overlay at bottom of window (if enabled)
        if SHOW_FPS_COUNTER:
            self._draw_fps_counter(painter)

    def _draw_player_view(
        self,
        painter,
        player_number,
        x_offset,
        y_offset,
        width,
        height,
        overlay_color=None,
    ):
        """Draw a single player's view."""
        # Set clipping rectangle for this view
        painter.save()
        painter.setClipRect(x_offset, y_offset, width, height)

        # Calculate view center for this player's view
        view_center_x = width / 2
        view_center_y = height / 2
        view_width = width
        view_height = height

        # Get camera position and following_dot based on which player this view is following
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
                camera_x = self.game_engine.red_dot.virtual_x
                camera_y = self.game_engine.red_dot.virtual_y
                following_dot = self.game_engine.red_dot

        # --- Grid Caching ---
        # Always check and update the grid cache for each player view
        grid_spacing = Renderer.get_adaptive_grid_spacing(view_width, view_height)
        cache_idx = 0 if player_number == 2 else 1
        cache_params = (camera_x, camera_y, width, height, grid_spacing)
        cache = self._grid_cache[cache_idx]
        params = self._grid_cache_params[cache_idx]
        needs_redraw = cache is None or params is None or params != cache_params
        if needs_redraw:
            print(f"Redrawing grid for player {player_number} (cache_idx={cache_idx})")
            grid_pixmap = QPixmap(width, height)
            grid_pixmap.fill(QColor(0, 0, 0))  # Fill with black
            grid_painter = QPainter(grid_pixmap)
            Renderer.draw_triangular_grid(
                grid_painter, camera_x, camera_y, view_center_x, view_center_y
            )
            grid_painter.end()
            self._grid_cache[cache_idx] = grid_pixmap
            self._grid_cache_params[cache_idx] = cache_params
        # Translate painter to the view's coordinate system
        painter.translate(x_offset, y_offset)
        # Blit grid pixmap at (0,0) in local view coordinates
        painter.drawPixmap(0, 0, self._grid_cache[cache_idx])
        # --- End Grid Caching ---

        # Draw vignette and all other elements as before (no change)
        Renderer.draw_vignette_gradient(
            painter, camera_x, camera_y, view_center_x, view_center_y
        )
        Renderer.draw_static_circles(painter, camera_x, camera_y, width, height)
        Renderer.draw_gravitational_dots(painter, camera_x, camera_y, width, height)
        Renderer.draw_blue_square(
            painter, self.game_engine.blue_square, camera_x, camera_y, width, height
        )
        Renderer.draw_projectiles(
            painter, self.game_engine.projectiles, camera_x, camera_y, width, height
        )

        # Draw the dot this view is following at center
        if player_number == 1:
            Renderer.draw_red_dot(
                painter, self.game_engine.red_dot, view_center_x, view_center_y
            )
        else:
            # For player 2 view, draw purple dot at center in purple color
            Renderer.draw_purple_dot_centered(
                painter, following_dot, view_center_x, view_center_y
            )

        # Draw the other player's dot in world coordinates if it exists
        if player_number == 1 and self.game_engine.purple_dot is not None:
            Renderer.draw_purple_dot(
                painter,
                self.game_engine.purple_dot,
                camera_x,
                camera_y,
                view_center_x,
                view_center_y,
            )
        elif player_number == 2:
            # Draw red dot in world coordinates when viewing from purple dot
            Renderer.draw_red_dot_world(
                painter,
                self.game_engine.red_dot,
                camera_x,
                camera_y,
                view_center_x,
                view_center_y,
            )

        # Draw off-screen indicator for blue square if it's not visible
        Renderer.draw_off_screen_indicator(
            painter, self.game_engine.blue_square, camera_x, camera_y, width, height
        )

        # Draw player labels
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        if player_number == 1:
            if GAMEPAD_ENABLED and self.gamepad_manager.is_gamepad_connected(
                GAMEPAD_1_INDEX
            ):
                painter.drawText(10, 25, "Player 1 (Red) - Gamepad 1")
            else:
                painter.drawText(10, 25, "Player 1 (Red) - Arrow Keys + Enter")
        else:
            if GAMEPAD_ENABLED and self.gamepad_manager.is_gamepad_connected(
                GAMEPAD_2_INDEX
            ):
                painter.drawText(10, 25, "Player 2 (Purple) - Gamepad 2")
            else:
                painter.drawText(10, 25, "Player 2 (Purple) - WASD + Ctrl")

        # Draw status display (score, hit points, and rate limiters)
        red_score = self.game_engine.get_red_player_score()
        purple_score = self.game_engine.get_purple_player_score()
        red_hp = self.game_engine.get_red_player_hp()
        purple_hp = self.game_engine.get_purple_player_hp()

        # Get rate limiter progress for both players
        player1_rate_data = self.game_engine.get_player1_rate_limiter_progress()
        player2_rate_data = self.game_engine.get_player2_rate_limiter_progress()

        # Draw status display - each player sees only their own info
        if player_number == 1:
            # Player 1 view - show only Player 1 status
            StatusDisplay.draw_player_status(
                painter, 10, 50, "Player 1", red_hp, red_score, player1_rate_data
            )
        else:
            # Player 2 view - show only Player 2 status
            StatusDisplay.draw_player_status(
                painter, 10, 50, "Player 2", purple_hp, purple_score, player2_rate_data
            )

        # Also draw the original status display for compatibility
        Renderer.draw_status_display(
            painter, red_score, purple_score, red_hp, purple_hp, width, height
        )

        # --- Overlay for Game Over Flashing ---
        if overlay_color is not None:
            painter.setBrush(QBrush(overlay_color))
            painter.setPen(QPen(overlay_color))
            painter.drawRect(0, 0, width, height)
        painter.restore()

    def keyPressEvent(self, event):
        """Handle key press events for both players (fallback when gamepad not connected)."""
        key = event.key()

        # Player 1 controls (Arrow keys + Enter) - only if gamepad 1 is not connected
        if not (
            GAMEPAD_ENABLED
            and self.gamepad_manager.is_gamepad_connected(GAMEPAD_1_INDEX)
        ):
            if key in [
                Qt.Key.Key_Left,
                Qt.Key.Key_Right,
                Qt.Key.Key_Up,
                Qt.Key.Key_Down,
            ]:
                self.game_engine.set_player1_key(key, True)
            elif key == Qt.Key.Key_Return:  # Enter key
                self.game_engine.shoot_projectile_player1()

        # Player 2 controls (WASD + Left Ctrl) - only if gamepad 2 is not connected
        if not (
            GAMEPAD_ENABLED
            and self.gamepad_manager.is_gamepad_connected(GAMEPAD_2_INDEX)
        ):
            if key in [Qt.Key.Key_A, Qt.Key.Key_D, Qt.Key.Key_W, Qt.Key.Key_S]:
                self.game_engine.set_player2_key(key, True)
            elif key == Qt.Key.Key_Control:  # Left Ctrl
                self.game_engine.shoot_projectile_player2()

    def keyReleaseEvent(self, event):
        """Handle key release events for both players (fallback when gamepad not connected)."""
        key = event.key()

        # Player 1 controls - only if gamepad 1 is not connected
        if not (
            GAMEPAD_ENABLED
            and self.gamepad_manager.is_gamepad_connected(GAMEPAD_1_INDEX)
        ):
            if key in [
                Qt.Key.Key_Left,
                Qt.Key.Key_Right,
                Qt.Key.Key_Up,
                Qt.Key.Key_Down,
            ]:
                self.game_engine.set_player1_key(key, False)

        # Player 2 controls - only if gamepad 2 is not connected
        if not (
            GAMEPAD_ENABLED
            and self.gamepad_manager.is_gamepad_connected(GAMEPAD_2_INDEX)
        ):
            if key in [Qt.Key.Key_A, Qt.Key.Key_D, Qt.Key.Key_W, Qt.Key.Key_S]:
                self.game_engine.set_player2_key(key, False)

    def _update_fps(self):
        """Update FPS counter."""
        self.fps_counter += 1
        current_time = time.time()

        # Update FPS display every second
        if current_time - self.last_fps_time >= 1.0:
            self.fps_display = self.fps_counter / (current_time - self.last_fps_time)
            self.fps_counter = 0
            self.last_fps_time = current_time

    def _draw_fps_counter(self, painter):
        """Draw FPS counter overlay at the bottom of the window."""
        painter.save()

        # Reset clipping to draw on the full window
        painter.setClipping(False)

        # Set up colors from config
        background_color = QColor(*FPS_COUNTER_BACKGROUND)
        text_color = QColor(*FPS_COUNTER_COLOR)

        # Set font
        font = QFont("Arial", 12, QFont.Weight.Bold)
        painter.setFont(font)

        # Calculate text metrics
        fps_text = f"FPS: {self.fps_display:.1f}"
        font_metrics = painter.fontMetrics()
        text_width = font_metrics.horizontalAdvance(fps_text)
        text_height = font_metrics.height()

        # Position at bottom center
        window_width = self.width()
        window_height = self.height()
        x = (window_width - text_width) // 2
        y = window_height - text_height - 10  # 10px from bottom

        # Draw background rectangle
        padding = 8
        painter.setBrush(QBrush(background_color))
        painter.setPen(QPen(QColor(0, 0, 0, 0)))  # No border
        painter.drawRoundedRect(
            x - padding,
            y - padding,
            text_width + 2 * padding,
            text_height + 2 * padding,
            5,
            5,  # Rounded corners
        )

        # Draw text
        painter.setPen(QPen(text_color))
        painter.drawText(x, y + font_metrics.ascent(), fps_text)

        painter.restore()
