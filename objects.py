from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
# --- STAR ICON ---
SVG_STAR_ICON = """<svg viewBox=\"0 0 24 24\" width=\"96\" height=\"96\"><polygon points=\"0,12 12,10 24,12 12,14\" fill=\"#FFFFFF\" /><polygon points=\"12,0 10,12 12,24 14,12\" fill=\"#FFFFFF\" /><rect x=\"11\" y=\"11\" width=\"2\" height=\"2\" fill=\"#F0F0F0\" /><rect x=\"7\" y=\"7\" width=\"2\" height=\"2\" fill=\"#E0E0E0\" /><rect x=\"15\" y=\"7\" width=\"2\" height=\"2\" fill=\"#E0E0E0\" /><rect x=\"7\" y=\"15\" width=\"2\" height=\"2\" fill=\"#E0E0E0\" /><rect x=\"15\" y=\"15\" width=\"2\" height=\"2\" fill=\"#E0E0E0\" /></svg>"""
"""
Game object classes for the Topographical Plane application.
Contains the RedDot and BlueSquare classes with their properties and behaviors.
"""

import math

from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QByteArray, QRectF
from config import *
from physics import PhysicsEngine

# --- SVG ASSET CONSTANTS ---
SVG_RED_SHIP = """<svg viewBox="0 0 24 24" width="96" height="96"><rect x="8" y="2" width="8" height="4" fill="#FF0000" /><rect x="6" y="6" width="12" height="6" fill="#FF0000" /><rect x="4" y="12" width="16" height="4" fill="#FF0000" /><rect x="10" y="8" width="4" height="2" fill="#ADD8E6" /><rect x="6" y="16" width="4" height="4" fill="#8B0000" /><rect x="14" y="16" width="4" height="4" fill="#8B0000" /><rect x="7" y="20" width="2" height="2" fill="#FFA500" /><rect x="15" y="20" width="2" height="2" fill="#FFA500" /></svg>"""
SVG_PURPLE_SHIP = """<svg viewBox="0 0 24 24" width="96" height="96"><rect x="8" y="2" width="8" height="4" fill="#800080" /><rect x="6" y="6" width="12" height="6" fill="#800080" /><rect x="4" y="12" width="16" height="4" fill="#800080" /><rect x="10" y="8" width="4" height="2" fill="#B0E0E6" /><rect x="6" y="16" width="4" height="4" fill="#4B0082" /><rect x="14" y="16" width="4" height="4" fill="#4B0082" /><rect x="7" y="20" width="2" height="2" fill="#FFD700" /><rect x="15" y="20" width="2" height="2" fill="#FFD700" /></svg>"""
SVG_BLUE_CUBE = """<svg viewBox="0 0 24 24" width="96" height="96"><rect x="4" y="8" width="16" height="12" fill="#0000FF" /><polygon points="4,8 8,4 20,4 16,8" fill="#4169E1" /><polygon points="20,4 20,12 16,16 16,8" fill="#0000CD" /><rect x="6" y="10" width="4" height="2" fill="#ADD8E6" /></svg>"""
SVG_RED_GOAL = """<svg viewBox="0 0 24 24" width="96" height="96"><circle cx="12" cy="12" r="10" fill="#000000" /><circle cx="12" cy="12" r="8" fill="#330000" /><circle cx="12" cy="12" r="6" fill="#660000" /><circle cx="12" cy="12" r="4" fill="#990000" /><circle cx="12" cy="12" r="2" fill="#FF0000" /><rect x="10" y="2" width="1" height="1" fill="#FF0000" /><rect x="2" y="10" width="1" height="1" fill="#FF0000" /><rect x="18" y="10" width="1" height="1" fill="#FF0000" /><rect x="10" y="18" width="1" height="1" fill="#FF0000" /></svg>"""
SVG_PURPLE_GOAL = """<svg viewBox="0 0 24 24" width="96" height="96"><circle cx="12" cy="12" r="10" fill="#000000" /><circle cx="12" cy="12" r="8" fill="#330033" /><circle cx="12" cy="12" r="6" fill="#660066" /><circle cx="12" cy="12" r="4" fill="#990099" /><circle cx="12" cy="12" r="2" fill="#800080" /><rect x="10" y="2" width="1" height="1" fill="#800080" /><rect x="2" y="10" width="1" height="1" fill="#800080" /><rect x="18" y="10" width="1" height="1" fill="#800080" /><rect x="10" y="18" width="1" height="1" fill="#800080" /></svg>"""
SVG_PROJECTILE_ICON = """<svg viewBox="0 0 24 24" width="96" height="96"><rect x="10" y="10" width="4" height="4" fill="#FFFF00" /><rect x="8" y="10" width="2" height="4" fill="#FFD700" /><rect x="14" y="10" width="2" height="4" fill="#FFD700" /><rect x="10" y="8" width="4" height="2" fill="#FFD700" /><rect x="10" y="14" width="4" height="2" fill="#FFD700" /><rect x="9" y="9" width="1" height="1" fill="#FFEC8B" /><rect x="14" y="9" width="1" height="1" fill="#FFEC8B" /><rect x="9" y="14" width="1" height="1" fill="#FFEC8B" /><rect x="14" y="14" width="1" height="1" fill="#FFEC8B" /></svg>"""


