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
from rate_limiter import ProjectileRateLimiter
import math


class GameEngine:
    def _calculate_collision_volume(
        self,
        obj1_vel_x,
        obj1_vel_y,
        obj2_vel_x,
        obj2_vel_y,
        base_volume=1.0,
        max_volume=1.0,
    ):
        """
        Calculate collision volume based on relative velocities.

        Args:
            obj1_vel_x, obj1_vel_y: Velocity of first object
            obj2_vel_x, obj2_vel_y: Velocity of second object
            base_volume: Minimum volume (0.0 to 1.0)
            max_volume: Maximum volume (0.0 to 1.0)

        Returns:
            float: Volume level between base_volume and max_volume
        """
        # Calculate relative velocity magnitude
        rel_vel_x = obj1_vel_x - obj2_vel_x
        rel_vel_y = obj1_vel_y - obj2_vel_y
        relative_speed = math.sqrt(rel_vel_x * rel_vel_x + rel_vel_y * rel_vel_y)

        # Define speed thresholds for volume scaling
        min_speed = 50.0  # Below this, use base volume
        max_speed = 500.0  # Above this, use max volume

        # Calculate volume based on relative speed
        if relative_speed <= min_speed:
            return base_volume
        elif relative_speed >= max_speed:
            return max_volume
        else:
            # Linear interpolation between base and max volume
            speed_ratio = (relative_speed - min_speed) / (max_speed - min_speed)
            return base_volume + (max_volume - base_volume) * speed_ratio

    def _play_collision_sound(
        self,
        sound_effect,
        obj1_vel_x,
        obj1_vel_y,
        obj2_vel_x=0.0,
        obj2_vel_y=0.0,
        base_volume=0.3,
    ):
        """
        Play a collision sound with volume modulated by relative velocities.

        Args:
            sound_effect: The pygame sound object to play
            obj1_vel_x, obj1_vel_y: Velocity of first object
            obj2_vel_x, obj2_vel_y: Velocity of second object (default 0 for stationary)
            base_volume: Base volume level (0.0 to 1.0)
        """
        try:
            import builtins

            if hasattr(builtins, sound_effect) and getattr(builtins, sound_effect):
                sound = getattr(builtins, sound_effect)
                volume = self._calculate_collision_volume(
                    obj1_vel_x,
                    obj1_vel_y,
                    obj2_vel_x,
                    obj2_vel_y,
                    base_volume=base_volume,
                )
                sound.set_volume(volume)
                sound.play()
            else:
                pass  # Sound not found or None - silent fail
        except Exception:
            pass  # Silent fail for sound errors

    def _handle_projectile_collisions(self):
        """Check and resolve collisions between all active projectiles."""
        from physics import PhysicsEngine

        projectiles = self.projectiles
        n = len(projectiles)
        for i in range(n):
            p1 = projectiles[i]
            if not p1.is_active:
                continue
            for j in range(i + 1, n):
                p2 = projectiles[j]
                if not p2.is_active:
                    continue
                # Prevent interaction if both projectiles were just launched and are still overlapping (multi-shot)
                if getattr(p1, "just_launched", False) and getattr(
                    p2, "just_launched", False
                ):
                    # Only allow interaction if they are no longer overlapping
                    dx = p2.x - p1.x
                    dy = p2.y - p1.y
                    dist_sq = dx * dx + dy * dy
                    min_dist = p1.radius + p2.radius
                    if dist_sq < min_dist * min_dist:
                        continue  # Still grouped, skip collision
                    else:
                        # Once separated, mark as no longer just launched
                        p1.just_launched = False
                        p2.just_launched = False
                # Check for collision (circle-circle)
                dx = p2.x - p1.x
                dy = p2.y - p1.y
                dist_sq = dx * dx + dy * dy
                min_dist = p1.radius + p2.radius
                if dist_sq < min_dist * min_dist:
                    dist = math.sqrt(dist_sq) if dist_sq > 0 else 1e-6
                    # Normal vector
                    nx = dx / dist
                    ny = dy / dist
                    # Move projectiles apart to prevent overlap
                    overlap = min_dist - dist
                    p1.x -= nx * (overlap / 2)
                    p1.y -= ny * (overlap / 2)
                    p2.x += nx * (overlap / 2)
                    p2.y += ny * (overlap / 2)
                    # Apply collision response
                    v1x, v1y, v2x, v2y = PhysicsEngine.apply_collision_response(
                        p1.velocity_x,
                        p1.velocity_y,
                        p1.mass,
                        p2.velocity_x,
                        p2.velocity_y,
                        p2.mass,
                        nx,
                        ny,
                    )
                    p1.velocity_x, p1.velocity_y = v1x, v1y
                    p2.velocity_x, p2.velocity_y = v2x, v2y

                    # Play collision sound with volume based on relative velocities
                    self._play_collision_sound(
                        "SFX_LANDHIT",
                        p1.velocity_x,
                        p1.velocity_y,
                        p2.velocity_x,
                        p2.velocity_y,
                    )

    def get_player1_projectile_speed_multiplier(self):
        mult = 1.0
        for p in self.player1_powerups:
            if p == "projectile_speed_50":
                mult *= 1.5
        return mult

    def get_player2_projectile_speed_multiplier(self):
        mult = 1.0
        for p in self.player2_powerups:
            if p == "projectile_speed_50":
                mult *= 1.5
        return mult

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

        # Black hole for additional gravitational dynamics
        from objects import BlackHole

        self.black_hole = BlackHole()

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

        # Boundary collision tracking to prevent sound spam
        self.red_outside_boundary_last_frame = False
        self.purple_outside_boundary_last_frame = False

        # Input states for both players
        self.player1_keys = set()  # Arrow keys + Enter
        self.player2_keys = set()  # WASD + Ctrl

        # Gamepad manager reference (set by split screen view)
        self._gamepad_manager = None

        # Gamepad button state tracking (to detect button press/release)
        self.gamepad1_shoot_pressed = False
        self.gamepad2_shoot_pressed = False

        # Rate limiters for projectile firing
        self.player1_rate_limiter = ProjectileRateLimiter()
        self.player2_rate_limiter = ProjectileRateLimiter()

        # Powerup tracking
        self.player1_powerups = []  # List of powerups earned by Player 1 (Red)
        self.player2_powerups = []  # List of powerups earned by Player 2 (Purple)

        # Score pulse system for visual feedback
        self.score_pulse_active = False
        self.score_pulse_timer = 0
        self.score_pulse_duration = 30  # frames
        self.score_pulse_player = None  # 1 or 2

        # Circle pulse system for goal scoring visual feedback
        self.circle_pulse_active = False
        self.circle_pulse_timer = 0
        self.circle_pulse_duration = 60  # frames (longer than score pulse)
        self.circle_pulse_circle = None  # "red" or "purple"

    def set_gamepad_manager(self, gamepad_manager):
        """Set the gamepad manager reference."""
        self._gamepad_manager = gamepad_manager

    def create_purple_dot(self):
        """Create the purple dot for player 2 if it doesn't exist."""
        if self.purple_dot is None:
            # Use PurpleDot's default starting position (in red circle goal)
            self.purple_dot = PurpleDot()

    def apply_powerup_effects(self):
        # Player 1
        base_rate = 3  # Default starting projectile rate reduced from 5 to 3
        for p in self.player1_powerups:
            if p == "plus_2_projectiles_per_sec":
                base_rate += 2
            if p == "plus_1_projectile_per_sec":
                base_rate += 1
        self.player1_rate_limiter.max_rate = base_rate

        # Player 2
        base_rate2 = 3  # Default starting projectile rate reduced from 5 to 3
        for p in self.player2_powerups:
            if p == "plus_2_projectiles_per_sec":
                base_rate2 += 2
            if p == "plus_1_projectile_per_sec":
                base_rate2 += 1
        self.player2_rate_limiter.max_rate = base_rate2

        # HP bonus
        self.red_player_hp = int(INITIAL_HIT_POINTS * self.get_player1_hp_multiplier())
        self.purple_player_hp = int(
            INITIAL_HIT_POINTS * self.get_player2_hp_multiplier()
        )

        # Mass and gravity effects are handled in helper methods and used in physics/collision logic.

    def get_player1_acceleration(self):
        base = ACCELERATION
        for p in self.player1_powerups:
            if p == "acceleration_50":
                base *= 1.5
        return base

    def get_player2_acceleration(self):
        base = ACCELERATION
        for p in self.player2_powerups:
            if p == "acceleration_50":
                base *= 1.5
        return base

    def get_player1_effective_top_speed(self):
        base = MAX_SPEED
        for p in self.player1_powerups:
            if p == "top_speed_50":
                base *= 1.5
        return base

    def get_player2_effective_top_speed(self):
        base = MAX_SPEED
        for p in self.player2_powerups:
            if p == "top_speed_50":
                base *= 1.5
        return base

    def get_player1_projectile_radius(self):
        base = PROJECTILE_RADIUS
        # Apply all 50% size increases cumulatively
        for p in self.player1_powerups:
            if p == "double_projectile_radius":
                base *= 2
        # Stackable 50% increases
        count_50 = self.player1_powerups.count("projectile_size_50")
        base *= 1.5**count_50
        return base

    def get_player2_projectile_radius(self):
        base = PROJECTILE_RADIUS
        for p in self.player2_powerups:
            if p == "double_projectile_radius":
                base *= 2
        count_50 = self.player2_powerups.count("projectile_size_50")
        base *= 1.5**count_50
        return base

    def get_player1_projectile_damage(self):
        base = 1  # Default projectile damage
        for p in self.player1_powerups:
            if p == "projectile_damage_plus_1":
                base += 1
        return base

    def get_player2_projectile_damage(self):
        base = 1  # Default projectile damage
        for p in self.player2_powerups:
            if p == "projectile_damage_plus_1":
                base += 1
        return base

    def get_player1_projectile_mass(self):
        base = PROJECTILE_MASS
        for p in self.player1_powerups:
            if p == "projectile_mass_50":
                base *= 1.5
        return base

    def get_player2_projectile_mass(self):
        base = PROJECTILE_MASS
        for p in self.player2_powerups:
            if p == "projectile_mass_50":
                base *= 1.5
        return base

    def get_player1_hp_multiplier(self):
        mult = 1.0
        for p in self.player1_powerups:
            if p == "hp_50":
                mult *= 1.5
        return mult

    def get_player2_hp_multiplier(self):
        mult = 1.0
        for p in self.player2_powerups:
            if p == "hp_50":
                mult *= 1.5
        return mult

    def get_player1_dot_mass(self):
        base = DOT_MASS
        for p in self.player1_powerups:
            if p == "dot_mass_50":
                base *= 1.5
        return base

    def get_player2_dot_mass(self):
        base = DOT_MASS
        for p in self.player2_powerups:
            if p == "dot_mass_50":
                base *= 1.5
        return base

    def get_player1_goal_gravity(self):
        base = GRAVITY_STRENGTH
        for p in self.player1_powerups:
            if p == "goal_gravity_50":
                base *= 1.5
        return base

    def get_player2_goal_gravity(self):
        base = GRAVITY_STRENGTH
        for p in self.player2_powerups:
            if p == "goal_gravity_50":
                base *= 1.5
        return base

    def get_player1_num_projectiles(self):
        # Always at least 1, +1 for each double_shot powerup
        return 1 + self.player1_powerups.count("double_shot")

    def get_player2_num_projectiles(self):
        return 1 + self.player2_powerups.count("double_shot")

    def reset_game_state(self):
        """Reset all game state to initial values for a new game."""
        self.red_dot = RedDot()
        self.purple_dot = PurpleDot() if self.purple_dot is not None else None
        self.blue_square = BlueSquare()
        self.projectiles = []
        self.red_gravity_dot = RedGravitationalDot()
        self.purple_gravity_dot = PurpleGravitationalDot()
        self.central_gravity_dot = CentralGravitationalDot()
        self.red_player_score = 0
        self.purple_player_score = 0
        self.red_circle_overlap_timer = 0
        self.purple_circle_overlap_timer = 0
        self.red_player_hp = INITIAL_HIT_POINTS
        self.purple_player_hp = INITIAL_HIT_POINTS
        self.red_dot_collision_cooldown = 0
        self.purple_dot_collision_cooldown = 0
        self.player1_keys = set()
        self.player2_keys = set()
        self.player1_rate_limiter = ProjectileRateLimiter()
        self.player2_rate_limiter = ProjectileRateLimiter()
        self.player1_powerups = []
        self.player2_powerups = []
        # Gamepad state
        self.gamepad1_shoot_pressed = False
        self.gamepad2_shoot_pressed = False
        # Reset score pulse system
        self.reset_score_pulse()
        # Reset circle pulse system
        self.reset_circle_pulse()
        # Keep gamepad manager reference if set
        if hasattr(self, "_gamepad_manager"):
            self.set_gamepad_manager(self._gamepad_manager)
        self.apply_powerup_effects()

    def reset_positions_only(self):
        """Reset player and blue square positions, but keep scores and powerups."""
        self.red_dot = RedDot()
        self.purple_dot = PurpleDot() if self.purple_dot is not None else None
        self.blue_square = BlueSquare()
        self.projectiles = []
        self.red_circle_overlap_timer = 0
        self.purple_circle_overlap_timer = 0
        self.red_player_hp = INITIAL_HIT_POINTS
        self.purple_player_hp = INITIAL_HIT_POINTS
        self.red_dot_collision_cooldown = 0
        self.purple_dot_collision_cooldown = 0
        self.player1_keys = set()
        self.player2_keys = set()
        self.player1_rate_limiter = ProjectileRateLimiter()
        self.player2_rate_limiter = ProjectileRateLimiter()
        # Gamepad state
        self.gamepad1_shoot_pressed = False
        self.gamepad2_shoot_pressed = False
        # Reset score pulse system
        self.reset_score_pulse()
        # Reset circle pulse system
        self.reset_circle_pulse()
        if hasattr(self, "_gamepad_manager"):
            self.set_gamepad_manager(self._gamepad_manager)
        self.apply_powerup_effects()

    """Centralized game logic and state management."""

    def update_game_state(self):
        """Update all game objects - called every frame."""
        self._handle_input()
        self._update_physics()
        self._handle_collisions()
        self._update_hit_points()
        self._update_scoring()
        self.update_score_pulse()  # Update score pulse effects
        self.update_circle_pulse()  # Update circle pulse effects

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
            # print(f"[DEBUG] Player 1 gamepad input: {gamepad1_input}")  # Debug print
            max_speed = self.get_player1_effective_top_speed()
            self.red_dot.acceleration_x = (
                gamepad1_input["left_stick_x"] * ANALOG_STICK_MULTIPLIER
            )
            self.red_dot.acceleration_y = (
                gamepad1_input["left_stick_y"] * ANALOG_STICK_MULTIPLIER
            )
            # Clamp velocity to max_speed
            speed = math.sqrt(self.red_dot.velocity_x**2 + self.red_dot.velocity_y**2)
            if speed > max_speed:
                scale = max_speed / speed
                self.red_dot.velocity_x *= scale
                self.red_dot.velocity_y *= scale
            # Handle projectile firing with 'A' button (shoot_button)
            a_pressed = gamepad1_input.get("shoot_button", 0) == 1
            if a_pressed and not self.gamepad1_shoot_pressed:
                self.shoot_projectile_player1()
            self.gamepad1_shoot_pressed = a_pressed
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
            # Keyboard firing (e.g., Enter key)
            if (
                Qt.Key.Key_Return in self.player1_keys
                or Qt.Key.Key_Enter in self.player1_keys
            ):
                self.shoot_projectile_player1()

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
                # print(f"[DEBUG] Player 2 gamepad input: {gamepad2_input}")  # Debug print
                max_speed2 = self.get_player2_effective_top_speed()
                self.purple_dot.acceleration_x = (
                    gamepad2_input["left_stick_x"] * ANALOG_STICK_MULTIPLIER
                )
                self.purple_dot.acceleration_y = (
                    gamepad2_input["left_stick_y"] * ANALOG_STICK_MULTIPLIER
                )
                speed2 = math.sqrt(
                    self.purple_dot.velocity_x**2 + self.purple_dot.velocity_y**2
                )
                if speed2 > max_speed2:
                    scale2 = max_speed2 / speed2
                    self.purple_dot.velocity_x *= scale2
                    self.purple_dot.velocity_y *= scale2
                # Handle projectile firing with 'A' button (shoot_button)
                a_pressed2 = gamepad2_input.get("shoot_button", 0) == 1
                if a_pressed2 and not self.gamepad2_shoot_pressed:
                    self.shoot_projectile_player2()
                self.gamepad2_shoot_pressed = a_pressed2
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
                # Keyboard firing (e.g., Ctrl key)
                if Qt.Key.Key_Control in self.player2_keys:
                    self.shoot_projectile_player2()

    def _update_physics(self):
        """Update physics for all objects."""
        self.red_dot.update_physics()
        if self.purple_dot is not None:
            self.purple_dot.update_physics()
        self.blue_square.update_physics()

        # Update black hole physics
        self.black_hole.update_physics()

        # Apply gravitational forces to the blue square
        self._apply_gravitational_forces()

        # Apply black hole gravity to players
        self.black_hole.apply_gravity_to_object(self.red_dot)
        if self.purple_dot is not None:
            self.black_hole.apply_gravity_to_object(self.purple_dot)

        # Update projectile physics and apply gravity to each projectile
        for projectile in self.projectiles[
            :
        ]:  # Use slice copy to safely modify during iteration
            # Apply gravitational forces to projectiles
            self._apply_gravitational_forces_to_projectile(projectile)
            projectile.update_physics()
            if not projectile.is_active:
                self.projectiles.remove(projectile)

    def _handle_collisions(self):
        """Check and resolve collisions between objects."""
        # Blue square collisions (check for hit point damage)
        if self.blue_square.check_collision_with_dot(self.red_dot):
            # Play sound for red player hitting blue square with volume based on collision speed
            self._play_collision_sound(
                "SFX_DEFAULTHIT",
                self.red_dot.velocity_x,
                self.red_dot.velocity_y,
                self.blue_square.velocity_x,
                self.blue_square.velocity_y,
            )
            self._damage_player("red", "blue_square")
        if self.purple_dot is not None:
            if self.blue_square.check_collision_with_dot(self.purple_dot):
                # Play sound for purple player hitting blue square with volume based on collision speed
                self._play_collision_sound(
                    "SFX_DEFAULTHIT",
                    self.purple_dot.velocity_x,
                    self.purple_dot.velocity_y,
                    self.blue_square.velocity_x,
                    self.blue_square.velocity_y,
                )
                self._damage_player("purple", "blue_square")

        # Projectile collisions (check for hit point damage)
        for projectile in self.projectiles:
            if projectile.is_active:
                if projectile.check_collision_with_square(self.blue_square):
                    # Play sound for projectile hitting blue cube with volume based on collision speed
                    self._play_collision_sound(
                        "SFX_ENEMYBLOCK",
                        projectile.velocity_x,
                        projectile.velocity_y,
                        self.blue_square.velocity_x,
                        self.blue_square.velocity_y,
                    )
                if projectile.check_collision_with_dot(self.red_dot, "red"):
                    # Play sound for projectile hitting red player with volume based on collision speed
                    self._play_collision_sound(
                        "SFX_LANDHIT",
                        projectile.velocity_x,
                        projectile.velocity_y,
                        self.red_dot.velocity_x,
                        self.red_dot.velocity_y,
                    )
                    self._damage_player("red", "projectile")
                if self.purple_dot is not None:
                    if projectile.check_collision_with_dot(self.purple_dot, "purple"):
                        # Play sound for projectile hitting purple player with volume based on collision speed
                        self._play_collision_sound(
                            "SFX_LANDHIT",
                            projectile.velocity_x,
                            projectile.velocity_y,
                            self.purple_dot.velocity_x,
                            self.purple_dot.velocity_y,
                        )
                        self._damage_player("purple", "projectile")

        # Projectile vs projectile collisions
        self._handle_projectile_collisions()

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

                # Play collision sound with volume based on relative velocities
                self._play_collision_sound(
                    "SFX_LANDHIT",
                    self.red_dot.velocity_x,
                    self.red_dot.velocity_y,
                    self.purple_dot.velocity_x,
                    self.purple_dot.velocity_y,
                )

    def shoot_projectile_player1(self):
        """Create and add a projectile for player 1 (red dot)."""
        if len(self.projectiles) >= PROJECTILE_MAX_COUNT:
            return

        # Check rate limiter
        if not self.player1_rate_limiter.can_fire():
            return

        num_projectiles = self.get_player1_num_projectiles()
        # Calculate base direction
        speed = math.sqrt(self.red_dot.velocity_x**2 + self.red_dot.velocity_y**2)
        if speed < 0.1:
            return
        direction_x = self.red_dot.velocity_x / speed
        direction_y = self.red_dot.velocity_y / speed
        base_angle = math.atan2(direction_y, direction_x)
        spread_deg = 2.0  # 2 degrees between each projectile
        spread_rad = math.radians(spread_deg)
        # Center the spread
        start_angle = base_angle - (spread_rad * (num_projectiles - 1) / 2)
        speed_mult = self.get_player1_projectile_speed_multiplier()
        for i in range(num_projectiles):
            angle = start_angle + i * spread_rad
            dx = math.cos(angle)
            dy = math.sin(angle)
            # Vary speed across the arc: center is fastest, edges are slower
            if num_projectiles > 1:
                center_index = (num_projectiles - 1) / 2
                distance_from_center = (
                    abs(i - center_index) / center_index
                )  # 0 at center, 1 at edge
            else:
                distance_from_center = 0
            speed_factor = (
                1.0 - 0.3 * distance_from_center
            )  # 1.0 at center, 0.7 at edge
            projectile_speed = (
                (PROJECTILE_MIN_SPEED + speed) * speed_mult * speed_factor
            )
            # Place each projectile just outside the player's dot, separated by 1 degree
            launch_distance = self.red_dot.radius + 1.0  # 1px margin to avoid overlap
            launch_x = self.red_dot.virtual_x + dx * launch_distance
            launch_y = self.red_dot.virtual_y + dy * launch_distance
            projectile_vel_x = dx * projectile_speed
            projectile_vel_y = dy * projectile_speed
            from objects import Projectile

            new_projectile = Projectile(
                launch_x,
                launch_y,
                projectile_vel_x,
                projectile_vel_y,
                "red",
            )
            new_projectile.radius = self.get_player1_projectile_radius()
            new_projectile.damage = self.get_player1_projectile_damage()
            new_projectile.mass = self.get_player1_projectile_mass()
            self.projectiles.append(new_projectile)
        # Play projectile fire sound effect
        try:
            import builtins

            if hasattr(builtins, "SFX_LASERBLAST") and builtins.SFX_LASERBLAST:
                builtins.SFX_LASERBLAST.play()
        except Exception:
            pass
        self.player1_rate_limiter.record_shot()

    def shoot_projectile_player2(self):
        """Create and add a projectile for player 2 (purple dot)."""
        if self.purple_dot is None or len(self.projectiles) >= PROJECTILE_MAX_COUNT:
            return

        # Check rate limiter
        if not self.player2_rate_limiter.can_fire():
            return

        num_projectiles = self.get_player2_num_projectiles()
        # Calculate base direction
        speed = math.sqrt(self.purple_dot.velocity_x**2 + self.purple_dot.velocity_y**2)
        if speed < 0.1:
            return
        direction_x = self.purple_dot.velocity_x / speed
        direction_y = self.purple_dot.velocity_y / speed
        base_angle = math.atan2(direction_y, direction_x)
        spread_deg = 2.0  # 2 degrees between each projectile
        spread_rad = math.radians(spread_deg)
        # Center the spread
        start_angle = base_angle - (spread_rad * (num_projectiles - 1) / 2)
        speed_mult = self.get_player2_projectile_speed_multiplier()
        for i in range(num_projectiles):
            angle = start_angle + i * spread_rad
            dx = math.cos(angle)
            dy = math.sin(angle)
            # Vary speed across the arc: center is fastest, edges are slower
            if num_projectiles > 1:
                center_index = (num_projectiles - 1) / 2
                distance_from_center = (
                    abs(i - center_index) / center_index
                )  # 0 at center, 1 at edge
            else:
                distance_from_center = 0
            speed_factor = (
                1.0 - 0.3 * distance_from_center
            )  # 1.0 at center, 0.7 at edge
            projectile_speed = (
                (PROJECTILE_MIN_SPEED + speed) * speed_mult * speed_factor
            )
            # Place each projectile just outside the player's dot, separated by 1 degree
            launch_distance = (
                self.purple_dot.radius + 1.0
            )  # 1px margin to avoid overlap
            launch_x = self.purple_dot.virtual_x + dx * launch_distance
            launch_y = self.purple_dot.virtual_y + dy * launch_distance
            projectile_vel_x = dx * projectile_speed
            projectile_vel_y = dy * projectile_speed
            from objects import Projectile

            new_projectile = Projectile(
                launch_x,
                launch_y,
                projectile_vel_x,
                projectile_vel_y,
                "purple",
            )
            new_projectile.radius = self.get_player2_projectile_radius()
            new_projectile.damage = self.get_player2_projectile_damage()
            new_projectile.mass = self.get_player2_projectile_mass()
            self.projectiles.append(new_projectile)
        # Play projectile fire sound effect
        try:
            import builtins

            if hasattr(builtins, "SFX_LASERBLAST") and builtins.SFX_LASERBLAST:
                builtins.SFX_LASERBLAST.play()
        except Exception:
            pass
        self.player2_rate_limiter.record_shot()

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
        # Set goal gravity strengths based on player powerups
        self.red_gravity_dot.strength = self.get_player1_goal_gravity()
        self.purple_gravity_dot.strength = self.get_player2_goal_gravity()

        # Apply gravity from red gravitational dot
        self.red_gravity_dot.apply_gravity_to_object(self.blue_square)

        # Apply gravity from purple gravitational dot
        self.purple_gravity_dot.apply_gravity_to_object(self.blue_square)

        # Apply gravity from central gravitational dot
        self.central_gravity_dot.apply_gravity_to_object(self.blue_square)

        # Apply powerful gravity from black hole
        self.black_hole.apply_gravity_to_object(self.blue_square)

    def _apply_gravitational_forces_to_projectile(self, projectile):
        """Apply gravitational forces from the gravitational dots to a projectile."""
        # Set goal gravity strengths based on player powerups
        self.red_gravity_dot.strength = self.get_player1_goal_gravity()
        self.purple_gravity_dot.strength = self.get_player2_goal_gravity()

        # Apply gravity from red gravitational dot
        self.red_gravity_dot.apply_gravity_to_object(projectile)

        # Apply gravity from purple gravitational dot
        self.purple_gravity_dot.apply_gravity_to_object(projectile)

        # Apply gravity from central gravitational dot
        self.central_gravity_dot.apply_gravity_to_object(projectile)

        # Apply powerful gravity from black hole
        self.black_hole.apply_gravity_to_object(projectile)

    def _damage_player(self, player, damage_source):
        """Apply damage to a player if not on cooldown."""
        if player == "red" and self.red_dot_collision_cooldown <= 0:
            self.red_player_hp -= HIT_POINT_DAMAGE
            self.red_dot_collision_cooldown = self.collision_cooldown_frames
            self.red_dot.trigger_hp_damage_pulse()  # Trigger yellow pulse effect
            # print(f"Red player hit by {damage_source}! HP: {self.red_player_hp}")
        elif player == "purple" and self.purple_dot_collision_cooldown <= 0:
            self.purple_player_hp -= HIT_POINT_DAMAGE
            self.purple_dot_collision_cooldown = self.collision_cooldown_frames
            if self.purple_dot is not None:
                self.purple_dot.trigger_hp_damage_pulse()  # Trigger yellow pulse effect
            # print(f"Purple player hit by {damage_source}! HP: {self.purple_player_hp}")

    def _update_hit_points(self):
        """Update hit point system and check for boundary collisions."""
        # Update collision cooldowns
        if self.red_dot_collision_cooldown > 0:
            self.red_dot_collision_cooldown -= 1
        if self.purple_dot_collision_cooldown > 0:
            self.purple_dot_collision_cooldown -= 1

        # Check for boundary collisions - now handled in physics layer
        # No need for separate boundary collision checking since physics handles bouncing and sound

        # Check for HP depletion
        if self.red_player_hp <= 0:
            # Play selfdestruct sound for red player death
            try:
                import builtins

                if hasattr(builtins, "SFX_SELFDESTRUCT") and builtins.SFX_SELFDESTRUCT:
                    builtins.SFX_SELFDESTRUCT.play()
            except Exception:
                pass
            self.purple_player_score += 1  # HP depletion = 1 point
            self.trigger_score_pulse(2)  # Trigger purple player score pulse
            self._reset_player_hp()
            # print(
            #     f"Purple player scores 1 point from red HP depletion! Score: {self.purple_player_score}")
        elif self.purple_player_hp <= 0:
            # Play selfdestruct sound for purple player death
            try:
                import builtins

                if hasattr(builtins, "SFX_SELFDESTRUCT") and builtins.SFX_SELFDESTRUCT:
                    builtins.SFX_SELFDESTRUCT.play()
            except Exception:
                pass
            self.red_player_score += 1  # HP depletion = 1 point
            self.trigger_score_pulse(1)  # Trigger red player score pulse
            self._reset_player_hp()
            # print(
            #     f"Red player scores 1 point from purple HP depletion! Score: {self.red_player_score}")

    def _check_boundary_collisions(self):
        """Check if players hit the elliptical boundary and apply damage."""
        from config import GRID_RADIUS_X, GRID_RADIUS_Y

        # Check red player boundary collision
        red_ellipse_val = (self.red_dot.virtual_x / GRID_RADIUS_X) ** 2 + (
            self.red_dot.virtual_y / GRID_RADIUS_Y
        ) ** 2
        red_outside_boundary = red_ellipse_val > 1.0

        if red_outside_boundary:
            # Only play sound when first crossing the boundary (not every frame while outside)
            if not self.red_outside_boundary_last_frame:
                print(
                    f"DEBUG: Red player boundary collision! Position: ({self.red_dot.virtual_x:.1f}, {self.red_dot.virtual_y:.1f}), Speed: ({self.red_dot.velocity_x:.1f}, {self.red_dot.velocity_y:.1f})"
                )
                # Play boundary collision sound with volume based on player speed
                self._play_collision_sound(
                    "SFX_FREESHIELD",
                    self.red_dot.velocity_x,
                    self.red_dot.velocity_y,
                    0.0,
                    0.0,
                    base_volume=0.7,  # Increased base volume for boundary collisions
                )  # Boundary is stationary
            self._damage_player("red", "boundary")

        # Update boundary state for next frame
        self.red_outside_boundary_last_frame = red_outside_boundary

        # Check purple player boundary collision
        if self.purple_dot is not None:
            purple_ellipse_val = (self.purple_dot.virtual_x / GRID_RADIUS_X) ** 2 + (
                self.purple_dot.virtual_y / GRID_RADIUS_Y
            ) ** 2
            purple_outside_boundary = purple_ellipse_val > 1.0

            if purple_outside_boundary:
                # Only play sound when first crossing the boundary (not every frame while outside)
                if not self.purple_outside_boundary_last_frame:
                    # Play boundary collision sound with volume based on player speed
                    self._play_collision_sound(
                        "SFX_FREESHIELD",
                        self.purple_dot.velocity_x,
                        self.purple_dot.velocity_y,
                        0.0,
                        0.0,
                        base_volume=0.7,  # Increased base volume for boundary collisions
                    )  # Boundary is stationary
                self._damage_player("purple", "boundary")

            # Update boundary state for next frame
            self.purple_outside_boundary_last_frame = purple_outside_boundary

    def _reset_player_hp(self):
        """Reset both players' HP to initial values."""
        self.red_player_hp = INITIAL_HIT_POINTS
        self.purple_player_hp = INITIAL_HIT_POINTS
        self.red_dot_collision_cooldown = 0
        self.purple_dot_collision_cooldown = 0
        # Reset boundary collision state tracking
        self.red_outside_boundary_last_frame = False
        self.purple_outside_boundary_last_frame = False

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
            self.red_player_score += 2  # Goal = 2 points
            self.trigger_circle_pulse("red")  # Trigger red circle pulse
            self._respawn_blue_square()
            self.projectiles.clear()  # Remove all projectiles after a goal
            self.red_circle_overlap_timer = 0
            # Play goal scored sound effect
            try:
                import builtins

                if hasattr(builtins, "SFX_ENEMYALERT") and builtins.SFX_ENEMYALERT:
                    builtins.SFX_ENEMYALERT.play()
            except Exception:
                pass
            # print(
            #     f"Red player scores 2 points for a goal! Total: {self.red_player_score}")

        if self.purple_circle_overlap_timer >= SCORE_OVERLAP_FRAMES:
            self.purple_player_score += 2  # Goal = 2 points
            self.trigger_circle_pulse("purple")  # Trigger purple circle pulse
            self._respawn_blue_square()
            self.projectiles.clear()  # Remove all projectiles after a goal
            self.purple_circle_overlap_timer = 0
            # Play goal scored sound effect
            try:
                import builtins

                if hasattr(builtins, "SFX_ENEMYALERT") and builtins.SFX_ENEMYALERT:
                    builtins.SFX_ENEMYALERT.play()
            except Exception:
                pass
            # print(
            #     f"Purple player scores 2 points for a goal! Total: {self.purple_player_score}")

    def _respawn_blue_square(self):
        """Respawn the blue square at the center of the grid."""
        self.blue_square.x = BLUE_SQUARE_RESPAWN_X
        self.blue_square.y = BLUE_SQUARE_RESPAWN_Y
        self.blue_square.velocity_x = 0.0
        self.blue_square.velocity_y = 0.0
        self.blue_square.angular_velocity = 0.0

    def trigger_score_pulse(self, player_number):
        """Trigger a score pulse effect for visual feedback."""
        self.score_pulse_active = True
        self.score_pulse_timer = 0
        self.score_pulse_player = player_number

    def update_score_pulse(self):
        """Update the score pulse timer."""
        if self.score_pulse_active:
            self.score_pulse_timer += 1
            if self.score_pulse_timer >= self.score_pulse_duration:
                self.score_pulse_active = False
                self.score_pulse_timer = 0
                self.score_pulse_player = None

    def get_score_pulse_state(self):
        """Get the current score pulse state for rendering."""
        return {
            "active": self.score_pulse_active,
            "timer": self.score_pulse_timer,
            "duration": self.score_pulse_duration,
            "player": self.score_pulse_player,
        }

    def reset_score_pulse(self):
        """Reset the score pulse system."""
        self.score_pulse_active = False
        self.score_pulse_timer = 0
        self.score_pulse_player = None

    def trigger_circle_pulse(self, circle_color):
        """Trigger a circle pulse effect for visual feedback."""
        self.circle_pulse_active = True
        self.circle_pulse_timer = 0
        self.circle_pulse_circle = circle_color

    def update_circle_pulse(self):
        """Update the circle pulse timer."""
        if self.circle_pulse_active:
            self.circle_pulse_timer += 1
            if self.circle_pulse_timer >= self.circle_pulse_duration:
                self.circle_pulse_active = False
                self.circle_pulse_timer = 0
                self.circle_pulse_circle = None

    def get_circle_pulse_state(self):
        """Get the current circle pulse state for rendering."""
        return {
            "active": self.circle_pulse_active,
            "timer": self.circle_pulse_timer,
            "duration": self.circle_pulse_duration,
            "circle": self.circle_pulse_circle,
        }

    def reset_circle_pulse(self):
        """Reset the circle pulse system."""
        self.circle_pulse_active = False
        self.circle_pulse_timer = 0
        self.circle_pulse_circle = None

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

    def get_player1_rate_limiter_progress(self):
        """Get Player 1's rate limiter progress for UI display."""
        return self.player1_rate_limiter.get_progress()

    def get_player2_rate_limiter_progress(self):
        """Get Player 2's rate limiter progress for UI display."""
        return self.player2_rate_limiter.get_progress()

    def get_player1_effective_top_speed(self):
        base = MAX_SPEED
        for p in self.player1_powerups:
            if p == "top_speed_50":
                base *= 1.5
        return base

    def get_player2_effective_top_speed(self):
        base = MAX_SPEED
        for p in self.player2_powerups:
            if p == "top_speed_50":
                base *= 1.5
        return base

    def get_player1_projectile_radius(self):
        base = PROJECTILE_RADIUS
        # Apply 50% increase for each 'projectile_size_50' powerup
        for p in self.player1_powerups:
            if p == "double_projectile_radius":
                base *= 2
        for p in self.player1_powerups:
            if p == "projectile_size_50":
                base *= 1.5
        return base

    def get_player2_projectile_radius(self):
        base = PROJECTILE_RADIUS
        # Apply 50% increase for each 'projectile_size_50' powerup
        for p in self.player2_powerups:
            if p == "double_projectile_radius":
                base *= 2
        for p in self.player2_powerups:
            if p == "projectile_size_50":
                base *= 1.5
        return base

    def get_player1_projectiles_per_sec(self):
        base = (
            self.player1_rate_limiter.max_rate
            if hasattr(self.player1_rate_limiter, "max_rate")
            else 5
        )
        for p in self.player1_powerups:
            if p == "plus_2_projectiles_per_sec":
                base += 2
        return base

    def get_player2_projectiles_per_sec(self):
        base = (
            self.player2_rate_limiter.max_rate
            if hasattr(self.player2_rate_limiter, "max_rate")
            else 5
        )
        for p in self.player2_powerups:
            if p == "plus_2_projectiles_per_sec":
                base += 2
        return base
