"""
Powerup selection view for end-of-round powerup selection.
Displays powerup options in a full-screen view instead of a dialog.
"""

import random
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QFontMetrics
from PyQt6.QtCore import Qt, QRect, pyqtSignal, QTimer
from config import *


class PowerupSelectionView(QWidget):
    """Full-screen view for powerup selection at the end of each round."""

    # Signal emitted when a powerup is selected (powerup_key, should_reset)
    powerup_selected = pyqtSignal(str, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.winner_player = None
        self.loser_player = None
        self.powerup_options = []
        self.selected_index = 0  # Currently highlighted option
        self.button_rects = []  # Store button rectangles for click detection

        # Set focus policy to receive keyboard events
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Set dark background
        self.setStyleSheet("background-color: #111;")

        # --- Controller support ---
        self._gamepad_timer = QTimer(self)
        self._gamepad_timer.timeout.connect(self._poll_gamepad)
        self._gamepad_last_x = 0.0
        self._gamepad_nav_cooldown = 0  # Frames to wait before next nav
        self._gamepad_nav_cooldown_max = 8  # ~8*16ms = 128ms between moves
        self._gamepad_last_a = False

    def setup_round_end(self, winner, loser):
        """Setup the view for a new round end."""
        self.winner_player = winner
        self.loser_player = loser
        self.selected_index = 0
        self.button_rects = []

        # Generate 3 random powerup options
        all_powerups = [
            ("increase_accel_50", "Increase acceleration by 50%"),
            ("top_speed_50", "Top speed +50%"),
            ("projectile_size_50", "Increase projectile size by 50%"),
            ("plus_1_projectile_per_sec", "+1 projectile/second"),
            ("projectile_damage_plus_1", "Increase projectile damage by 1"),
            ("projectile_mass_50", "Increase projectile mass by 50%"),
            ("projectile_speed_50", "Increase projectile speed by 50%"),
            ("hp_50", "Increase HP by 50%"),
            ("double_shot", "Increase projectiles by 1"),
            ("dot_mass_50", "Increase player dot mass by 50%"),
            ("goal_gravity_50", "Increase gravitational pull of your goal by 50%"),
        ]
        self.powerup_options = random.sample(all_powerups, 3)

        # Show and focus this widget
        self.show()
        self.setFocus()
        self.update()

        # Start polling for gamepad input
        self._gamepad_timer.start(16)
        self._gamepad_nav_cooldown = 0
        self._gamepad_last_x = 0.0
        self._gamepad_last_a = False

    def _poll_gamepad(self):
        # Only poll if gamepad support is enabled
        if not getattr(self, "_gamepad_timer", None):
            return
        from config import (
            GAMEPAD_ENABLED,
            GAMEPAD_1_INDEX,
            GAMEPAD_1_SHOOT_BUTTON,
            GAMEPAD_DEADZONE,
        )

        if not GAMEPAD_ENABLED:
            return
        # Try to get GamepadManager from parent SplitScreenView
        parent = self.parent()
        gamepad_manager = None
        # Traverse up to find SplitScreenView if needed
        for _ in range(3):
            if parent is None:
                break
            if hasattr(parent, "gamepad_manager"):
                gamepad_manager = parent.gamepad_manager
                break
            parent = getattr(parent, "parent", lambda: None)()
        if not gamepad_manager:
            return
        if not gamepad_manager.is_gamepad_connected(GAMEPAD_1_INDEX):
            return
        state = gamepad_manager.get_gamepad_input(GAMEPAD_1_INDEX)
        x = state.get("left_stick_x", 0.0)
        a = bool(state.get("shoot_button", False))
        # Navigation cooldown logic
        if self._gamepad_nav_cooldown > 0:
            self._gamepad_nav_cooldown -= 1
        # Left/right navigation (only trigger on edge/cooldown)
        if abs(x) > GAMEPAD_DEADZONE:
            if self._gamepad_nav_cooldown == 0:
                if x < 0:
                    self.selected_index = (self.selected_index - 1) % len(
                        self.powerup_options
                    )
                    self.update()
                    self._gamepad_nav_cooldown = self._gamepad_nav_cooldown_max
                elif x > 0:
                    self.selected_index = (self.selected_index + 1) % len(
                        self.powerup_options
                    )
                    self.update()
                    self._gamepad_nav_cooldown = self._gamepad_nav_cooldown_max
        else:
            self._gamepad_nav_cooldown = 0
        # A button for selection (only on press, not hold)
        if a and not self._gamepad_last_a:
            if 0 <= self.selected_index < len(self.powerup_options):
                powerup_key = self.powerup_options[self.selected_index][0]
                self.powerup_selected.emit(powerup_key, False)
        self._gamepad_last_a = a

    def hideEvent(self, event):
        # Stop polling when hidden
        if getattr(self, "_gamepad_timer", None):
            self._gamepad_timer.stop()
        super().hideEvent(event)

    def paintEvent(self, event):
        """Draw the powerup selection screen."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Get window dimensions
        width = self.width()
        height = self.height()

        # Clear button rects for this frame
        self.button_rects = []

        # Draw background gradient
        self._draw_background(painter, width, height)

        # Draw title section
        self._draw_title_section(painter, width, height)

        # Draw powerup options
        self._draw_powerup_options(painter, width, height)

        # Draw footer with controls
        self._draw_footer(painter, width, height)

    def _draw_background(self, painter, width, height):
        """Draw the background gradient."""
        # Create a subtle gradient from dark to slightly lighter
        gradient_rect = QRect(0, 0, width, height)

        # Fill with dark background
        painter.fillRect(gradient_rect, QColor(17, 17, 17))

        # Add some subtle visual elements
        painter.setPen(QPen(QColor(40, 40, 40), 2))

        # Draw subtle grid lines
        grid_spacing = 50
        for x in range(0, width, grid_spacing):
            painter.drawLine(x, 0, x, height)
        for y in range(0, height, grid_spacing):
            painter.drawLine(0, y, width, y)

    def _draw_title_section(self, painter, width, height):
        """Draw the title and round result."""
        # Title font
        title_font = QFont("Arial", 36, QFont.Weight.Bold)
        painter.setFont(title_font)
        painter.setPen(QPen(QColor(255, 255, 255)))

        # Main title
        title_text = "ROUND COMPLETE"
        title_metrics = painter.fontMetrics()
        title_width = title_metrics.horizontalAdvance(title_text)
        title_x = (width - title_width) // 2
        title_y = height // 6
        painter.drawText(title_x, title_y, title_text)

        # Winner announcement
        winner_font = QFont("Arial", 24, QFont.Weight.Bold)
        painter.setFont(winner_font)

        winner_text = f"Player {self.winner_player} Wins!"
        if self.winner_player == 1:
            painter.setPen(QPen(QColor(255, 100, 100)))  # Light red
        else:
            painter.setPen(QPen(QColor(200, 100, 255)))  # Light purple

        winner_metrics = painter.fontMetrics()
        winner_width = winner_metrics.horizontalAdvance(winner_text)
        winner_x = (width - winner_width) // 2
        winner_y = title_y + 60
        painter.drawText(winner_x, winner_y, winner_text)

        # Powerup selection instruction
        instruction_font = QFont("Arial", 18, QFont.Weight.Normal)
        painter.setFont(instruction_font)
        painter.setPen(QPen(QColor(200, 200, 200)))

        instruction_text = f"Player {self.loser_player}, choose your powerup:"
        instruction_metrics = painter.fontMetrics()
        instruction_width = instruction_metrics.horizontalAdvance(instruction_text)
        instruction_x = (width - instruction_width) // 2
        instruction_y = winner_y + 80
        painter.drawText(instruction_x, instruction_y, instruction_text)

    def _draw_powerup_options(self, painter, width, height):
        """Draw the three powerup options."""
        # Calculate button layout
        button_width = 300
        button_height = 120
        button_spacing = 40
        total_width = (button_width * 3) + (button_spacing * 2)
        start_x = (width - total_width) // 2
        start_y = height // 2 - button_height // 2

        # Draw each powerup option
        for i, (powerup_key, powerup_desc) in enumerate(self.powerup_options):
            button_x = start_x + i * (button_width + button_spacing)
            button_y = start_y

            # Store button rectangle for click detection
            button_rect = QRect(button_x, button_y, button_width, button_height)
            self.button_rects.append(button_rect)

            # Determine if this button is selected
            is_selected = i == self.selected_index

            # Draw button background
            if is_selected:
                # Highlighted button
                painter.setBrush(QBrush(QColor(70, 70, 150)))
                painter.setPen(QPen(QColor(120, 120, 255), 3))
            else:
                # Normal button
                painter.setBrush(QBrush(QColor(50, 50, 50)))
                painter.setPen(QPen(QColor(100, 100, 100), 2))

            painter.drawRoundedRect(button_rect, 10, 10)

            # Draw button text
            text_font = QFont("Arial", 14, QFont.Weight.Bold)
            painter.setFont(text_font)

            if is_selected:
                painter.setPen(QPen(QColor(255, 255, 255)))
            else:
                painter.setPen(QPen(QColor(200, 200, 200)))

            # Word wrap the text if needed
            text_lines = self._wrap_text(
                powerup_desc, button_width - 20, painter.fontMetrics()
            )

            # Calculate text position
            line_height = painter.fontMetrics().height()
            total_text_height = len(text_lines) * line_height
            text_start_y = (
                button_y + (button_height - total_text_height) // 2 + line_height
            )

            # Draw each line of text
            for j, line in enumerate(text_lines):
                line_width = painter.fontMetrics().horizontalAdvance(line)
                line_x = button_x + (button_width - line_width) // 2
                line_y = text_start_y + j * line_height
                painter.drawText(line_x, line_y, line)

            # Draw selection indicator
            if is_selected:
                # Draw selection arrow
                arrow_size = 20
                arrow_x = button_x - arrow_size - 10
                arrow_y = button_y + button_height // 2

                painter.setBrush(QBrush(QColor(255, 255, 100)))
                painter.setPen(QPen(QColor(255, 255, 100)))

                # Draw triangle pointing right
                triangle_points = [
                    (arrow_x, arrow_y - arrow_size // 2),
                    (arrow_x, arrow_y + arrow_size // 2),
                    (arrow_x + arrow_size, arrow_y),
                ]

                from PyQt6.QtCore import QPoint
                from PyQt6.QtGui import QPolygon

                triangle = QPolygon([QPoint(x, y) for x, y in triangle_points])
                painter.drawPolygon(triangle)

    def _draw_footer(self, painter, width, height):
        """Draw the footer with control instructions and reset option."""
        footer_y = height - 100

        # Controls text
        controls_font = QFont("Arial", 14, QFont.Weight.Normal)
        painter.setFont(controls_font)
        painter.setPen(QPen(QColor(180, 180, 180)))

        controls_text = "Use Arrow Keys or A/D to navigate • Enter/Space to select • R to reset game"
        controls_metrics = painter.fontMetrics()
        controls_width = controls_metrics.horizontalAdvance(controls_text)
        controls_x = (width - controls_width) // 2
        painter.drawText(controls_x, footer_y, controls_text)

        # Reset game instruction
        reset_font = QFont("Arial", 12, QFont.Weight.Normal)
        painter.setFont(reset_font)
        painter.setPen(QPen(QColor(150, 150, 150)))

        reset_text = "Press R to reset the entire game instead of continuing"
        reset_metrics = painter.fontMetrics()
        reset_width = reset_metrics.horizontalAdvance(reset_text)
        reset_x = (width - reset_width) // 2
        painter.drawText(reset_x, footer_y + 30, reset_text)

    def _wrap_text(self, text, max_width, font_metrics):
        """Wrap text to fit within the specified width."""
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font_metrics.horizontalAdvance(test_line) <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    def keyPressEvent(self, event):
        """Handle keyboard navigation."""
        key = event.key()

        if key in [Qt.Key.Key_Left, Qt.Key.Key_A]:
            # Move selection left
            self.selected_index = (self.selected_index - 1) % len(self.powerup_options)
            self.update()
        elif key in [Qt.Key.Key_Right, Qt.Key.Key_D]:
            # Move selection right
            self.selected_index = (self.selected_index + 1) % len(self.powerup_options)
            self.update()
        elif key in [Qt.Key.Key_Return, Qt.Key.Key_Space]:
            # Select current powerup
            if 0 <= self.selected_index < len(self.powerup_options):
                powerup_key = self.powerup_options[self.selected_index][0]
                self.powerup_selected.emit(powerup_key, False)  # False = don't reset
        elif key == Qt.Key.Key_R:
            # Reset game
            self.powerup_selected.emit("", True)  # True = reset game

    def mousePressEvent(self, event):
        """Handle mouse clicks on powerup buttons."""
        click_pos = event.position().toPoint()

        # Check if click is on any button
        for i, button_rect in enumerate(self.button_rects):
            if button_rect.contains(click_pos):
                self.selected_index = i
                powerup_key = self.powerup_options[i][0]
                self.powerup_selected.emit(powerup_key, False)
                return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handle mouse hover to highlight buttons."""
        hover_pos = event.position().toPoint()

        # Check if hovering over any button
        for i, button_rect in enumerate(self.button_rects):
            if button_rect.contains(hover_pos):
                if self.selected_index != i:
                    self.selected_index = i
                    self.update()
                return

        super().mouseMoveEvent(event)