class RedDot:
    """Represents the movable red dot with momentum physics."""

    def __init__(self, x=RED_PLAYER_INITIAL_X, y=RED_PLAYER_INITIAL_Y):
        # Position (world coordinates)
        self.virtual_x = float(x)
        self.virtual_y = float(y)

        # Physics properties
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.mass = DOT_MASS
        self.radius = DOT_RADIUS

        # Input state
        self.acceleration_x = 0.0
        self.acceleration_y = 0.0

        # Visual effects
        self.pulse_timer = 0  # Timer for HP damage pulse effect

        # SVG Renderer for red ship
        self.svg_renderer = QSvgRenderer(QByteArray(SVG_RED_SHIP.encode("utf-8")))

        # Store last movement angle and size for rendering when stationary
        # At start, orient toward center of gameplay area
        dx = 0 - self.virtual_x
        dy = 0 - self.virtual_y
        if dx == 0 and dy == 0:
            self._last_angle = 180  # Default up
        else:
            self._last_angle = math.degrees(math.atan2(dy, dx)) + 180
        self._last_size = self.radius * 2 * 1.5

    def draw_svg(self, painter, screen_x, screen_y, scale=1.0, angle=None):
        # Draw the SVG centered at (screen_x, screen_y), scaled to 150% of the momentum triangle size, and rotated 180deg from movement
        momentum_info = self.get_momentum_info()
        if momentum_info:
            ship_size = (
                momentum_info["size"] * 2.2 * 1.5
            )  # 50% larger (same for both ships)
            ship_angle = math.degrees(momentum_info["angle"]) + 180
            # Store last movement angle and size
            self._last_angle = ship_angle
            self._last_size = ship_size
        else:
            ship_size = self._last_size
            ship_angle = self._last_angle
        rect = QRectF(-ship_size / 2, -ship_size / 2, ship_size, ship_size)
        painter.save()
        painter.translate(screen_x, screen_y)
        painter.rotate(ship_angle - 90)  # SVG points up, so 0 deg = up
        self.svg_renderer.render(painter, rect)
        painter.restore()

    def update_physics(self):
        """Update velocity and position based on current acceleration."""
        self.velocity_x, self.velocity_y = PhysicsEngine.apply_momentum_physics(
            self.velocity_x, self.velocity_y, self.acceleration_x, self.acceleration_y
        )

        # Update position
        new_x = self.virtual_x + self.velocity_x
        new_y = self.virtual_y + self.velocity_y

        # Check circular boundary
        is_outside, corrected_x, corrected_y, normal_x, normal_y = (
            PhysicsEngine.check_circular_boundary(
                new_x, new_y, self.radius, GRID_RADIUS
            )
        )

        if is_outside:
            self.virtual_x = corrected_x
            self.virtual_y = corrected_y

            # Apply bounce with energy loss
            dot_product = self.velocity_x * normal_x + self.velocity_y * normal_y
            self.velocity_x -= 2 * dot_product * normal_x * BOUNCE_FACTOR
            self.velocity_y -= 2 * dot_product * normal_y * BOUNCE_FACTOR
        else:
            self.virtual_x = new_x
            self.virtual_y = new_y

        # Update pulse timer
        if self.pulse_timer > 0:
            self.pulse_timer -= 1

    def get_screen_position(self):
        """Get the screen position (always at center since camera follows dot)."""
        return WINDOW_CENTER_X, WINDOW_CENTER_Y

    def get_momentum_info(self):
        """Get information for drawing the momentum indicator."""
        speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        if speed < MOMENTUM_MIN_SPEED:
            return None

        angle = math.atan2(self.velocity_y, self.velocity_x)
        triangle_size = min(
            MOMENTUM_MAX_SIZE,
            max(
                MOMENTUM_MIN_SIZE,
                MOMENTUM_MIN_SIZE
                + (speed / MAX_SPEED) * (MOMENTUM_MAX_SIZE - MOMENTUM_MIN_SIZE),
            ),
        )

        return {"angle": angle, "size": triangle_size, "speed": speed}

    def shoot_projectile(self):
        """
        Create a projectile in the direction of momentum.

        Returns:
            Projectile: New projectile instance, or None if not moving
        """
        speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)

        # Only shoot if moving (to determine direction)
        if speed < 0.1:
            return None

        # Calculate projectile direction (same as momentum direction)
        direction_x = self.velocity_x / speed if speed > 0 else 0
        direction_y = self.velocity_y / speed if speed > 0 else 0

        # Calculate projectile velocity (minimum speed + red dot's speed)
        projectile_speed = PROJECTILE_MIN_SPEED + speed
        projectile_vel_x = direction_x * projectile_speed
        projectile_vel_y = direction_y * projectile_speed

        # Create projectile at red dot's position
        return Projectile(
            self.virtual_x, self.virtual_y, projectile_vel_x, projectile_vel_y, "red"
        )

    def trigger_hp_damage_pulse(self):
        """Trigger the visual pulse effect when HP damage occurs."""
        self.pulse_timer = (
            SQUARE_PULSE_DURATION  # Reuse the same duration as square pulse
        )

    def is_pulsing(self):
        """Check if the dot is currently showing the HP damage pulse effect."""
        return self.pulse_timer > 0


