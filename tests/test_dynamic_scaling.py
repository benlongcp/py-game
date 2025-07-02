#!/usr/bin/env python3
"""
Test script to verify dynamic window scaling functionality.
This creates a resizable window to test that the game scales properly.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont
from split_screen import SplitScreenView
from game_engine import GameEngine


class TestWindow(QMainWindow):
    """Test window for verifying dynamic scaling functionality."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dynamic Scaling Test")

        # Performance monitoring
        self.frame_count = 0
        self.last_fps_time = time.time()
        self.fps = 0.0

        # Create game engine
        self.game_engine = GameEngine()

        # Create split screen view
        self.split_screen = SplitScreenView(self.game_engine)

        # Setup layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Add FPS display
        self.fps_label = QLabel("FPS: 0.0")
        self.fps_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(self.fps_label)

        # Add test buttons
        btn_small = QPushButton("Set Small Size (800x600)")
        btn_small.clicked.connect(lambda: self.set_size(800, 600))
        layout.addWidget(btn_small)

        btn_medium = QPushButton("Set Medium Size (1200x800)")
        btn_medium.clicked.connect(lambda: self.set_size(1200, 800))
        layout.addWidget(btn_medium)

        btn_large = QPushButton("Set Large Size (1600x1200)")
        btn_large.clicked.connect(lambda: self.set_size(1600, 1200))
        layout.addWidget(btn_large)

        btn_maximize = QPushButton("Maximize Window")
        btn_maximize.clicked.connect(self.showMaximized)
        layout.addWidget(btn_maximize)

        # Add the split screen view
        layout.addWidget(self.split_screen)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Start with medium size
        self.set_size(1200, 800)

        # Setup update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)  # ~60 FPS

        print("Dynamic Scaling Test Window Created")
        print("Use the buttons to test different window sizes.")
        print("Verify that:")
        print("- Objects remain properly positioned when resizing")
        print("- Physics continue to work correctly")
        print("- Rendering performance remains good")
        print("- Both player views scale correctly")

    def set_size(self, width, height):
        """Set the window to a specific size."""
        self.resize(width, height + 120)  # Extra height for buttons
        print(f"Window resized to {width}x{height}")

    def update_game(self):
        """Update the game engine and calculate FPS."""
        self.game_engine.update_game_state()

        # Calculate FPS
        self.frame_count += 1
        current_time = time.time()
        time_diff = current_time - self.last_fps_time

        # Update FPS display every 0.5 seconds
        if time_diff >= 0.5:
            self.fps = self.frame_count / time_diff
            self.fps_label.setText(f"FPS: {self.fps:.1f}")
            self.frame_count = 0
            self.last_fps_time = current_time


def main():
    app = QApplication(sys.argv)

    # Create test window
    test_window = TestWindow()
    test_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
