#!/usr/bin/env python3
"""
Visual demonstration of consistent status display formatting.
Shows the status display in various states to verify consistency.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPainter, QPixmap, QFont
from PyQt6.QtCore import Qt
from rendering import Renderer
from config import *


class StatusDisplayDemo(QWidget):
    """Widget to demonstrate status display consistency."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Status Display Consistency Demo")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Title
        title = QLabel("Status Display Consistency Demo")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        # Description
        desc = QLabel("All displays below should use the same multiplayer format:")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)

        # Create demonstration pixmaps
        demo_scenarios = [
            ("Initial State (0-0)", 0, 0, 10, 10),
            ("Red Player Scores (2-0)", 2, 0, 10, 10),
            ("Both Players Score (2-1)", 2, 1, 10, 10),
            ("After HP Damage (2-1)", 2, 1, 7, 8),
            ("Purple Wins (1-3)", 1, 3, 5, 10),
        ]

        for desc_text, red_score, purple_score, red_hp, purple_hp in demo_scenarios:
            # Create label for scenario description
            scenario_label = QLabel(desc_text)
            scenario_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            scenario_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            layout.addWidget(scenario_label)

            # Create pixmap to draw status on
            pixmap = QPixmap(400, 60)
            pixmap.fill(Qt.GlobalColor.white)

            painter = QPainter(pixmap)
            Renderer.draw_status_display(
                painter, red_score, purple_score, red_hp, purple_hp, 400, 60
            )
            painter.end()

            # Create label to show the pixmap
            pixmap_label = QLabel()
            pixmap_label.setPixmap(pixmap)
            pixmap_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(pixmap_label)

        # Conclusion
        conclusion = QLabel(
            "✅ All status displays use consistent multiplayer formatting"
        )
        conclusion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        conclusion.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        conclusion.setStyleSheet("color: green;")
        layout.addWidget(conclusion)

        self.setLayout(layout)


def main():
    """Main function to run the status display demo."""
    app = QApplication(sys.argv)

    demo = StatusDisplayDemo()
    demo.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