class BlueSquare:
    def draw_svg(self, painter, screen_x, screen_y):
        # Draw the SVG centered at (screen_x, screen_y), scaled to match the square size, and rotated
        rect = QRectF(-self.size / 2, -self.size / 2, self.size, self.size)
        painter.save()
        painter.translate(screen_x, screen_y)
        painter.rotate(math.degrees(self.angle))
        self.svg_renderer.render(painter, rect)
        painter.restore()

    """Represents the blue square obstacle with physics."""

    def __init__(self, x=INITIAL_SQUARE_X, y=INITIAL_SQUARE_Y):
        # Position (world coordinates)
        self.x = float(x)
        self.y = float(y)

        # Linear physics properties
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.mass = SQUARE_MASS * 2  # Increased mass by 100%
        self.size = DOT_RADIUS * SQUARE_SIZE_MULTIPLIER * 1.5  # Increased size by 50%
        self.angle = 0.0  # Current rotation angle in radians
        self.angular_velocity = 0.0  # Angular velocity in radians per frame
        self.moment_of_inertia = PhysicsEngine.calculate_moment_of_inertia(
            self.mass, self.size
        )  # Visual effects
        self.pulse_timer = 0  # Timer for collision pulse effect

        # SVG Renderer for blue cube
        self.svg_renderer = QSvgRenderer(QByteArray(SVG_BLUE_CUBE.encode("utf-8")))

    def update_physics(self):
        """Update velocity, position, and rotation with friction."""
        # Apply linear friction
        self.velocity_x *= SQUARE_FRICTION
        self.velocity_y *= SQUARE_FRICTION

        # Update position based on velocity
        new_x = self.x + self.velocity_x
        new_y = self.y + self.velocity_y

        # Check if the square would go outside the circular boundary
        # For a square, we need to check if any corner would be outside
        half_size = self.size / 2

        # Calculate the distance from center to the farthest corner of the square
        # This is the diagonal distance from center to corner
        corner_distance = math.sqrt((half_size) ** 2 + (half_size) ** 2)

        # Check if the square center + corner distance exceeds the boundary
        distance_from_center = math.sqrt(new_x**2 + new_y**2)
        max_distance = GRID_RADIUS - corner_distance

        if distance_from_center > max_distance:
            # Square would go outside boundary - correct position
            angle = math.atan2(new_y, new_x)
            corrected_x = math.cos(angle) * max_distance
            corrected_y = math.sin(angle) * max_distance

            self.x = corrected_x
            self.y = corrected_y

            # Calculate normal vector (pointing inward)
            normal_x = -math.cos(angle)
            normal_y = -math.sin(angle)

            # Apply bounce with energy loss
            dot_product = self.velocity_x * normal_x + self.velocity_y * normal_y
            self.velocity_x -= 2 * dot_product * normal_x * BOUNCE_FACTOR
            self.velocity_y -= 2 * dot_product * normal_y * BOUNCE_FACTOR
        else:
            # Square stays within boundary
            self.x = new_x
            self.y = new_y

        # Apply rotational friction
        self.angular_velocity = PhysicsEngine.apply_rotational_physics(
            self.angular_velocity
        )

        # Update rotation
        self.angle += self.angular_velocity
        # Keep angle within 0 to 2π range for cleaner values
        self.angle = self.angle % (2 * math.pi)

        # Update pulse timer
        if self.pulse_timer > 0:
            self.pulse_timer -= 1

    def trigger_collision_pulse(self):
        """Trigger the visual pulse effect when collision occurs."""
        self.pulse_timer = SQUARE_PULSE_DURATION

    def is_pulsing(self):
        """Check if the square is currently showing the pulse effect."""
        return self.pulse_timer > 0

    def get_screen_position(
        self, camera_x, camera_y, view_width=WINDOW_WIDTH, view_height=WINDOW_HEIGHT
    ):
        """Get the screen position based on camera position and view dimensions."""
        view_center_x = view_width / 2
        view_center_y = view_height / 2
        screen_x = self.x - (camera_x - view_center_x)
        screen_y = self.y - (camera_y - view_center_y)
        return screen_x, screen_y

    def is_visible(
        self, camera_x, camera_y, view_width=WINDOW_WIDTH, view_height=WINDOW_HEIGHT
    ):
        """Check if the square is visible on screen with dynamic view dimensions."""
        screen_x, screen_y = self.get_screen_position(
            camera_x, camera_y, view_width, view_height
        )
        half_size = self.size / 2

        return (
            screen_x + half_size >= 0
            and screen_x - half_size <= view_width
            and screen_y + half_size >= 0
            and screen_y - half_size <= view_height
        )

    def check_collision_with_dot(self, dot):
        """
        Check collision with a red dot and apply physics response.

        Args:
            dot: RedDot instance

        Returns:
            bool: True if collision occurred and was resolved
        """
        is_colliding, normal_x, normal_y, penetration = (
            PhysicsEngine.check_rect_circle_collision(
                self.x,
                self.y,
                self.size,
                self.size,
                dot.virtual_x,
                dot.virtual_y,
                dot.radius,
            )
        )

        if is_colliding:
            # Calculate the correct position to place the dot just outside the square
            # The collision detection gives us the closest edge, so we position the dot
            # at the collision boundary (which is square edge + dot radius)

            half_size = self.size / 2

            if normal_x == -1:  # Hit left side
                dot.virtual_x = self.x - half_size - dot.radius - 0.1
            elif normal_x == 1:  # Hit right side
                dot.virtual_x = self.x + half_size + dot.radius + 0.1
            elif normal_y == -1:  # Hit top side
                dot.virtual_y = self.y - half_size - dot.radius - 0.1
            elif normal_y == 1:  # Hit bottom side
                dot.virtual_y = (
                    self.y + half_size + dot.radius + 0.1
                )  # Calculate impact point for torque calculation
            impact_point_x = dot.virtual_x - normal_x * dot.radius
            impact_point_y = dot.virtual_y - normal_y * dot.radius

            # Apply collision response for linear momentum
            old_dot_vel_x, old_dot_vel_y = dot.velocity_x, dot.velocity_y
            dot.velocity_x, dot.velocity_y, self.velocity_x, self.velocity_y = (
                PhysicsEngine.apply_collision_response(
                    dot.velocity_x,
                    dot.velocity_y,
                    dot.mass,
                    self.velocity_x,
                    self.velocity_y,
                    self.mass,
                    normal_x,
                    normal_y,
                )
            )

            # Calculate the impulse that was applied to the square
            impulse_x = (
                self.velocity_x - 0
            ) * self.mass  # Assuming square was initially at rest for this collision
            impulse_y = (self.velocity_y - 0) * self.mass

            # Apply rotational physics - calculate torque from the collision
            angular_velocity_change = PhysicsEngine.calculate_collision_torque(
                impact_point_x,
                impact_point_y,
                self.x,
                self.y,
                impulse_x,
                impulse_y,
                self.moment_of_inertia,
            )  # Add the angular velocity change to current angular velocity
            self.angular_velocity += angular_velocity_change

            # Trigger visual pulse effect
            self.trigger_collision_pulse()

            return True

        return False


