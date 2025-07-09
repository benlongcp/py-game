#!/usr/bin/env python3
"""
Test script to visualize the elliptical vignette gradient.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor
from PyQt6.QtCore import Qt
from rendering import Renderer
from config import *


class VignetteTestWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Elliptical Vignette Gradient Test")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: black;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Set up coordinates
        width = self.width()
        height = self.height()
        view_center_x = width // 2
        view_center_y = height // 2
        camera_x = 0  # Centered on world origin
        camera_y = 0

        # Draw a simple background grid for reference
        painter.setPen(QPen(QColor(50, 50, 50), 1))
        for x in range(0, width, 50):
            painter.drawLine(x, 0, x, height)
        for y in range(0, height, 50):
            painter.drawLine(0, y, width, y)

        # Draw the elliptical boundary for reference
        world_origin_screen_x = view_center_x - camera_x
        world_origin_screen_y = view_center_y - camera_y

        painter.setPen(QPen(QColor(100, 255, 100), 2))  # Green boundary
        painter.setBrush(QBrush(Qt.BrushStyle.NoBrush))
        painter.drawEllipse(
            int(world_origin_screen_x - GRID_RADIUS_X),
            int(world_origin_screen_y - GRID_RADIUS_Y),
            GRID_RADIUS_X * 2,
            GRID_RADIUS_Y * 2,
        )

        # Draw the vignette gradient
        Renderer.draw_vignette_gradient(
            painter, camera_x, camera_y, view_center_x, view_center_y
        )

        # Add some text
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.drawText(
            10, 30, f"Ellipse dimensions: {GRID_RADIUS_X} x {GRID_RADIUS_Y}"
        )
        painter.drawText(10, 50, "Green line shows the actual play area boundary")
        painter.drawText(10, 70, "White gradient should match the ellipse shape")


def main():
    app = QApplication(sys.argv)

    widget = VignetteTestWidget()
    widget.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
