"""
Physics calculations and collision detection for the Topographical Plane application.
Handles momentum transfer, boundary checking, and collision response.
"""

import math
from config import *


class PhysicsEngine:
    """Handles all physics calculations for the topographical plane simulation."""

    @staticmethod
    def apply_momentum_physics(
        velocity_x, velocity_y, acceleration_x, acceleration_y, dt=1.0
    ):
        """
        Apply acceleration and deceleration to velocity components.

        Args:
            velocity_x, velocity_y: Current velocity components
            acceleration_x, acceleration_y: Applied acceleration
            dt: Time delta (usually 1.0 for frame-based updates)

        Returns:
            tuple: New (velocity_x, velocity_y)
        """
        # Apply acceleration
        new_velocity_x = velocity_x + acceleration_x * dt
        new_velocity_y = velocity_y + acceleration_y * dt

        # Apply deceleration (friction)
        new_velocity_x *= DECELERATION
        new_velocity_y *= DECELERATION

        # Clamp to maximum speed
        speed = math.sqrt(new_velocity_x**2 + new_velocity_y**2)
        if speed > MAX_SPEED:
            scale = MAX_SPEED / speed
            new_velocity_x *= scale
            new_velocity_y *= scale

        return new_velocity_x, new_velocity_y

    @staticmethod
    def check_circular_boundary(x, y, radius, boundary_radius):
        """
        Check if a circular object is within a circular boundary.

        Args:
            x, y: Object center position
            radius: Object radius
            boundary_radius: Boundary radius

        Returns:
            tuple: (is_outside, corrected_x, corrected_y, normal_x, normal_y)
        """
        distance_from_center = math.sqrt(x**2 + y**2)
        max_distance = boundary_radius - radius

        if distance_from_center > max_distance:
            # Outside boundary - calculate correction
            angle = math.atan2(y, x)
            corrected_x = math.cos(angle) * max_distance
            corrected_y = math.sin(angle) * max_distance

            # Calculate normal vector (pointing inward)
            normal_x = -math.cos(angle)
            normal_y = -math.sin(angle)

            return True, corrected_x, corrected_y, normal_x, normal_y

        return False, x, y, 0, 0

    @staticmethod
    def apply_collision_response(
        obj1_vel_x,
        obj1_vel_y,
        obj1_mass,
        obj2_vel_x,
        obj2_vel_y,
        obj2_mass,
        normal_x,
        normal_y,
        restitution=RESTITUTION,
    ):
        """
        Apply collision response using conservation of momentum.

        Args:
            obj1_vel_x, obj1_vel_y: Object 1 velocity components
            obj1_mass: Object 1 mass
            obj2_vel_x, obj2_vel_y: Object 2 velocity components
            obj2_mass: Object 2 mass
            normal_x, normal_y: Collision normal vector
            restitution: Coefficient of restitution (bounciness)

        Returns:
            tuple: (new_obj1_vel_x, new_obj1_vel_y, new_obj2_vel_x, new_obj2_vel_y)
        """
        # Calculate relative velocity
        relative_velocity_x = obj1_vel_x - obj2_vel_x
        relative_velocity_y = obj1_vel_y - obj2_vel_y

        # Calculate relative velocity in collision normal direction
        relative_velocity_normal = (
            relative_velocity_x * normal_x + relative_velocity_y * normal_y
        )

        # Don't resolve if velocities are separating
        if relative_velocity_normal > 0:
            return obj1_vel_x, obj1_vel_y, obj2_vel_x, obj2_vel_y

        # Calculate collision impulse
        impulse_magnitude = -(1 + restitution) * relative_velocity_normal
        impulse_magnitude /= 1 / obj1_mass + 1 / obj2_mass

        # Apply impulse to both objects
        impulse_x = impulse_magnitude * normal_x
        impulse_y = impulse_magnitude * normal_y

        new_obj1_vel_x = obj1_vel_x + impulse_x / obj1_mass
        new_obj1_vel_y = obj1_vel_y + impulse_y / obj1_mass
        new_obj2_vel_x = obj2_vel_x - impulse_x / obj2_mass
        new_obj2_vel_y = obj2_vel_y - impulse_y / obj2_mass

        return new_obj1_vel_x, new_obj1_vel_y, new_obj2_vel_x, new_obj2_vel_y

    @staticmethod
    def check_rect_circle_collision(
        rect_x, rect_y, rect_width, rect_height, circle_x, circle_y, circle_radius
    ):
        """
        Check collision between a rectangle and circle.

        Args:
            rect_x, rect_y: Rectangle center position
            rect_width, rect_height: Rectangle dimensions
            circle_x, circle_y: Circle center position
            circle_radius: Circle radius

        Returns:
            tuple: (is_colliding, collision_normal_x, collision_normal_y, penetration_depth)
        """
        # Calculate rectangle boundaries
        half_width = rect_width / 2
        half_height = rect_height / 2
        rect_left = rect_x - half_width
        rect_right = rect_x + half_width
        rect_top = rect_y - half_height
        rect_bottom = rect_y + half_height

        # Expand rectangle by circle radius to create collision zone
        collision_left = rect_left - circle_radius
        collision_right = rect_right + circle_radius
        collision_top = rect_top - circle_radius
        collision_bottom = rect_bottom + circle_radius

        # Check if circle center is in collision zone
        if (
            circle_x > collision_left
            and circle_x < collision_right
            and circle_y > collision_top
            and circle_y < collision_bottom
        ):

            # Calculate distances to each edge
            dist_to_left = abs(circle_x - collision_left)
            dist_to_right = abs(circle_x - collision_right)
            dist_to_top = abs(circle_y - collision_top)
            dist_to_bottom = abs(circle_y - collision_bottom)

            # Find closest edge
            min_distance = min(dist_to_left, dist_to_right, dist_to_top, dist_to_bottom)

            if min_distance == dist_to_left:
                return True, -1, 0, min_distance  # Hit left side
            elif min_distance == dist_to_right:
                return True, 1, 0, min_distance  # Hit right side
            elif min_distance == dist_to_top:
                return True, 0, -1, min_distance  # Hit top side
            else:
                return True, 0, 1, min_distance  # Hit bottom side

        return False, 0, 0, 0

    @staticmethod
    def apply_rotational_physics(angular_velocity, dt=1.0):
        """
        Apply rotational friction to angular velocity.

        Args:
            angular_velocity: Current angular velocity (radians per frame)
            dt: Time delta (usually 1.0 for frame-based updates)

        Returns:
            float: New angular velocity
        """
        # Apply angular friction
        new_angular_velocity = angular_velocity * ANGULAR_FRICTION

        # Clamp to maximum angular speed
        if abs(new_angular_velocity) > MAX_ANGULAR_VELOCITY:
            new_angular_velocity = (
                MAX_ANGULAR_VELOCITY
                if new_angular_velocity > 0
                else -MAX_ANGULAR_VELOCITY
            )

        return new_angular_velocity

    @staticmethod
    def calculate_moment_of_inertia(mass, size):
        """
        Calculate moment of inertia for a square object.

        Args:
            mass: Object mass
            size: Square side length

        Returns:
            float: Moment of inertia
        """
        # For a square: I = (1/6) * mass * (width^2 + height^2)
        # Since it's a square: I = (1/3) * mass * side^2
        return MOMENT_OF_INERTIA_FACTOR * mass * (size * size)

    @staticmethod
    def calculate_collision_torque(
        impact_point_x,
        impact_point_y,
        center_x,
        center_y,
        impulse_x,
        impulse_y,
        moment_of_inertia,
    ):
        """
        Calculate the torque and resulting angular velocity change from a collision.

        Args:
            impact_point_x, impact_point_y: Point where collision occurs
            center_x, center_y: Center of mass of the object
            impulse_x, impulse_y: Linear impulse applied at impact point
            moment_of_inertia: Object's moment of inertia

        Returns:
            float: Change in angular velocity (radians per frame)
        """
        # Calculate vector from center of mass to impact point
        r_x = impact_point_x - center_x
        r_y = impact_point_y - center_y

        # Calculate torque using cross product: τ = r × F
        # In 2D: τ = r_x * F_y - r_y * F_x
        torque = r_x * impulse_y - r_y * impulse_x

        # Calculate angular impulse and resulting angular velocity change
        # Δω = τ / I (where I is moment of inertia)
        angular_velocity_change = torque / moment_of_inertia

        return angular_velocity_change
