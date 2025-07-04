"""
Game object classes for the Topographical Plane application.
Contains the RedDot and BlueSquare classes with their properties and behaviors.
"""

import math
from config import *
from physics import PhysicsEngine


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
    """Represents the blue square obstacle with physics."""

    def __init__(self, x=INITIAL_SQUARE_X, y=INITIAL_SQUARE_Y):
        # Position (world coordinates)
        self.x = float(x)
        self.y = float(y)

        # Linear physics properties
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.mass = SQUARE_MASS
        self.size = DOT_RADIUS * SQUARE_SIZE_MULTIPLIER  # Rotational physics properties
        self.angle = 0.0  # Current rotation angle in radians
        self.angular_velocity = 0.0  # Angular velocity in radians per frame
        self.moment_of_inertia = PhysicsEngine.calculate_moment_of_inertia(
            self.mass, self.size
        )  # Visual effects
        self.pulse_timer = 0  # Timer for collision pulse effect

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

    def update_physics(self):
        """Update projectile position."""
        if not self.is_active:
            return

        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Check if projectile is outside the grid boundary
        distance_from_center = math.sqrt(self.x**2 + self.y**2)
        if distance_from_center > GRID_RADIUS - self.radius:
            # Projectile hit the boundary - deactivate it
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

        # Prevent self-collision: projectile doesn't collide with the player who fired it
        if self.owner_id == dot_id:
            return False

        # Check for circle-circle collision
        distance = math.sqrt(
            (self.x - dot.virtual_x) ** 2 + (self.y - dot.virtual_y) ** 2
        )
        collision_distance = self.radius + dot.radius

        if distance <= collision_distance:
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
        # Purple dot has the same properties as red dot but different color
        # Color is handled in the rendering layer

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


class StaticPurpleCircle(StaticCircle):
    """Purple static circle positioned on the right side of the equator."""

    def __init__(self):
        super().__init__(
            STATIC_PURPLE_CIRCLE_X,
            STATIC_PURPLE_CIRCLE_Y,
            STATIC_PURPLE_CIRCLE_COLOR,
            STATIC_PURPLE_CIRCLE_OUTLINE,
        )


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