class Projectile:
    def draw_svg(self, painter, screen_x, screen_y):
        # Draw the SVG centered at (screen_x, screen_y), scaled to 300% of projectile radius
        size = self.radius * 2 * 3.0  # 300% increase
        rect = QRectF(-size / 2, -size / 2, size, size)
        painter.save()
        painter.translate(screen_x, screen_y)
        self.svg_renderer.render(painter, rect)
        painter.restore()

    """Represents a green projectile shot by a player."""

    def __init__(self, x, y, velocity_x, velocity_y, owner_id="red"):
        # Position (world coordinates)
        self.x = float(x)
        self.y = float(y)

        # Physics properties
        self.velocity_x = float(velocity_x)
        self.velocity_y = float(velocity_y)
        self.mass = PROJECTILE_MASS
        self.radius = PROJECTILE_RADIUS

        # State
        self.is_active = True
        self.owner_id = owner_id  # "red" or "purple" - who fired this projectile

        # Track if this projectile has bounced or hit anything yet
        self.has_made_contact = False

        # Track number of bounces off the play area boundary
        self.bounce_count = 0

        # SVG Renderer for projectile icon
        self.svg_renderer = QSvgRenderer(
            QByteArray(SVG_PROJECTILE_ICON.encode("utf-8"))
        )

        # For multi-shot: projectiles are initially 'grouped' and cannot interact until separated
        self.just_launched = True

    def update_physics(self):
        """Update projectile position and handle boundary bounces."""
        if not self.is_active:
            return

        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Check for collision with circular boundary (bounce)
        distance_from_center = math.sqrt(self.x**2 + self.y**2)
        boundary_radius = GRID_RADIUS - self.radius
        if distance_from_center > boundary_radius:
            # Calculate normal at the point of contact (from center to projectile)
            nx = self.x / distance_from_center
            ny = self.y / distance_from_center
            # Reflect velocity vector
            dot = self.velocity_x * nx + self.velocity_y * ny
            self.velocity_x -= 2 * dot * nx
            self.velocity_y -= 2 * dot * ny
            # Move projectile just inside the boundary
            self.x = nx * boundary_radius
            self.y = ny * boundary_radius
            self.bounce_count += 1
            self.has_made_contact = True  # Bouncing counts as contact
            if self.bounce_count >= 6:
                self.is_active = False

    def get_screen_position(
        self, camera_x, camera_y, view_width=WINDOW_WIDTH, view_height=WINDOW_HEIGHT
    ):
        """Get the screen position based on camera position and view dimensions."""
        view_center_x = view_width / 2
        view_center_y = view_height / 2
        screen_x = self.x - (camera_x - view_center_x)
        screen_y = self.y - (camera_y - view_center_y)
        return screen_x, screen_y

    def is_visible(
        self, camera_x, camera_y, view_width=WINDOW_WIDTH, view_height=WINDOW_HEIGHT
    ):
        """Check if the projectile is visible on screen with dynamic view dimensions."""
        screen_x, screen_y = self.get_screen_position(
            camera_x, camera_y, view_width, view_height
        )
        return (
            screen_x + self.radius >= 0
            and screen_x - self.radius <= view_width
            and screen_y + self.radius >= 0
            and screen_y - self.radius <= view_height
        )

    def check_collision_with_square(self, square):
        """
        Check collision with the blue square and bounce off.

        Args:
            square: BlueSquare instance

        Returns:
            bool: True if collision occurred
        """
        if not self.is_active:
            return False

        is_colliding, normal_x, normal_y, penetration = (
            PhysicsEngine.check_rect_circle_collision(
                square.x,
                square.y,
                square.size,
                square.size,
                self.x,
                self.y,
                self.radius,
            )
        )

        if is_colliding:
            self.has_made_contact = True  # Mark as having made contact
            # Calculate the correct position to place the projectile just outside the square
            # Use the same logic as the red dot collision handling
            half_size = square.size / 2

            if normal_x == -1:  # Hit left side
                self.x = square.x - half_size - self.radius - 0.1
            elif normal_x == 1:  # Hit right side
                self.x = square.x + half_size + self.radius + 0.1
            elif normal_y == -1:  # Hit top side
                self.y = square.y - half_size - self.radius - 0.1
            elif normal_y == 1:  # Hit bottom side
                self.y = square.y + half_size + self.radius + 0.1

            # Calculate impact point for torque calculation
            impact_point_x = self.x - normal_x * self.radius
            impact_point_y = self.y - normal_y * self.radius

            # Apply proper Newtonian collision response for linear momentum
            old_projectile_vel_x, old_projectile_vel_y = (
                self.velocity_x,
                self.velocity_y,
            )
            self.velocity_x, self.velocity_y, square.velocity_x, square.velocity_y = (
                PhysicsEngine.apply_collision_response(
                    self.velocity_x,
                    self.velocity_y,
                    self.mass,
                    square.velocity_x,
                    square.velocity_y,
                    square.mass,
                    normal_x,
                    normal_y,
                )
            )

            # Calculate the impulse that was applied to the square for rotational physics
            impulse_x = (
                square.velocity_x - 0
            ) * square.mass  # Assuming square was initially at rest
            impulse_y = (square.velocity_y - 0) * square.mass

            # Apply rotational physics - calculate torque from the collision
            angular_velocity_change = PhysicsEngine.calculate_collision_torque(
                impact_point_x,
                impact_point_y,
                square.x,
                square.y,
                impulse_x,
                impulse_y,
                square.moment_of_inertia,
            )

            # Add the angular velocity change to current angular velocity
            square.angular_velocity += angular_velocity_change

            # Trigger visual pulse effect on the square
            square.trigger_collision_pulse()

            return True

        return False

    def check_collision_with_dot(self, dot, dot_id="red"):
        """
        Check collision with a dot and apply Newtonian physics response.

        Args:
            dot: RedDot or PurpleDot instance
            dot_id: "red" or "purple" - which player this dot belongs to

        Returns:
            bool: True if collision occurred
        """
        if not self.is_active:
            return False

        # Only allow self-collision if projectile has made contact with something else
        if self.owner_id == dot_id and not self.has_made_contact:
            return False

        # Check for circle-circle collision
        distance = math.sqrt(
            (self.x - dot.virtual_x) ** 2 + (self.y - dot.virtual_y) ** 2
        )
        collision_distance = self.radius + dot.radius

        if distance <= collision_distance:
            if self.owner_id == dot_id:
                self.has_made_contact = (
                    True  # Mark as having made contact after first hit
                )
            # Calculate collision normal (from dot to projectile)
            if distance > 0:
                normal_x = (self.x - dot.virtual_x) / distance
                normal_y = (self.y - dot.virtual_y) / distance
            else:
                # Handle the rare case of exact overlap
                normal_x = 1.0
                normal_y = 0.0

            # Separate the objects to prevent overlap
            overlap = collision_distance - distance
            separation = overlap / 2

            # Move projectile away from dot
            self.x += normal_x * separation
            self.y += normal_y * separation

            # Move dot away from projectile
            dot.virtual_x -= normal_x * separation
            dot.virtual_y -= normal_y * separation

            # Apply proper Newtonian collision response for linear momentum
            self.velocity_x, self.velocity_y, dot.velocity_x, dot.velocity_y = (
                PhysicsEngine.apply_collision_response(
                    self.velocity_x,
                    self.velocity_y,
                    self.mass,
                    dot.velocity_x,
                    dot.velocity_y,
                    dot.mass,
                    normal_x,
                    normal_y,
                )
            )

            return True

        return False


