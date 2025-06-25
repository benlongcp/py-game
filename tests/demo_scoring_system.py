#!/usr/bin/env python3
"""
Interactive demo to showcase the scoring system.
This script demonstrates how players can score points by keeping the blue square in static circles.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPainter, QPen, QColor, QFont
from game_engine import GameEngine
from rendering import Renderer
from config import *


class ScoringDemoWindow(QMainWindow):
    """Demo window showcasing the scoring system."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scoring System Demo - py-widget")
        self.setGeometry(100, 100, 800, 600)

        # Initialize game engine
        self.game_engine = GameEngine()
        self.game_engine.create_purple_dot()  # Enable multiplayer

        # Timer for game updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(FRAME_TIME_MS)

        # Demo phase and timer
        self.demo_phase = "instructions"
        self.demo_timer = 0
        self.phase_duration = 180  # 3 seconds at 60 FPS

        # Initialize demo
        self.setup_demo_phase()

    def setup_demo_phase(self):
        """Set up the current demo phase."""
        if self.demo_phase == "instructions":
            # Show instructions
            pass
        elif self.demo_phase == "red_scoring":
            # Move blue square to red circle
            self.game_engine.blue_square.x = STATIC_RED_CIRCLE_X
            self.game_engine.blue_square.y = STATIC_RED_CIRCLE_Y
            self.game_engine.blue_square.velocity_x = 0
            self.game_engine.blue_square.velocity_y = 0
        elif self.demo_phase == "purple_scoring":
            # Move blue square to purple circle
            self.game_engine.blue_square.x = STATIC_PURPLE_CIRCLE_X
            self.game_engine.blue_square.y = STATIC_PURPLE_CIRCLE_Y
            self.game_engine.blue_square.velocity_x = 0
            self.game_engine.blue_square.velocity_y = 0
        elif self.demo_phase == "manual_control":
            # Let users control the game
            pass

    def update_game(self):
        """Update game state and demo progression."""
        self.game_engine.update_game_state()
        self.demo_timer += 1

        # Progress through demo phases automatically
        if self.demo_phase == "instructions" and self.demo_timer >= self.phase_duration:
            self.demo_phase = "red_scoring"
            self.demo_timer = 0
            self.setup_demo_phase()
        elif (
            self.demo_phase == "red_scoring" and self.demo_timer >= self.phase_duration
        ):
            self.demo_phase = "purple_scoring"
            self.demo_timer = 0
            self.setup_demo_phase()
        elif (
            self.demo_phase == "purple_scoring"
            and self.demo_timer >= self.phase_duration
        ):
            self.demo_phase = "manual_control"
            self.demo_timer = 0
            self.setup_demo_phase()

        self.update()

    def paintEvent(self, event):
        """Render the demo."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Calculate view settings
        view_width = self.width()
        view_height = self.height()
        camera_x = 0  # Center view on origin
        camera_y = 0

        # Draw background
        painter.fillRect(0, 0, view_width, view_height, QColor(240, 240, 240))

        # Draw grid
        Renderer.draw_grid(painter, camera_x, camera_y, view_width, view_height)

        # Draw static circles
        Renderer.draw_static_red_circle(painter, camera_x, camera_y)
        Renderer.draw_static_purple_circle(painter, camera_x, camera_y)

        # Draw gravitational dots
        Renderer.draw_red_gravitational_dot(
            painter, self.game_engine.red_gravity_dot, camera_x, camera_y
        )
        Renderer.draw_purple_gravitational_dot(
            painter, self.game_engine.purple_gravity_dot, camera_x, camera_y
        )

        # Draw players
        Renderer.draw_red_dot_world(
            painter, self.game_engine.red_dot, camera_x, camera_y
        )
        Renderer.draw_purple_dot(
            painter, self.game_engine.purple_dot, camera_x, camera_y
        )

        # Draw blue square
        Renderer.draw_blue_square_world(
            painter, self.game_engine.blue_square, camera_x, camera_y
        )

        # Draw projectiles
        for projectile in self.game_engine.projectiles:
            Renderer.draw_projectile_world(painter, projectile, camera_x, camera_y)

        # Draw score
        red_score = self.game_engine.get_red_player_score()
        purple_score = self.game_engine.get_purple_player_score()
        Renderer.draw_score(painter, red_score, purple_score, view_width, view_height)

        # Draw demo information
        self.draw_demo_info(painter, view_width, view_height)

    def draw_demo_info(self, painter, view_width, view_height):
        """Draw demo information and instructions."""
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        font = QFont()
        font.setPointSize(12)
        painter.setFont(font)

        y_offset = 30

        if self.demo_phase == "instructions":
            lines = [
                "🎯 Scoring System Demo",
                "",
                "• Players score when the blue square fully overlaps a static circle for 1.0 seconds",
                "• Red player scores from the red circle (left side)",
                "• Purple player scores from the purple circle (right side)",
                "• Blue square respawns at grid center after scoring",
                "",
                "Demo will automatically show scoring for both players...",
            ]
        elif self.demo_phase == "red_scoring":
            overlap_progress = (
                self.game_engine.red_circle_overlap_timer / SCORE_OVERLAP_FRAMES
            )
            lines = [
                "🔴 Red Player Scoring Demo",
                "",
                f"Blue square overlap progress: {overlap_progress:.1%}",
                f"Frames needed for score: {SCORE_OVERLAP_FRAMES}",
                f"Current overlap frames: {self.game_engine.red_circle_overlap_timer}",
                "",
                "Watch as the blue square stays in the red circle...",
            ]
        elif self.demo_phase == "purple_scoring":
            overlap_progress = (
                self.game_engine.purple_circle_overlap_timer / SCORE_OVERLAP_FRAMES
            )
            lines = [
                "🟣 Purple Player Scoring Demo",
                "",
                f"Blue square overlap progress: {overlap_progress:.1%}",
                f"Frames needed for score: {SCORE_OVERLAP_FRAMES}",
                f"Current overlap frames: {self.game_engine.purple_circle_overlap_timer}",
                "",
                "Watch as the blue square stays in the purple circle...",
            ]
        elif self.demo_phase == "manual_control":
            lines = [
                "🎮 Manual Control Mode",
                "",
                "Controls:",
                "• Player 1 (Red): Arrow keys + Space (shoot)",
                "• Player 2 (Purple): WASD + Ctrl (shoot)",
                "",
                "Try to score points by shooting the blue square into the static circles!",
                "Keep it inside a circle for 1.0 seconds to score.",
            ]

        for i, line in enumerate(lines):
            painter.drawText(10, y_offset + (i * 20), line)

    def keyPressEvent(self, event):
        """Handle key press events."""
        if self.demo_phase == "manual_control":
            # Forward input to game engine
            key = event.key()

            # Player 1 controls
            if key in [
                Qt.Key.Key_Left,
                Qt.Key.Key_Right,
                Qt.Key.Key_Up,
                Qt.Key.Key_Down,
            ]:
                self.game_engine.set_player1_key(key, True)
            elif key == Qt.Key.Key_Space:
                self.game_engine.shoot_projectile_player1()

            # Player 2 controls
            elif key in [Qt.Key.Key_A, Qt.Key.Key_D, Qt.Key.Key_W, Qt.Key.Key_S]:
                self.game_engine.set_player2_key(key, True)
            elif key == Qt.Key.Key_Control:
                self.game_engine.shoot_projectile_player2()

    def keyReleaseEvent(self, event):
        """Handle key release events."""
        if self.demo_phase == "manual_control":
            # Forward input to game engine
            key = event.key()

            # Player 1 controls
            if key in [
                Qt.Key.Key_Left,
                Qt.Key.Key_Right,
                Qt.Key.Key_Up,
                Qt.Key.Key_Down,
            ]:
                self.game_engine.set_player1_key(key, False)

            # Player 2 controls
            elif key in [Qt.Key.Key_A, Qt.Key.Key_D, Qt.Key.Key_W, Qt.Key.Key_S]:
                self.game_engine.set_player2_key(key, False)


def main():
    """Main function to run the scoring demo."""
    app = QApplication(sys.argv)

    window = ScoringDemoWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
