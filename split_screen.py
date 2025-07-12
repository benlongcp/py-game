"""
Split-screen widget for dual-player topographical plane game.
Displays two views side-by-side in a single window.
Supports both keyboard and gamepad input.
"""

import time
import random
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QPixmap, QFontMetrics
from PyQt6.QtCore import Qt, QTimer
from config import *
from game_engine import GameEngine
from rendering import Renderer
from gamepad_manager import GamepadManager
from rate_limiter_ui import RateLimiterUI, StatusDisplay
from powerup_view import PowerupSelectionView


class GameView(QWidget):
    """Widget for the main split-screen game view."""

    def __init__(self, split_screen_parent):
        super().__init__()
        self.split_screen = split_screen_parent

        # Set focus policy to receive keyboard events
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def paintEvent(self, event):
        """Paint the split-screen game view."""
        self.split_screen._paint_game_view(self, event)

    def keyPressEvent(self, event):
        """Forward key events to split screen."""
        self.split_screen.keyPressEvent(event)

    def keyReleaseEvent(self, event):
        """Forward key events to split screen."""
        self.split_screen.keyReleaseEvent(event)


class SplitScreenView(QWidget):
    """Single window with two side-by-side player views."""

    def _init_game_over_state(self):
        self.game_over = False
        self.game_over_winner = None  # 1 or 2
        self._flash_timer = 0
        self._flash_on = False
        self._powerup_delay_timer = 0  # Timer for delaying powerup view
        self._powerup_delay_duration = 90  # 1.5 seconds at 60 FPS
        self._powerup_view_shown = False  # Track if powerup view has been shown
        if not hasattr(self, "points_to_win"):
            self.points_to_win = 3

    def _start_game_over(self, winner):
        self.game_over = True
        self.game_over_winner = winner
        self._flash_timer = 0
        self._flash_on = False
        self._powerup_delay_timer = 0  # Start the delay timer
        self._powerup_view_shown = False  # Reset the flag
        # Don't show powerup view immediately - wait for delay

    def _show_powerup_selection_view(self):
        """Show the powerup selection view instead of a dialog."""
        loser_num = 2 if self.game_over_winner == 1 else 1
        self.powerup_view.setup_round_end(self.game_over_winner, loser_num)
        # Switch to powerup selection view
        self.stacked_widget.setCurrentWidget(self.powerup_view)

    def _on_powerup_selected(self, powerup_key, should_reset):
        """Handle powerup selection from the powerup view."""
        if should_reset:
            # Reset the entire game
            self._reset_game()
        else:
            # Apply the selected powerup
            loser_num = 2 if self.game_over_winner == 1 else 1
            if loser_num == 1:
                self.game_engine.player1_powerups.append(powerup_key)
            else:
                self.game_engine.player2_powerups.append(powerup_key)

            # Play powerup selection sound effect
            try:
                import builtins

                if hasattr(builtins, "SFX_TOGGLESWITCH") and builtins.SFX_TOGGLESWITCH:
                    builtins.SFX_TOGGLESWITCH.play()
            except Exception:
                pass

            # Continue the game
            self._continue_game()

        # Switch back to game view
        self.stacked_widget.setCurrentWidget(self.game_view)

    def _continue_game(self):
        self.points_to_win = 3  # Each round is always to 3 points
        self.game_engine.reset_positions_only()
        # Reset both player scores to 0 for the new round
        self.game_engine.red_player_score = 0
        self.game_engine.purple_player_score = 0
        self._init_game_over_state()
        self.game_view.update()

    def _reset_game(self):
        self.game_engine.reset_game_state()
        self.points_to_win = 3  # Reset win points to 3
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

        self._setup_stacked_widget()
        self._setup_window()
        self._setup_timer()
        self._setup_gamepad_timer()
        self._init_game_over_state()

    def _setup_stacked_widget(self):
        """Setup the stacked widget for switching between game view and powerup view."""
        # Create stacked widget
        self.stacked_widget = QStackedWidget()

        # Create game view
        self.game_view = GameView(self)

        # Create powerup selection view
        self.powerup_view = PowerupSelectionView()
        self.powerup_view.powerup_selected.connect(self._on_powerup_selected)

        # Add widgets to stack
        self.stacked_widget.addWidget(self.game_view)
        self.stacked_widget.addWidget(self.powerup_view)

        # Set initial view to game view
        self.stacked_widget.setCurrentWidget(self.game_view)

        # Set layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

    def _init_grid_cache(self):
        """Initialize the grid cache for both player views."""
        self._grid_cache = [None, None]  # One for each player view
        self._grid_cache_params = [
            None,
            None,
        ]  # Store (camera_x, camera_y, width, height, spacing)

    def _setup_window(self):
        """Initialize window properties."""
        # Enable dynamic resizing with smaller minimum size constraints
        min_width = 800  # Reduced from (WINDOW_WIDTH * 2) + 20
        min_height = 400  # Reduced from WINDOW_HEIGHT
        self.setMinimumSize(min_width, min_height)

        # Set initial size but allow resizing
        initial_width = (WINDOW_WIDTH * 2) + 20  # +20 for divider
        initial_height = WINDOW_HEIGHT
        self.resize(initial_width, initial_height)

        self.setWindowTitle("Multi-Player Topographical Plane - Split Screen")
        self.setStyleSheet("background-color: black;")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Initialize grid cache
        self._init_grid_cache()  # Initialize fullscreen tracking
        self._is_fullscreen = False

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
        """Handle paint events for the stacked widget."""
        # Let the stacked widget handle its own painting
        super().paintEvent(event)

    def _draw_fps_counter_bottom_center(self, painter):
        """Draw FPS counter at the horizontal center of the window at the very bottom."""
        painter.save()
        try:
            # Reset clipping to draw on the full window
            painter.setClipping(False)

            # Set up colors from config
            text_color = QColor(*FPS_COUNTER_COLOR)

            # Set font
            font = QFont("Arial", 12, QFont.Weight.Bold)
            painter.setFont(font)

            # Calculate text metrics
            fps_text = f"FPS: {self.fps_display:.1f}"
            font_metrics = painter.fontMetrics()
            text_width = font_metrics.horizontalAdvance(fps_text)

            # Position at left side, at the very bottom
            window_width = self.width()
            window_height = self.height()

            # Left-justify with margin from left edge
            x = 10  # 10px margin from left edge
            y = window_height - 8  # 8px margin from bottom edge

            # Draw text
            painter.setPen(QPen(text_color))
            painter.drawText(x, y, fps_text)
        finally:
            painter.restore()

    def _draw_fps_counter_centered_bottom(self, painter):
        """Draw FPS counter in a dedicated row at the bottom, centered between split screens."""
        painter.save()
        try:
            # Reset clipping to draw on the full window
            painter.setClipping(False)

            # Set up colors from config
            row_background = QColor(*FPS_COUNTER_BACKGROUND)
            text_color = QColor(*FPS_COUNTER_COLOR)

            # Set font
            font = QFont("Arial", 14, QFont.Weight.Bold)
            painter.setFont(font)

            # Calculate text metrics
            fps_text = f"FPS: {self.fps_display:.1f}"
            font_metrics = painter.fontMetrics()
            text_width = font_metrics.horizontalAdvance(fps_text)
            text_height = font_metrics.height()

            # Define row height
            row_height = max(36, text_height + 10)
            window_width = self.width()
            window_height = self.height()

            divider_width = 20
            row_y = window_height - row_height

            # Draw full-width background row
            painter.setBrush(QBrush(row_background))
            painter.setPen(QPen(QColor(0, 0, 0, 0)))  # No border
            painter.drawRect(0, row_y, window_width, row_height)

            # Draw FPS text centered in the full container (window)
            center_x = window_width // 2
            x = center_x - text_width // 2
            # Properly center text vertically in the row
            y = row_y + row_height // 2 + text_height // 2 - font_metrics.descent()
            painter.setPen(QPen(text_color))
            painter.drawText(x, y, fps_text)
        finally:
            painter.restore()

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
        """Draw a single player's view, with optional resolution capping and scaling."""
        from config import ENABLE_RESOLUTION_CAP, MAX_RENDER_WIDTH, MAX_RENDER_HEIGHT
        from PyQt6.QtGui import QPixmap

        # Determine render target size
        render_width = min(width, MAX_RENDER_WIDTH) if ENABLE_RESOLUTION_CAP else width
        render_height = (
            min(height, MAX_RENDER_HEIGHT) if ENABLE_RESOLUTION_CAP else height
        )

        # Create offscreen pixmap for capped rendering
        render_pixmap = QPixmap(render_width, render_height)
        render_pixmap.fill(QColor(0, 0, 0))
        render_painter = QPainter(render_pixmap)

        # Control antialiasing based on performance mode
        if hasattr(self, "_antialiasing_enabled") and not self._antialiasing_enabled:
            # Disable antialiasing for fullscreen performance
            render_painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        else:
            render_painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Calculate view center for this player's view (in render target coordinates)
        view_center_x = render_width / 2
        view_center_y = render_height / 2
        view_width = render_width
        view_height = render_height

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

        # --- Grid Caching (per render size) ---
        grid_spacing = Renderer.get_adaptive_grid_spacing(view_width, view_height)
        cache_idx = 0 if player_number == 2 else 1
        cache_params = (camera_x, camera_y, render_width, render_height, grid_spacing)
        cache = self._grid_cache[cache_idx]
        params = self._grid_cache_params[cache_idx]
        needs_redraw = cache is None or params is None or params != cache_params
        if needs_redraw:
            grid_pixmap = QPixmap(render_width, render_height)
            grid_pixmap.fill(QColor(0, 0, 0))
            grid_painter = QPainter(grid_pixmap)
            Renderer.draw_triangular_grid(
                grid_painter, camera_x, camera_y, view_center_x, view_center_y
            )
            grid_painter.end()
            self._grid_cache[cache_idx] = grid_pixmap
            self._grid_cache_params[cache_idx] = cache_params
        render_painter.drawPixmap(0, 0, self._grid_cache[cache_idx])
        # --- End Grid Caching ---

        # Draw vignette and all other elements as before (no change)
        Renderer.draw_vignette_gradient(
            render_painter, camera_x, camera_y, view_center_x, view_center_y
        )
        Renderer.draw_static_circles(
            render_painter,
            camera_x,
            camera_y,
            render_width,
            render_height,
            self.game_engine,
        )
        Renderer.draw_gravitational_dots(
            render_painter, camera_x, camera_y, render_width, render_height
        )

        # Draw the black hole
        Renderer.draw_black_hole(
            render_painter,
            self.game_engine.black_hole,
            camera_x,
            camera_y,
            render_width,
            render_height,
        )

        Renderer.draw_blue_square(
            render_painter,
            self.game_engine.blue_square,
            camera_x,
            camera_y,
            render_width,
            render_height,
        )
        Renderer.draw_projectiles(
            render_painter,
            self.game_engine.projectile_pool.get_active_projectiles(),
            camera_x,
            camera_y,
            render_width,
            render_height,
        )

        # Draw the dot this view is following at center
        if player_number == 1:
            Renderer.draw_red_dot(
                render_painter, self.game_engine.red_dot, view_center_x, view_center_y
            )
        else:
            Renderer.draw_purple_dot_centered(
                render_painter,
                self.game_engine.purple_dot,
                view_center_x,
                view_center_y,
            )

        # Draw the other player's dot in world coordinates if it exists
        if player_number == 1 and self.game_engine.purple_dot is not None:
            Renderer.draw_purple_dot(
                render_painter,
                self.game_engine.purple_dot,
                camera_x,
                camera_y,
                view_center_x,
                view_center_y,
            )
        elif player_number == 2:
            Renderer.draw_red_dot_world(
                render_painter,
                self.game_engine.red_dot,
                camera_x,
                camera_y,
                view_center_x,
                view_center_y,
            )

        # Draw off-screen indicator for blue square if it's not visible
        Renderer.draw_off_screen_indicator(
            render_painter,
            self.game_engine.blue_square,
            camera_x,
            camera_y,
            render_width,
            render_height,
        )

        # Draw player labels
        render_painter.setPen(QPen(QColor(0, 0, 0), 2))
        if player_number == 1:
            if GAMEPAD_ENABLED and self.gamepad_manager.is_gamepad_connected(
                GAMEPAD_1_INDEX
            ):
                render_painter.drawText(10, 25, "Player 1 (Red) - Gamepad 1")
            else:
                render_painter.drawText(10, 25, "Player 1 (Red) - Arrow Keys + Enter")
        else:
            if GAMEPAD_ENABLED and self.gamepad_manager.is_gamepad_connected(
                GAMEPAD_2_INDEX
            ):
                render_painter.drawText(10, 25, "Player 2 (Purple) - Gamepad 2")
            else:
                render_painter.drawText(10, 25, "Player 2 (Purple) - WASD + Ctrl")

        # Draw status display (score, hit points, and rate limiters)
        red_score = self.game_engine.get_red_player_score()
        purple_score = self.game_engine.get_purple_player_score()
        red_hp = self.game_engine.get_red_player_hp()
        purple_hp = self.game_engine.get_purple_player_hp()

        player1_rate_data = self.game_engine.get_player1_rate_limiter_progress()
        player2_rate_data = self.game_engine.get_player2_rate_limiter_progress()

        POWERUP_MARGIN = 24
        status_block_y = 50
        powerup_column_y = status_block_y + 60 + POWERUP_MARGIN
        if player_number == 1:
            StatusDisplay.draw_player_status(
                render_painter,
                10,
                status_block_y,
                "Player 1",
                red_hp,
                red_score,
                player1_rate_data,
                self.points_to_win,
            )
            self._draw_powerup_status_column(
                render_painter, player_number, 10, powerup_column_y
            )
        else:
            StatusDisplay.draw_player_status(
                render_painter,
                10,
                status_block_y,
                "Player 2",
                purple_hp,
                purple_score,
                player2_rate_data,
                self.points_to_win,
            )
            self._draw_powerup_status_column(
                render_painter, player_number, 10, powerup_column_y
            )

        # Draw overlay color if needed (score pulse/flash)
        if overlay_color:
            render_painter.setPen(QPen(overlay_color, 0))
            render_painter.setBrush(QBrush(overlay_color))
            render_painter.drawRect(0, 0, render_width, render_height)

        render_painter.end()

        # Now scale/blit the rendered pixmap to the actual player view area
        painter.save()
        painter.setClipRect(x_offset, y_offset, width, height)
        painter.drawPixmap(x_offset, y_offset, width, height, render_pixmap)
        painter.restore()

    # Powerup status row at bottom removed. Now shown under status column.
    def _draw_powerup_status_column(self, painter, player_number, x, y):
        """Draws the powerup summary for the given player as a vertical column under their status block."""
        painter.save()
        try:
            painter.setFont(QFont("Arial", 10, QFont.Weight.Normal))
            fm = painter.fontMetrics()
            if player_number == 1:
                powerups = self.game_engine.player1_powerups
            else:
                powerups = self.game_engine.player2_powerups
            summary = self._summarize_powerups(powerups) if powerups else []
            col_x = x + 70
            # Increase the vertical margin between the shots counter and the powerup status column
            # Old: col_y = y
            col_y = y + 24  # Increase margin (was 0, now 24px)
            line_height = fm.height() + 2
            if summary:
                painter.setPen(QPen(QColor(255, 215, 0)))
                for idx, item in enumerate(summary):
                    painter.drawText(col_x, col_y + idx * line_height, item)
            else:
                painter.setPen(QPen(QColor(180, 180, 180)))
                painter.drawText(col_x, col_y, "No powerups")
        finally:
            painter.restore()

    def _summarize_powerups(self, powerups):
        # Count each stackable powerup
        from collections import Counter

        count = Counter(powerups)
        labels = {
            "increase_accel_50": "Acceleration",
            "top_speed_50": "Top Speed",
            "projectile_size_50": "Projectile Size",
            "plus_1_projectile_per_sec": "Projectile Rate",
            "projectile_damage_plus_1": "Projectile Damage",
            "projectile_mass_50": "Projectile Mass",
            "projectile_speed_50": "Projectile Speed",
            "hp_50": "HP",
            "double_shot": "Double Shot",
            "dot_mass_50": "Dot Mass",
            "goal_gravity_50": "Goal Gravity",
        }
        stackable = {
            "increase_accel_50",
            "top_speed_50",
            "projectile_size_50",
            "plus_1_projectile_per_sec",
            "projectile_damage_plus_1",
            "projectile_mass_50",
            "projectile_speed_50",
            "hp_50",
            "dot_mass_50",
            "goal_gravity_50",
        }
        summary = []
        for key in labels:
            if key in count:
                if key in stackable:
                    # Each instance is +50% or +1, so show total
                    if key.endswith("_50"):
                        percent = 50 * count[key]
                        summary.append(f"{labels[key]} +{percent}%")
                    elif key == "plus_1_projectile_per_sec":
                        summary.append(f"Projectile Rate +{count[key]}")
                    elif key == "projectile_damage_plus_1":
                        summary.append(f"Projectile Damage +{count[key]}")
                elif key == "double_shot":
                    # Show number of projectiles: always at least 1, +1 per double_shot
                    n = 1 + count["double_shot"]
                    summary.append(f"Projectiles x{n}")
                else:
                    summary.append(labels[key])
        # Add any unknowns
        for key in count:
            if key not in labels:
                summary.append(key)
        return summary

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

        # Volume controls (+ and - keys)
        from volume_slider import get_master_volume_slider
        volume_slider = get_master_volume_slider()
        
        if key == Qt.Key.Key_Plus or key == Qt.Key.Key_Equal:  # + key (shift + = or numpad +)
            current_volume = volume_slider.get_volume()
            new_volume = min(1.0, current_volume + VOLUME_STEP)
            volume_slider.set_volume(new_volume)
            volume_slider.show_temporarily()
            self.update()  # Trigger repaint to show slider
            return
        elif key == Qt.Key.Key_Minus:  # - key
            current_volume = volume_slider.get_volume()
            new_volume = max(0.0, current_volume - VOLUME_STEP)
            volume_slider.set_volume(new_volume)
            volume_slider.show_temporarily()
            self.update()  # Trigger repaint to show slider
            return

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

    def mousePressEvent(self, event):
        """Handle mouse press events for volume slider interaction."""
        from volume_slider import get_master_volume_slider

        volume_slider = get_master_volume_slider()

        # Convert event position to QPoint
        mouse_pos = event.pos()

        # Check if volume slider handled the event
        if volume_slider.handle_mouse_press(mouse_pos, self.width(), self.height()):
            event.accept()
            self.update()  # Trigger repaint
            return

        # Let the event propagate if not handled
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Handle mouse release events for volume slider interaction."""
        from volume_slider import get_master_volume_slider

        volume_slider = get_master_volume_slider()

        # Check if volume slider handled the event
        if volume_slider.handle_mouse_release():
            event.accept()
            self.update()  # Trigger repaint
            return

        # Let the event propagate if not handled
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        """Handle mouse move events for volume slider interaction."""
        from volume_slider import get_master_volume_slider

        volume_slider = get_master_volume_slider()

        # Convert event position to QPoint
        mouse_pos = event.pos()

        # Check if volume slider handled the event
        if volume_slider.handle_mouse_move(mouse_pos, self.width(), self.height()):
            event.accept()
            self.update()  # Trigger repaint
            return

        # Let the event propagate if not handled
        super().mouseMoveEvent(event)

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
        try:
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

            # Centered at the bottom, with margin
            window_width = self.width()
            window_height = self.height()
            margin = 20  # Space from bottom edge
            x = (window_width - text_width) // 2
            y = window_height - margin - text_height

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
            # Vertically center text in the background rectangle
            painter.drawText(x, y + text_height - font_metrics.descent(), fps_text)
        finally:
            painter.restore()

    def _powerup_label(self, powerup):
        labels = {
            "increase_accel_50": "Acceleration +50%",
            "top_speed_50": "Top Speed +50%",
            "projectile_size_50": "Projectile Size +50%",
            "plus_1_projectile_per_sec": "+1 Projectile/sec",
            "projectile_damage_plus_1": "Projectile Damage +1",
            "projectile_mass_50": "Projectile Mass +50%",
            "projectile_speed_50": "Projectile Speed +50%",
            "hp_50": "HP +50%",
            "double_shot": "Projectiles +1",
            "dot_mass_50": "Dot Mass +50%",
            "goal_gravity_50": "Goal Gravity +50%",
        }
        return labels.get(powerup, powerup)

    def _paint_game_view(self, widget, event):
        """Paint the game view content."""
        painter = QPainter(widget)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Update FPS counter
        self._update_fps()

        # Calculate dynamic view dimensions - allow play area to stretch to fit window
        window_width = widget.width()
        window_height = widget.height()
        divider_width = 20

        # Use full window size for play area calculations (no resolution capping)
        # Performance is managed through adaptive grid spacing and simple dot rendering
        view_height = window_height
        view_width = (window_width - divider_width) // 2

        # --- Game Over Check ---
        if not self.game_over:
            red_score = self.game_engine.get_red_player_score()
            purple_score = self.game_engine.get_purple_player_score()
            if red_score >= self.points_to_win:
                self._start_game_over(1)
            elif purple_score >= self.points_to_win:
                self._start_game_over(2)

        # --- Score Pulse Effect ---
        score_pulse_state = self.game_engine.get_score_pulse_state()
        score_pulse_color1 = None
        score_pulse_color2 = None
        if score_pulse_state["active"]:
            # Calculate pulse intensity (fade in then fade out)
            progress = score_pulse_state["timer"] / score_pulse_state["duration"]
            if progress < 0.5:
                # Fade in
                intensity = int(progress * 2 * 120)  # Max 120 alpha
            else:
                # Fade out
                intensity = int((1 - progress) * 2 * 120)

            if score_pulse_state["player"] == 1:
                # Red player scored - red pulse
                score_pulse_color1 = QColor(255, 100, 100, intensity)
                score_pulse_color2 = QColor(0, 0, 0, 0)  # No pulse on other view
            else:
                # Purple player scored - purple pulse
                score_pulse_color1 = QColor(0, 0, 0, 0)  # No pulse on other view
                score_pulse_color2 = QColor(200, 100, 255, intensity)

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

            # --- Powerup View Delay Logic ---
            if not self._powerup_view_shown:
                self._powerup_delay_timer += 1
                if self._powerup_delay_timer >= self._powerup_delay_duration:
                    self._show_powerup_selection_view()
                    self._powerup_view_shown = True

        # Combine score pulse and flash effects
        final_color1 = flash_color1 if flash_color1 else score_pulse_color1
        final_color2 = flash_color2 if flash_color2 else score_pulse_color2

        # Draw Player 2 view (left side - Purple)
        self._draw_player_view(
            painter, 2, 0, 0, view_width, view_height, overlay_color=final_color2
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
            overlay_color=final_color1,
        )

        # Draw FPS counter at the bottom left of the window
        if SHOW_FPS_COUNTER:
            self._draw_fps_counter_bottom_center(painter)

        # Draw volume slider at the bottom right of the window
        self._draw_volume_slider(painter)

    def _optimize_for_fullscreen(self):
        """Apply aggressive optimizations specifically for fullscreen mode."""
        if not hasattr(self, "_fullscreen_optimized"):
            self._fullscreen_optimized = True

            # Reduce grid detail in fullscreen
            if hasattr(self, "_original_grid_spacing"):
                return  # Already optimized

            # Store original values
            from config import GRID_SPACING, MAX_RENDER_WIDTH, MAX_RENDER_HEIGHT

            self._original_grid_spacing = GRID_SPACING
            self._original_max_render_width = MAX_RENDER_WIDTH
            self._original_max_render_height = MAX_RENDER_HEIGHT

            # Apply aggressive optimizations
            import config

            config.GRID_SPACING = GRID_SPACING * 3  # Triple spacing = 1/9 grid lines
            # Reduce render resolution cap further for fullscreen
            config.MAX_RENDER_WIDTH = min(800, MAX_RENDER_WIDTH)  # Cap at 800px width
            config.MAX_RENDER_HEIGHT = min(
                600, MAX_RENDER_HEIGHT
            )  # Cap at 600px height

            # Disable antialiasing for performance
            self._enable_antialiasing_optimization(False)

            # Force grid cache invalidation
            self._grid_cache = [None, None]
            self._grid_cache_params = [None, None]

            # Clear rendering caches
            from rendering import Renderer

            Renderer.clear_caches()

            print(
                "Applied fullscreen optimizations: reduced grid density, lowered resolution cap, disabled antialiasing"
            )

    def _restore_windowed_settings(self):
        """Restore normal settings for windowed mode."""
        if hasattr(self, "_fullscreen_optimized") and self._fullscreen_optimized:
            self._fullscreen_optimized = False

            # Restore original settings
            if hasattr(self, "_original_grid_spacing"):
                import config

                config.GRID_SPACING = self._original_grid_spacing
                config.MAX_RENDER_WIDTH = self._original_max_render_width
                config.MAX_RENDER_HEIGHT = self._original_max_render_height

                # Re-enable antialiasing
                self._enable_antialiasing_optimization(True)

                # Force grid cache invalidation
                self._grid_cache = [None, None]
                self._grid_cache_params = [None, None]

                # Clear rendering caches
                from rendering import Renderer

                Renderer.clear_caches()

                print(
                    "Restored windowed settings: normal grid spacing, full resolution, enabled antialiasing"
                )

    def changeEvent(self, event):
        """Handle window state changes (fullscreen/windowed)."""
        from PyQt6.QtCore import QEvent, Qt

        if event.type() == QEvent.Type.WindowStateChange:
            new_fullscreen = bool(self.windowState() & Qt.WindowState.WindowFullScreen)

            if new_fullscreen != self._is_fullscreen:
                self._is_fullscreen = new_fullscreen

                if new_fullscreen:
                    print("Switching to fullscreen mode - applying optimizations")
                    self._optimize_for_fullscreen()
                    # Also notify game engine
                    if hasattr(self.game_engine, "_enable_fullscreen_mode"):
                        self.game_engine._enable_fullscreen_mode()
                else:
                    print("Switching to windowed mode - restoring normal settings")
                    self._restore_windowed_settings()
                    # Also notify game engine
                    if hasattr(self.game_engine, "_disable_fullscreen_mode"):
                        self.game_engine._disable_fullscreen_mode()

        super().changeEvent(event)

    def _enable_antialiasing_optimization(self, enabled):
        """Enable/disable antialiasing in fullscreen mode."""
        self._antialiasing_enabled = enabled
        print(f"Antialiasing {'enabled' if enabled else 'disabled'} for performance")

    def _draw_volume_slider(self, painter):
        """Draw volume slider at the bottom right of the window."""
        from volume_slider import get_master_volume_slider

        painter.save()
        try:
            # Reset clipping to draw on the full window
            painter.setClipping(False)

            # Get the volume slider and draw it
            volume_slider = get_master_volume_slider()

            # Position it on the bottom right, opposite to FPS counter
            window_width = self.width()
            window_height = self.height()

            # Draw the volume slider
            volume_slider.draw(painter, window_width, window_height)

        finally:
            painter.restore()