class PurpleDot(RedDot):
    """Represents the second player's purple dot - inherits from RedDot."""

    def __init__(self, x=PURPLE_PLAYER_INITIAL_X, y=PURPLE_PLAYER_INITIAL_Y):
        super().__init__(x, y)
        # SVG Renderer for purple ship
        self.svg_renderer = QSvgRenderer(QByteArray(SVG_PURPLE_SHIP.encode("utf-8")))
        # Store last movement angle and size for rendering when stationary
        dx = 0 - self.virtual_x
        dy = 0 - self.virtual_y
        if dx == 0 and dy == 0:
            self._last_angle = 180
        else:
            self._last_angle = math.degrees(math.atan2(dy, dx)) + 180
        self._last_size = self.radius * 2 * 1.5

    def draw_svg(self, painter, screen_x, screen_y, scale=1.0, angle=None):
        # Draw the SVG centered at (screen_x, screen_y), scaled to match the red ship, and rotated 180deg from movement
        momentum_info = self.get_momentum_info()
        if momentum_info:
            ship_size = (
                momentum_info["size"] * 2.2 * 1.5
            )  # 50% larger (same for both ships)
            ship_angle = math.degrees(momentum_info["angle"]) + 180
            self._last_angle = ship_angle
            self._last_size = ship_size
        else:
            ship_size = self._last_size
            ship_angle = self._last_angle
        rect = QRectF(-ship_size / 2, -ship_size / 2, ship_size, ship_size)
        painter.save()
        painter.translate(screen_x, screen_y)
        painter.rotate(ship_angle - 90)  # SVG points up, so 0 deg = up
        self.svg_renderer.render(painter, rect)
        painter.restore()

    def get_color(self):
        """Return the purple color for this dot."""
        return (128, 0, 128)  # Purple color

    def shoot_projectile(self):
        """
        Create a projectile in the direction of momentum (Purple player version).

        Returns:
            Projectile: New projectile instance, or None if not moving
        """
        speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)

        # Only shoot if moving (to determine direction)
        if speed < 0.1:
            return None

        # Calculate projectile direction (same as momentum direction)
        direction_x = self.velocity_x / speed if speed > 0 else 0
        direction_y = self.velocity_y / speed if speed > 0 else 0

        # Calculate projectile velocity (minimum speed + purple dot's speed)
        projectile_speed = PROJECTILE_MIN_SPEED + speed
        projectile_vel_x = direction_x * projectile_speed
        projectile_vel_y = direction_y * projectile_speed

        # Create projectile at purple dot's position with "purple" owner_id
        return Projectile(
            self.virtual_x, self.virtual_y, projectile_vel_x, projectile_vel_y, "purple"
        )


