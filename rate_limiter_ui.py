"""
UI components for the rate limiter system.
Provides visual feedback for projectile firing rate limits and cooldowns.
"""

import math
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor
from PyQt6.QtCore import QRect
from config import *


class RateLimiterUI:
    """UI component for displaying rate limiter status as a pie chart."""

    @staticmethod
    def draw_rate_limiter(painter, center_x, center_y, progress_data):
        """
        Draw a pie chart style rate limiter indicator.

        Args:
            painter: QPainter object for drawing
            center_x: X coordinate of circle center
            center_y: Y coordinate of circle center
            progress_data: Dict from rate_limiter.get_progress()
        """
        radius = RATE_LIMITER_RADIUS
        thickness = RATE_LIMITER_THICKNESS

        # Determine colors based on state
        if progress_data["type"] == "cooldown":
            fill_color = RATE_LIMITER_COLOR_COOLDOWN
        elif progress_data["type"] == "warning":
            fill_color = RATE_LIMITER_COLOR_WARNING
        else:
            fill_color = RATE_LIMITER_COLOR_NORMAL

        # Draw background ring
        painter.setPen(QPen(QColor(*RATE_LIMITER_BACKGROUND_COLOR), thickness))
        painter.setBrush(QBrush())  # No fill
        painter.drawEllipse(
            center_x - radius, center_y - radius, radius * 2, radius * 2
        )

        # Draw progress arc
        if progress_data["progress"] > 0:
            painter.setPen(QPen(QColor(*fill_color), thickness))

            # Calculate arc parameters
            # Qt uses 16ths of a degree, starting from 3 o'clock, going clockwise
            start_angle = 90 * 16  # Start at 12 o'clock (90 degrees from 3 o'clock)
            span_angle = int(
                progress_data["progress"] * 360 * 16
            )  # Progress as arc span

            # Create rectangle for arc drawing
            rect = QRect(center_x - radius, center_y - radius, radius * 2, radius * 2)

            painter.drawArc(rect, start_angle, span_angle)

        # Draw center indicator based on state
        center_radius = radius // 3
        if progress_data["type"] == "cooldown":
            # Red center during cooldown
            painter.setBrush(QBrush(QColor(*RATE_LIMITER_COLOR_COOLDOWN)))
        elif progress_data["type"] == "warning":
            # Yellow center when approaching limit
            painter.setBrush(QBrush(QColor(*RATE_LIMITER_COLOR_WARNING)))
        else:
            # Green center when normal
            painter.setBrush(QBrush(QColor(*RATE_LIMITER_COLOR_NORMAL)))

        painter.setPen(QPen())  # No outline
        painter.drawEllipse(
            center_x - center_radius,
            center_y - center_radius,
            center_radius * 2,
            center_radius * 2,
        )

    @staticmethod
    def draw_rate_limiter_with_label(painter, x, y, progress_data, player_name):
        """
        Draw rate limiter with a text label.

        Args:
            painter: QPainter object
            x: X coordinate for the indicator
            y: Y coordinate for the indicator
            progress_data: Progress data from rate limiter
            player_name: String label (e.g., "P1", "P2")
        """
        # Draw the pie chart
        RateLimiterUI.draw_rate_limiter(painter, x, y, progress_data)

        # Draw label below the indicator
        painter.setPen(QPen(QColor(255, 255, 255)))  # White text
        painter.drawText(x - 10, y + RATE_LIMITER_RADIUS + 15, player_name)

        # Draw time remaining if in cooldown
        if progress_data["type"] == "cooldown" and progress_data["time_remaining"] > 0:
            time_text = f"{progress_data['time_remaining']:.1f}s"
            painter.drawText(x - 15, y + RATE_LIMITER_RADIUS + 30, time_text)


class StatusDisplay:
    """Combined status display for player information."""

    @staticmethod
    def draw_player_status(
        painter, x, y, player_name, hp, score, rate_limiter_data, points_to_win=None
    ):
        """
        Draw a comprehensive player status display.

        Args:
            painter: QPainter object
            x, y: Position for the status display
            player_name: Player identifier ("Player 1", "Player 2")
            hp: Hit points
            score: Player score
            rate_limiter_data: Rate limiter progress data
            points_to_win: Points needed to win (optional, for fraction display)
        """
        # Draw rate limiter indicator
        RateLimiterUI.draw_rate_limiter(painter, x + 30, y + 30, rate_limiter_data)

        # Draw player info text
        painter.setPen(QPen(QColor(255, 255, 255)))  # White text

        # Player name
        painter.drawText(x + 70, y + 20, player_name)

        # HP with color coding based on value
        hp_text = f"HP: {hp}"
        if hp <= 1:
            # Flash red when HP is 1 or below - use frame count for flashing
            import time

            flash_on = (int(time.time() * 8) % 2) == 0  # Flash 4 times per second
            if flash_on:
                painter.setPen(QPen(QColor(255, 0, 0)))  # Red
            else:
                painter.setPen(QPen(QColor(128, 0, 0)))  # Dark red
        elif hp <= 5:
            painter.setPen(QPen(QColor(255, 255, 0)))  # Yellow
        else:
            painter.setPen(QPen(QColor(255, 255, 255)))  # White
        painter.drawText(x + 70, y + 35, hp_text)

        # Reset to white for other text
        painter.setPen(QPen(QColor(255, 255, 255)))

        # Score (show as fraction if points_to_win is provided)
        if points_to_win is not None:
            painter.drawText(x + 70, y + 50, f"Score: {score}/{points_to_win}")
        else:
            painter.drawText(x + 70, y + 50, f"Score: {score}")

        # Rate limiter status
        if rate_limiter_data["type"] == "cooldown":
            status_text = f"Cooldown: {rate_limiter_data['time_remaining']:.1f}s"
            painter.setPen(QPen(QColor(*RATE_LIMITER_COLOR_COOLDOWN)))
        elif rate_limiter_data["type"] == "warning":
            shots_left = PROJECTILE_RATE_LIMIT - int(
                rate_limiter_data["progress"] * PROJECTILE_RATE_LIMIT
            )
            status_text = f"Shots left: {shots_left}"
            painter.setPen(QPen(QColor(*RATE_LIMITER_COLOR_WARNING)))
        else:
            shots_left = PROJECTILE_RATE_LIMIT - int(
                rate_limiter_data["progress"] * PROJECTILE_RATE_LIMIT
            )
            status_text = f"Shots: {shots_left}/{PROJECTILE_RATE_LIMIT}"
            painter.setPen(QPen(QColor(*RATE_LIMITER_COLOR_NORMAL)))

        painter.drawText(x + 70, y + 65, status_text)
