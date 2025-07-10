"""
Gamepad Manager for handling USB gamepad input.
Provides a unified interface for gamepad detection and input handling.
"""

import pygame
from config import *


class GamepadManager:
    """Manages gamepad detection and input handling."""

    def __init__(self):
        """Initialize pygame and detect connected gamepads."""
        pygame.init()
        pygame.joystick.init()

        self.gamepads = {}
        self.gamepad_count = 0

        # Initialize all connected gamepads
        self.refresh_gamepads()

    def refresh_gamepads(self):
        """Detect and initialize all connected gamepads."""
        self.gamepad_count = pygame.joystick.get_count()

        for i in range(self.gamepad_count):
            if i not in self.gamepads:
                gamepad = pygame.joystick.Joystick(i)
                gamepad.init()
                self.gamepads[i] = gamepad
                print(f"Gamepad {i} connected: {gamepad.get_name()}")

    def force_refresh_gamepads(self):
        """Manually refresh the gamepad list (use sparingly)."""
        self.refresh_gamepads()

    def get_gamepad_input(self, gamepad_index):
        """
        Get input state for a specific gamepad.

        Args:
            gamepad_index: Index of the gamepad to read from

        Returns:
            dict: Contains left_stick_x, left_stick_y, and shoot_button values
        """
        if gamepad_index not in self.gamepads:
            return {"left_stick_x": 0.0, "left_stick_y": 0.0, "shoot_button": False}

        gamepad = self.gamepads[gamepad_index]

        try:
            # Get left analog stick values
            left_x = gamepad.get_axis(0)  # Left stick X axis
            left_y = gamepad.get_axis(1)  # Left stick Y axis

            # Apply deadzone
            if abs(left_x) < GAMEPAD_DEADZONE:
                left_x = 0.0
            if abs(left_y) < GAMEPAD_DEADZONE:
                left_y = 0.0

            # Get shoot button (A button = button 0 on most controllers)
            shoot_button = gamepad.get_button(0)

            return {
                "left_stick_x": left_x * GAMEPAD_SENSITIVITY,
                "left_stick_y": left_y * GAMEPAD_SENSITIVITY,
                "shoot_button": shoot_button,
            }
        except Exception as e:
            print(f"Error reading gamepad {gamepad_index}: {e}")
            return {"left_stick_x": 0.0, "left_stick_y": 0.0, "shoot_button": False}

    def update(self):
        """Update gamepad states - call this each frame."""
        # Optimize pygame event pumping - only pump every few frames in fullscreen
        if not hasattr(self, "_pump_counter"):
            self._pump_counter = 0

        self._pump_counter += 1

        # In fullscreen mode, pump events less frequently to reduce CPU usage
        # This is the major performance bottleneck identified in profiling
        pump_frequency = 3 if hasattr(self, "_fullscreen_mode") else 1

        if self._pump_counter % pump_frequency == 0:
            pygame.event.pump()

        # Only refresh gamepad list occasionally, not every frame
        # This prevents potential gamepad reinitialization issues

    def is_gamepad_connected(self, gamepad_index):
        """
        Check if a specific gamepad is connected.

        Args:
            gamepad_index: Index of the gamepad to check

        Returns:
            bool: True if gamepad is connected, False otherwise
        """
        return gamepad_index in self.gamepads

    def get_gamepad_info(self):
        """
        Get information about all connected gamepads.

        Returns:
            list: List of gamepad names and indices
        """
        info = []
        for index, gamepad in self.gamepads.items():
            info.append(
                {
                    "index": index,
                    "name": gamepad.get_name(),
                    "axes": gamepad.get_numaxes(),
                    "buttons": gamepad.get_numbuttons(),
                }
            )
        return info

    def set_fullscreen_mode(self, enabled):
        """Enable/disable fullscreen optimizations."""
        if enabled:
            self._fullscreen_mode = True
            print(
                "GamepadManager: Enabled fullscreen optimizations (reduced event pumping)"
            )
        else:
            if hasattr(self, "_fullscreen_mode"):
                delattr(self, "_fullscreen_mode")
            print("GamepadManager: Disabled fullscreen optimizations")