class StaticCircle:
    """Represents a static decorative circle with no collision detection."""

    def __init__(self, x, y, color, outline_color):
        """
        Initialize a static circle.

        Args:
            x, y: World position of the circle center
            color: RGB tuple for the circle fill color
            outline_color: RGB tuple for the circle outline color
        """
        self.x = float(x)
        self.y = float(y)
        self.radius = STATIC_CIRCLE_RADIUS
        self.color = color
        self.outline_color = outline_color

    def get_screen_position(
        self, camera_x, camera_y, view_width=WINDOW_WIDTH, view_height=WINDOW_HEIGHT
    ):
        """Get the screen position based on camera position and view dimensions."""
        view_center_x = view_width / 2
        view_center_y = view_height / 2
        screen_x = self.x - (camera_x - view_center_x)
        screen_y = self.y - (camera_y - view_center_y)
        return screen_x, screen_y

    def is_visible(
        self, camera_x, camera_y, view_width=WINDOW_WIDTH, view_height=WINDOW_HEIGHT
    ):
        """Check if the circle is visible on screen with dynamic view dimensions."""
        screen_x, screen_y = self.get_screen_position(
            camera_x, camera_y, view_width, view_height
        )

        return (
            screen_x + self.radius >= 0
            and screen_x - self.radius <= view_width
            and screen_y + self.radius >= 0
            and screen_y - self.radius <= view_height
        )


