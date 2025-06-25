"""
Game Engine class for the Topographical Plane application.
Manages all game objects, physics, and collisions in a centralized way.
This allows multiple windows to reference the same game state.
"""

import math
from PyQt6.QtCore import Qt
from config import *
from objects import (
    RedDot,
    BlueSquare,
    Projectile,
    PurpleDot,
    RedGravitationalDot,
    PurpleGravitationalDot,
)
from physics import PhysicsEngine
import math


class GameEngine:
    """Centralized game logic and state management."""

    def __init__(self):
        """Initialize the game engine with all objects."""
        self.red_dot = RedDot()
        self.purple_dot = None  # Will be created when second player joins
        self.blue_square = BlueSquare()
        self.projectiles = []  # List to hold active projectiles

        # Gravitational dots for physics effects
        self.red_gravity_dot = RedGravitationalDot()
        self.purple_gravity_dot = PurpleGravitationalDot()

        # Scoring system
        self.red_player_score = 0
        self.purple_player_score = 0
        self.red_circle_overlap_timer = (
            0  # Frames blue square has been fully inside red circle
        )
        self.purple_circle_overlap_timer = (
            0  # Frames blue square has been fully inside purple circle
        )

        # Input states for both players
        self.player1_keys = set()  # Arrow keys + Space
        self.player2_keys = set()  # WASD + Ctrl

    def create_purple_dot(self):
        """Create the purple dot for player 2 if it doesn't exist."""
        if self.purple_dot is None:
            # Start purple dot at a different position
            self.purple_dot = PurpleDot(INITIAL_DOT_X - 100, INITIAL_DOT_Y - 100)

    def update_game_state(self):
        """Update all game objects - called every frame."""
        self._handle_input()
        self._update_physics()
        self._handle_collisions()
        self._update_scoring()

    def _handle_input(self):
        """Process input for both players."""
        # Player 1 (Red dot) - Arrow keys
        self.red_dot.acceleration_x = 0
        self.red_dot.acceleration_y = 0

        if Qt.Key.Key_Left in self.player1_keys:
            self.red_dot.acceleration_x = -ACCELERATION
        if Qt.Key.Key_Right in self.player1_keys:
            self.red_dot.acceleration_x = ACCELERATION
        if Qt.Key.Key_Up in self.player1_keys:
            self.red_dot.acceleration_y = -ACCELERATION
        if Qt.Key.Key_Down in self.player1_keys:
            self.red_dot.acceleration_y = ACCELERATION

        # Player 2 (Purple dot) - WASD keys
        if self.purple_dot is not None:
            self.purple_dot.acceleration_x = 0
            self.purple_dot.acceleration_y = 0

            if Qt.Key.Key_A in self.player2_keys:
                self.purple_dot.acceleration_x = -ACCELERATION
            if Qt.Key.Key_D in self.player2_keys:
                self.purple_dot.acceleration_x = ACCELERATION
            if Qt.Key.Key_W in self.player2_keys:
                self.purple_dot.acceleration_y = -ACCELERATION
            if Qt.Key.Key_S in self.player2_keys:
                self.purple_dot.acceleration_y = ACCELERATION

    def _update_physics(self):
        """Update physics for all objects."""
        self.red_dot.update_physics()
        if self.purple_dot is not None:
            self.purple_dot.update_physics()
        self.blue_square.update_physics()

        # Apply gravitational forces to the blue square
        self._apply_gravitational_forces()

        # Update projectile physics
        for projectile in self.projectiles[
            :
        ]:  # Use slice copy to safely modify during iteration
            projectile.update_physics()
            if not projectile.is_active:
                self.projectiles.remove(projectile)

    def _handle_collisions(self):
        """Check and resolve collisions between objects."""
        # Blue square collisions
        self.blue_square.check_collision_with_dot(self.red_dot)
        if self.purple_dot is not None:
            self.blue_square.check_collision_with_dot(self.purple_dot)

        # Projectile collisions
        for projectile in self.projectiles:
            if projectile.is_active:
                projectile.check_collision_with_square(self.blue_square)
                projectile.check_collision_with_dot(self.red_dot)
                if self.purple_dot is not None:
                    projectile.check_collision_with_dot(self.purple_dot)

        # Player vs player collision
        if self.purple_dot is not None:
            self._handle_player_collision()

    def _handle_player_collision(self):
        """Handle collision between red and purple dots."""
        distance = math.sqrt(
            (self.red_dot.virtual_x - self.purple_dot.virtual_x) ** 2
            + (self.red_dot.virtual_y - self.purple_dot.virtual_y) ** 2
        )
        collision_distance = self.red_dot.radius + self.purple_dot.radius

        if distance <= collision_distance:
            # Calculate collision normal (from red to purple)
            if distance > 0:
                normal_x = (
                    self.purple_dot.virtual_x - self.red_dot.virtual_x
                ) / distance
                normal_y = (
                    self.purple_dot.virtual_y - self.red_dot.virtual_y
                ) / distance
            else:
                normal_x = 1.0
                normal_y = 0.0

            # Separate the objects first
            overlap = collision_distance - distance
            separation = overlap / 2

            self.red_dot.virtual_x -= normal_x * separation
            self.red_dot.virtual_y -= normal_y * separation
            self.purple_dot.virtual_x += normal_x * separation
            self.purple_dot.virtual_y += normal_y * separation

            # Apply collision response with forced collision (bypass separating velocity check)
            # Calculate relative velocity
            relative_velocity_x = self.red_dot.velocity_x - self.purple_dot.velocity_x
            relative_velocity_y = self.red_dot.velocity_y - self.purple_dot.velocity_y

            # Calculate relative velocity in collision normal direction
            relative_velocity_normal = (
                relative_velocity_x * normal_x + relative_velocity_y * normal_y
            )

            # Force collision response even if objects appear to be separating
            # (since we detected overlap, they must have been approaching)
            if relative_velocity_normal > 0:
                # Objects are separating after overlap - this is the normal case
                # Apply collision response
                impulse_magnitude = -(1 + RESTITUTION) * relative_velocity_normal
                impulse_magnitude /= 1 / self.red_dot.mass + 1 / self.purple_dot.mass

                # Apply impulse to both objects
                impulse_x = impulse_magnitude * normal_x
                impulse_y = impulse_magnitude * normal_y

                self.red_dot.velocity_x += impulse_x / self.red_dot.mass
                self.red_dot.velocity_y += impulse_y / self.red_dot.mass
                self.purple_dot.velocity_x -= impulse_x / self.purple_dot.mass
                self.purple_dot.velocity_y -= impulse_y / self.purple_dot.mass

    def shoot_projectile_player1(self):
        """Create and add a projectile for player 1 (red dot)."""
        if len(self.projectiles) >= PROJECTILE_MAX_COUNT:
            return

        new_projectile = self.red_dot.shoot_projectile()
        if new_projectile:
            self.projectiles.append(new_projectile)

    def shoot_projectile_player2(self):
        """Create and add a projectile for player 2 (purple dot)."""
        if self.purple_dot is None or len(self.projectiles) >= PROJECTILE_MAX_COUNT:
            return

        new_projectile = self.purple_dot.shoot_projectile()
        if new_projectile:
            self.projectiles.append(new_projectile)

    def set_player1_key(self, key, pressed):
        """Set player 1 key state."""
        if pressed:
            self.player1_keys.add(key)
        else:
            self.player1_keys.discard(key)

    def set_player2_key(self, key, pressed):
        """Set player 2 key state."""
        if pressed:
            self.player2_keys.add(key)
        else:
            self.player2_keys.discard(key)

    def _apply_gravitational_forces(self):
        """Apply gravitational forces from the gravitational dots to the blue square."""
        # Apply gravity from red gravitational dot
        self.red_gravity_dot.apply_gravity_to_object(self.blue_square)

        # Apply gravity from purple gravitational dot
        self.purple_gravity_dot.apply_gravity_to_object(self.blue_square)

    def _update_scoring(self):
        """Update scoring based on blue square position relative to static circles."""
        # Import here to avoid circular imports
        from objects import StaticRedCircle, StaticPurpleCircle

        red_circle = StaticRedCircle()
        purple_circle = StaticPurpleCircle()

        # Check if blue square is fully inside red circle
        red_distance = math.sqrt(
            (self.blue_square.x - red_circle.x) ** 2
            + (self.blue_square.y - red_circle.y) ** 2
        )
        red_fully_inside = (
            red_distance + self.blue_square.size / 2
        ) <= red_circle.radius

        # Check if blue square is fully inside purple circle
        purple_distance = math.sqrt(
            (self.blue_square.x - purple_circle.x) ** 2
            + (self.blue_square.y - purple_circle.y) ** 2
        )
        purple_fully_inside = (
            purple_distance + self.blue_square.size / 2
        ) <= purple_circle.radius

        # Update red circle overlap timer
        if red_fully_inside:
            self.red_circle_overlap_timer += 1
            # Reset purple timer since blue square can't be in both circles
            self.purple_circle_overlap_timer = 0
        else:
            self.red_circle_overlap_timer = 0

        # Update purple circle overlap timer
        if purple_fully_inside:
            self.purple_circle_overlap_timer += 1
            # Reset red timer since blue square can't be in both circles
            self.red_circle_overlap_timer = 0
        else:
            self.purple_circle_overlap_timer = 0

        # Check for scoring conditions
        if self.red_circle_overlap_timer >= SCORE_OVERLAP_FRAMES:
            self.red_player_score += 1
            self._respawn_blue_square()
            self.red_circle_overlap_timer = 0

        if self.purple_circle_overlap_timer >= SCORE_OVERLAP_FRAMES:
            self.purple_player_score += 1
            self._respawn_blue_square()
            self.purple_circle_overlap_timer = 0

    def _respawn_blue_square(self):
        """Respawn the blue square at the center of the grid."""
        self.blue_square.x = BLUE_SQUARE_RESPAWN_X
        self.blue_square.y = BLUE_SQUARE_RESPAWN_Y
        self.blue_square.velocity_x = 0.0
        self.blue_square.velocity_y = 0.0
        self.blue_square.angular_velocity = 0.0

    def get_red_player_score(self):
        """Get the red player's score."""
        return self.red_player_score

    def get_purple_player_score(self):
        """Get the purple player's score."""
        return self.purple_player_score
