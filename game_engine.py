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
    CentralGravitationalDot,
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
        self.central_gravity_dot = CentralGravitationalDot()

        # Scoring system
        self.red_player_score = 0
        self.purple_player_score = 0
        self.red_circle_overlap_timer = (
            0  # Frames blue square has been fully inside red circle
        )
        self.purple_circle_overlap_timer = (
            0  # Frames blue square has been fully inside purple circle
        )

        # Hit Points system
        self.red_player_hp = INITIAL_HIT_POINTS
        self.purple_player_hp = INITIAL_HIT_POINTS

        # Collision tracking to prevent multiple damage from same collision
        self.red_dot_collision_cooldown = 0
        self.purple_dot_collision_cooldown = 0
        self.collision_cooldown_frames = 30  # 0.5 seconds at 60 FPS

        # Input states for both players
        self.player1_keys = set()  # Arrow keys + Enter
        self.player2_keys = set()  # WASD + Ctrl

        # Gamepad manager reference (set by split screen view)
        self._gamepad_manager = None

        # Gamepad button state tracking (to detect button press/release)
        self.gamepad1_shoot_pressed = False
        self.gamepad2_shoot_pressed = False

    def set_gamepad_manager(self, gamepad_manager):
        """Set the gamepad manager reference."""
        self._gamepad_manager = gamepad_manager

    def create_purple_dot(self):
        """Create the purple dot for player 2 if it doesn't exist."""
        if self.purple_dot is None:
            # Use PurpleDot's default starting position (in red circle goal)
            self.purple_dot = PurpleDot()

    def update_game_state(self):
        """Update all game objects - called every frame."""
        self._handle_input()
        self._update_physics()
        self._handle_collisions()
        self._update_hit_points()
        self._update_scoring()

    def _handle_input(self):
        """Process input for both players."""
        # Update gamepad manager if available
        if hasattr(self, "_gamepad_manager") and self._gamepad_manager:
            self._gamepad_manager.update()

        # Player 1 (Red dot) - Check gamepad first, then keyboard fallback
        gamepad_controlling_player1 = (
            hasattr(self, "_gamepad_manager")
            and self._gamepad_manager
            and GAMEPAD_ENABLED
            and self._gamepad_manager.is_gamepad_connected(GAMEPAD_1_INDEX)
        )

        if gamepad_controlling_player1:
            # Use gamepad input for Player 1
            gamepad1_input = self._gamepad_manager.get_gamepad_input(GAMEPAD_1_INDEX)
            self.red_dot.acceleration_x = (
                gamepad1_input["left_stick_x"] * ANALOG_STICK_MULTIPLIER
            )
            self.red_dot.acceleration_y = (
                gamepad1_input["left_stick_y"] * ANALOG_STICK_MULTIPLIER
            )

            # Handle shoot button
            if gamepad1_input["shoot_button"] and not self.gamepad1_shoot_pressed:
                self.shoot_projectile_player1()
                self.gamepad1_shoot_pressed = True
            elif not gamepad1_input["shoot_button"]:
                self.gamepad1_shoot_pressed = False
        else:
            # Use keyboard input for Player 1
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

        # Player 2 (Purple dot) - Check gamepad first, then keyboard fallback
        if self.purple_dot is not None:
            gamepad_controlling_player2 = (
                hasattr(self, "_gamepad_manager")
                and self._gamepad_manager
                and GAMEPAD_ENABLED
                and self._gamepad_manager.is_gamepad_connected(GAMEPAD_2_INDEX)
            )

            if gamepad_controlling_player2:
                # Use gamepad input for Player 2
                gamepad2_input = self._gamepad_manager.get_gamepad_input(
                    GAMEPAD_2_INDEX
                )
                self.purple_dot.acceleration_x = (
                    gamepad2_input["left_stick_x"] * ANALOG_STICK_MULTIPLIER
                )
                self.purple_dot.acceleration_y = (
                    gamepad2_input["left_stick_y"] * ANALOG_STICK_MULTIPLIER
                )

                # Handle shoot button
                if gamepad2_input["shoot_button"] and not self.gamepad2_shoot_pressed:
                    self.shoot_projectile_player2()
                    self.gamepad2_shoot_pressed = True
                elif not gamepad2_input["shoot_button"]:
                    self.gamepad2_shoot_pressed = False
            else:
                # Use keyboard input for Player 2
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
        # Blue square collisions (check for hit point damage)
        if self.blue_square.check_collision_with_dot(self.red_dot):
            self._damage_player("red", "blue_square")
        if self.purple_dot is not None:
            if self.blue_square.check_collision_with_dot(self.purple_dot):
                self._damage_player("purple", "blue_square")

        # Projectile collisions (check for hit point damage)
        for projectile in self.projectiles:
            if projectile.is_active:
                projectile.check_collision_with_square(self.blue_square)
                if projectile.check_collision_with_dot(self.red_dot, "red"):
                    self._damage_player("red", "projectile")
                if self.purple_dot is not None:
                    if projectile.check_collision_with_dot(self.purple_dot, "purple"):
                        self._damage_player("purple", "projectile")

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
            # Apply hit point damage first before separation
            self._damage_player("red", "player_collision")
            self._damage_player("purple", "player_collision")

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

        # Apply gravity from central gravitational dot
        self.central_gravity_dot.apply_gravity_to_object(self.blue_square)

    def _damage_player(self, player, damage_source):
        """Apply damage to a player if not on cooldown."""
        if player == "red" and self.red_dot_collision_cooldown <= 0:
            self.red_player_hp -= HIT_POINT_DAMAGE
            self.red_dot_collision_cooldown = self.collision_cooldown_frames
            self.red_dot.trigger_hp_damage_pulse()  # Trigger yellow pulse effect
            print(f"Red player hit by {damage_source}! HP: {self.red_player_hp}")
        elif player == "purple" and self.purple_dot_collision_cooldown <= 0:
            self.purple_player_hp -= HIT_POINT_DAMAGE
            self.purple_dot_collision_cooldown = self.collision_cooldown_frames
            if self.purple_dot is not None:
                self.purple_dot.trigger_hp_damage_pulse()  # Trigger yellow pulse effect
            print(f"Purple player hit by {damage_source}! HP: {self.purple_player_hp}")

    def _update_hit_points(self):
        """Update hit point system and check for boundary collisions."""
        # Update collision cooldowns
        if self.red_dot_collision_cooldown > 0:
            self.red_dot_collision_cooldown -= 1
        if self.purple_dot_collision_cooldown > 0:
            self.purple_dot_collision_cooldown -= 1

        # Check for boundary collisions
        self._check_boundary_collisions()

        # Check for HP depletion
        if self.red_player_hp <= 0:
            self.purple_player_score += 1
            self._reset_player_hp()
            print(
                f"Purple player scores from red HP depletion! Score: {self.purple_player_score}"
            )
        elif self.purple_player_hp <= 0:
            self.red_player_score += 1
            self._reset_player_hp()
            print(
                f"Red player scores from purple HP depletion! Score: {self.red_player_score}"
            )

    def _check_boundary_collisions(self):
        """Check if players hit the circular boundary and apply damage."""
        # Check red player boundary collision
        red_distance_from_center = math.sqrt(
            self.red_dot.virtual_x**2 + self.red_dot.virtual_y**2
        )
        if red_distance_from_center + self.red_dot.radius >= GRID_RADIUS:
            self._damage_player("red", "boundary")

        # Check purple player boundary collision
        if self.purple_dot is not None:
            purple_distance_from_center = math.sqrt(
                self.purple_dot.virtual_x**2 + self.purple_dot.virtual_y**2
            )
            if purple_distance_from_center + self.purple_dot.radius >= GRID_RADIUS:
                self._damage_player("purple", "boundary")

    def _reset_player_hp(self):
        """Reset both players' HP to initial values."""
        self.red_player_hp = INITIAL_HIT_POINTS
        self.purple_player_hp = INITIAL_HIT_POINTS
        self.red_dot_collision_cooldown = 0
        self.purple_dot_collision_cooldown = 0

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

        # Check for scoring conditions (award 2 points for static circle scoring)
        if self.red_circle_overlap_timer >= SCORE_OVERLAP_FRAMES:
            self.red_player_score += STATIC_CIRCLE_SCORE_POINTS
            self._respawn_blue_square()
            self.red_circle_overlap_timer = 0
            print(
                f"Red player scores {STATIC_CIRCLE_SCORE_POINTS} points! Total: {self.red_player_score}"
            )

        if self.purple_circle_overlap_timer >= SCORE_OVERLAP_FRAMES:
            self.purple_player_score += STATIC_CIRCLE_SCORE_POINTS
            self._respawn_blue_square()
            self.purple_circle_overlap_timer = 0
            print(
                f"Purple player scores {STATIC_CIRCLE_SCORE_POINTS} points! Total: {self.purple_player_score}"
            )

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

    def get_red_player_hp(self):
        """Get the red player's hit points."""
        return self.red_player_hp

    def get_purple_player_hp(self):
        """Get the purple player's hit points."""
        return self.purple_player_hp