class StaticRedCircle(StaticCircle):
    """Red static circle positioned on the left side of the equator."""

    def __init__(self):
        super().__init__(
            STATIC_RED_CIRCLE_X,
            STATIC_RED_CIRCLE_Y,
            STATIC_RED_CIRCLE_COLOR,
            STATIC_RED_CIRCLE_OUTLINE,
        )
        self.svg_renderer = QSvgRenderer(QByteArray(SVG_RED_GOAL.encode("utf-8")))

    def draw_svg(self, painter, screen_x, screen_y, size=None):
        # Draw the SVG centered at (screen_x, screen_y), scaled to match the circle radius
        r = self.radius if size is None else size / 2
        rect = QRectF(-r, -r, r * 2, r * 2)
        painter.save()
        painter.translate(screen_x, screen_y)
        self.svg_renderer.render(painter, rect)
        painter.restore()


class StaticPurpleCircle(StaticCircle):
    """Purple static circle positioned on the right side of the equator."""

    def __init__(self):
        super().__init__(
            STATIC_PURPLE_CIRCLE_X,
            STATIC_PURPLE_CIRCLE_Y,
            STATIC_PURPLE_CIRCLE_COLOR,
            STATIC_PURPLE_CIRCLE_OUTLINE,
        )
        self.svg_renderer = QSvgRenderer(QByteArray(SVG_PURPLE_GOAL.encode("utf-8")))

    def draw_svg(self, painter, screen_x, screen_y, size=None):
        # Draw the SVG centered at (screen_x, screen_y), scaled to match the circle radius
        r = self.radius if size is None else size / 2
        rect = QRectF(-r, -r, r * 2, r * 2)
        painter.save()
        painter.translate(screen_x, screen_y)
        self.svg_renderer.render(painter, rect)
        painter.restore()


class GravitationalDot:
    """Represents a gravitational dot that pulls objects toward its center."""

    def __init__(self, x, y):
        """
        Initialize a gravitational dot.

        Args:
            x, y: World position of the gravitational dot center
        """
        self.x = float(x)
        self.y = float(y)
        self.radius = GRAVITY_DOT_RADIUS
        self.strength = GRAVITY_STRENGTH
        self.max_distance = GRAVITY_MAX_DISTANCE

    def get_screen_position(
        self, camera_x, camera_y, view_width=WINDOW_WIDTH, view_height=WINDOW_HEIGHT
    ):
        """Get the screen position based on camera position and view dimensions."""
        view_center_x = view_width / 2
        view_center_y = view_height / 2
        screen_x = self.x - (camera_x - view_center_x)
        screen_y = self.y - (camera_y - view_center_y)
        return screen_x, screen_y

    def is_visible(
        self, camera_x, camera_y, view_width=WINDOW_WIDTH, view_height=WINDOW_HEIGHT
    ):
        """Check if the gravitational dot is visible on screen with dynamic view dimensions."""
        screen_x, screen_y = self.get_screen_position(
            camera_x, camera_y, view_width, view_height
        )

        return (
            screen_x + self.radius >= 0
            and screen_x - self.radius <= view_width
            and screen_y + self.radius >= 0
            and screen_y - self.radius <= view_height
        )

    def apply_gravity_to_object(self, obj):
        """
        Apply gravitational force to an object if it's within range.

        Args:
            obj: Object with x, y, velocity_x, velocity_y attributes

        Returns:
            bool: True if gravity was applied, False otherwise
        """
        # Calculate distance from gravitational dot to object
        dx = self.x - obj.x
        dy = self.y - obj.y
        distance = math.sqrt(dx * dx + dy * dy)

        # Only apply gravity if object is within the gravitational field
        if distance > self.max_distance or distance < 0.1:  # Avoid division by zero
            return False

        # Calculate gravitational force (inverse square law with configurable falloff)
        force_magnitude = self.strength / (distance**GRAVITY_FALLOFF_POWER)

        # Normalize direction vector
        force_x = (dx / distance) * force_magnitude
        force_y = (dy / distance) * force_magnitude

        # Apply force to object's velocity
        obj.velocity_x += force_x
        obj.velocity_y += force_y

        return True


class RedGravitationalDot(GravitationalDot):
    """Gravitational dot positioned at the center of the red static circle."""

    def __init__(self):
        super().__init__(STATIC_RED_CIRCLE_X, STATIC_RED_CIRCLE_Y)


class PurpleGravitationalDot(GravitationalDot):
    """Gravitational dot positioned at the center of the purple static circle."""

    def __init__(self):
        super().__init__(STATIC_PURPLE_CIRCLE_X, STATIC_PURPLE_CIRCLE_Y)


class CentralGravitationalDot(GravitationalDot):
    """Invisible gravitational dot positioned at the center of the grid."""

    def __init__(self):
        # Initialize with central gravity configuration
        super().__init__(CENTRAL_GRAVITY_X, CENTRAL_GRAVITY_Y)
        # Override with central gravity specific settings
        self.strength = CENTRAL_GRAVITY_STRENGTH
        self.max_distance = CENTRAL_GRAVITY_MAX_DISTANCE
        self.radius = CENTRAL_GRAVITY_RADIUS
