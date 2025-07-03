"""
Rendering functions for the Topographical Plane application.
Handles all drawing operations including the grid, objects, and effects.
"""

import math
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QRadialGradient, QPolygonF
from PyQt6.QtCore import QRectF, QPointF
from config import *


class Renderer:
    """Handles all rendering operations for the topographical plane."""

    @staticmethod
    def get_adaptive_grid_spacing(view_width, view_height):
        """
        Returns an adaptive grid spacing based on the view size.
        Increases spacing for very large windows to reduce draw calls.
        """
        base_spacing = int(
            GRID_SPACING * 3.0
        )  # 50% less dense again (total 75% less dense)
        max_dim = max(view_width, view_height)
        if max_dim > 1600:
            return base_spacing * 2
        elif max_dim > 1200:
            return int(base_spacing * 1.5)
        else:
            return base_spacing

    @staticmethod
    def draw_triangular_grid(painter, camera_x, camera_y, view_center_x, view_center_y):
        """
        Draw the triangular grid of dots.

        Args:
            painter: QPainter instance
            camera_x, camera_y: Camera position in world coordinates
            view_center_x, view_center_y: Center coordinates of the current view
        """
        # Set pen and brush for grid dots
        painter.setPen(QPen(QColor(*GRID_COLOR), 2))
        painter.setBrush(
            QBrush(QColor(*GRID_COLOR))
        )  # Calculate grid center position on screen
        # The world origin (0,0) should appear at screen coordinates that account for camera offset
        world_origin_screen_x = view_center_x - camera_x
        world_origin_screen_y = view_center_y - camera_y

        grid_center_x = world_origin_screen_x
        grid_center_y = world_origin_screen_y

        # Use adaptive grid spacing
        view_width = view_center_x * 2
        view_height = view_center_y * 2
        grid_spacing = Renderer.get_adaptive_grid_spacing(view_width, view_height)
        vertical_offset = grid_spacing * math.sqrt(3) / 2

        # Calculate visible range
        min_y = grid_center_y - GRID_RADIUS
        max_y = grid_center_y + GRID_RADIUS

        start_row = int((min_y - grid_center_y) / vertical_offset) - 2
        end_row = int((max_y - grid_center_y) / vertical_offset) + 2

        # Draw grid rows
        for row in range(start_row, end_row + 1):
            y = grid_center_y + (row * vertical_offset)

            # Skip rows outside the window
            if y < -GRID_DOT_RADIUS or y > (view_center_y * 2) + GRID_DOT_RADIUS:
                continue

            # Calculate horizontal offset for triangular pattern
            x_offset = 0 if row % 2 == 0 else grid_spacing / 2

            # Calculate visible columns for this row
            min_x = grid_center_x - GRID_RADIUS
            max_x = grid_center_x + GRID_RADIUS

            start_col = int((min_x - grid_center_x - x_offset) / grid_spacing) - 1
            end_col = int((max_x - grid_center_x - x_offset) / grid_spacing) + 1

            # Draw dots in this row
            for col in range(start_col, end_col + 1):
                x = grid_center_x + (col * grid_spacing) + x_offset

                # Skip dots outside the window
                if x < -GRID_DOT_RADIUS or x > (view_center_x * 2) + GRID_DOT_RADIUS:
                    continue

                # Check if dot is within the circular grid boundary
                grid_distance = math.sqrt(
                    (x - grid_center_x) ** 2 + (y - grid_center_y) ** 2
                )
                if grid_distance <= GRID_RADIUS:
                    painter.drawEllipse(
                        int(x - GRID_DOT_RADIUS),
                        int(y - GRID_DOT_RADIUS),
                        GRID_DOT_RADIUS * 2,
                        GRID_DOT_RADIUS * 2,
                    )

    @staticmethod
    def draw_vignette_gradient(
        painter, camera_x, camera_y, view_center_x, view_center_y
    ):
        """
        Draw the vignette gradient effect at the grid boundary.

        Args:
            painter: QPainter instance
            camera_x, camera_y: Camera position in world coordinates
            view_center_x, view_center_y: Center coordinates of the current view
        """  # Calculate grid center position on screen (same as triangular grid)
        # The world origin (0,0) should appear at screen coordinates that account for camera offset
        world_origin_screen_x = view_center_x - camera_x
        world_origin_screen_y = view_center_y - camera_y

        grid_center_x = world_origin_screen_x
        grid_center_y = world_origin_screen_y  # Create radial gradient that matches the actual grid boundary
        gradient = QRadialGradient(grid_center_x, grid_center_y, GRID_RADIUS)
        gradient.setColorAt(0.0, QColor(*VIGNETTE_COLOR))  # Transparent at center
        gradient.setColorAt(
            0.85, QColor(*VIGNETTE_COLOR)
        )  # Still transparent until near edge
        gradient.setColorAt(
            1.0, QColor(*VIGNETTE_EDGE_COLOR)
        )  # Opaque at actual boundary

        # Apply gradient and draw at the actual grid boundary radius
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QColor(0, 0, 0, 0)))  # Transparent pen
        painter.drawEllipse(
            int(grid_center_x - GRID_RADIUS),
            int(grid_center_y - GRID_RADIUS),
            GRID_RADIUS * 2,
            GRID_RADIUS * 2,
        )

    @staticmethod
    def draw_blue_square(painter, square, camera_x, camera_y, view_width, view_height):
        """
        Draw the blue square object.

        Args:
            painter: QPainter instance
            square: BlueSquare instance
            camera_x, camera_y: Camera position in world coordinates
            view_width, view_height: Dimensions of the view area
        """
        if not square.is_visible(camera_x, camera_y, view_width, view_height):
            return  # Get screen position
        screen_x, screen_y = square.get_screen_position(
            camera_x, camera_y, view_width, view_height
        )

        # Choose colors based on pulse state
        if square.is_pulsing():
            # Use lighter blue colors during pulse
            outline_color = SQUARE_PULSE_COLOR
            fill_color = SQUARE_PULSE_COLOR
            # Make the pulse intensity fade over time
            pulse_intensity = square.pulse_timer / SQUARE_PULSE_DURATION
            # Interpolate between normal and pulse colors
            normal_outline = QColor(*SQUARE_OUTLINE_COLOR)
            pulse_outline = QColor(*SQUARE_PULSE_COLOR)
            normal_fill = QColor(*SQUARE_COLOR)
            pulse_fill = QColor(*SQUARE_PULSE_COLOR)

            # Blend colors based on pulse intensity
            outline_r = int(
                normal_outline.red()
                + (pulse_outline.red() - normal_outline.red()) * pulse_intensity
            )
            outline_g = int(
                normal_outline.green()
                + (pulse_outline.green() - normal_outline.green()) * pulse_intensity
            )
            outline_b = int(
                normal_outline.blue()
                + (pulse_outline.blue() - normal_outline.blue()) * pulse_intensity
            )

            fill_r = int(
                normal_fill.red()
                + (pulse_fill.red() - normal_fill.red()) * pulse_intensity
            )
            fill_g = int(
                normal_fill.green()
                + (pulse_fill.green() - normal_fill.green()) * pulse_intensity
            )
            fill_b = int(
                normal_fill.blue()
                + (pulse_fill.blue() - normal_fill.blue()) * pulse_intensity
            )

            painter.setPen(
                QPen(QColor(outline_r, outline_g, outline_b), 3)
            )  # Thicker border during pulse
            painter.setBrush(QBrush(QColor(fill_r, fill_g, fill_b)))
        else:
            # Use normal colors
            painter.setPen(QPen(QColor(*SQUARE_OUTLINE_COLOR), 2))
            painter.setBrush(QBrush(QColor(*SQUARE_COLOR)))

        # Save the current transformation state
        painter.save()

        # Translate to the square center for rotation
        painter.translate(screen_x, screen_y)

        # Apply rotation
        painter.rotate(math.degrees(square.angle))  # Convert radians to degrees for Qt

        # Draw the square centered at origin (since we translated)
        half_size = square.size / 2
        rect = QRectF(-half_size, -half_size, square.size, square.size)
        painter.drawRect(rect)

        # Restore the transformation state
        painter.restore()

    @staticmethod
    def draw_red_dot(painter, dot, view_center_x, view_center_y):
        """
        Draw the red dot with momentum indicator.

        Args:
            painter: QPainter instance
            dot: RedDot instance
            view_center_x, view_center_y: Center coordinates of the current view
        """
        # Get screen position (always at center)
        screen_x, screen_y = view_center_x, view_center_y

        # Choose color based on pulse state
        if dot.is_pulsing():
            color = HP_DAMAGE_PULSE_COLOR  # Yellow when taking HP damage
        else:
            color = DOT_COLOR  # Normal red color

        # Draw the dot
        painter.setPen(QPen(QColor(*color), 2))
        painter.setBrush(QBrush(QColor(*color)))
        painter.drawEllipse(
            int(screen_x - dot.radius),
            int(screen_y - dot.radius),
            dot.radius * 2,
            dot.radius * 2,
        )

        # Draw momentum indicator if moving
        momentum_info = dot.get_momentum_info()
        if momentum_info:
            Renderer._draw_momentum_indicator(
                painter, screen_x, screen_y, momentum_info
            )

    @staticmethod
    def _draw_momentum_indicator(painter, center_x, center_y, momentum_info):
        """
        Draw the triangular momentum indicator.

        Args:
            painter: QPainter instance
            center_x, center_y: Center position for the indicator
            momentum_info: Dictionary with angle, size, and speed information
        """
        angle = momentum_info["angle"]
        triangle_size = momentum_info["size"]
        speed = momentum_info["speed"]

        # Calculate color intensity based on speed
        intensity = min(255, int(100 + (speed / MAX_SPEED) * 155))

        # Set triangle color (red with varying intensity)
        painter.setPen(QPen(QColor(intensity, 0, 0), 1))
        painter.setBrush(QBrush(QColor(intensity, 0, 0, 150)))

        # Calculate triangle points
        triangle_distance = DOT_RADIUS + MOMENTUM_DISTANCE

        # Tip of triangle (pointing in direction of movement)
        tip_x = center_x + math.cos(angle) * (triangle_distance + triangle_size)
        tip_y = center_y + math.sin(angle) * (triangle_distance + triangle_size)

        # Base points of triangle
        base_angle1 = angle + (2 * math.pi / 3)  # 120 degrees from tip
        base_angle2 = angle - (2 * math.pi / 3)  # 120 degrees from tip (other side)

        base1_x = center_x + math.cos(base_angle1) * triangle_distance
        base1_y = center_y + math.sin(base_angle1) * triangle_distance
        base2_x = center_x + math.cos(base_angle2) * triangle_distance
        base2_y = center_y + math.sin(base_angle2) * triangle_distance

        # Create and draw triangle
        triangle = QPolygonF(
            [
                QPointF(tip_x, tip_y),
                QPointF(base1_x, base1_y),
                QPointF(base2_x, base2_y),
            ]
        )
        painter.drawPolygon(triangle)

    @staticmethod
    @staticmethod
    def draw_projectiles(
        painter, projectiles, camera_x, camera_y, view_width, view_height
    ):
        """
        Draw all active projectiles.

        Args:
            painter: QPainter instance
            projectiles: List of Projectile instances
            camera_x, camera_y: Camera position in world coordinates
            view_width, view_height: Dimensions of the view area
        """
        # Set pen and brush for projectiles
        painter.setPen(QPen(QColor(*PROJECTILE_COLOR), 1))
        painter.setBrush(QBrush(QColor(*PROJECTILE_COLOR)))

        for projectile in projectiles:
            if not projectile.is_active or not projectile.is_visible(
                camera_x, camera_y, view_width, view_height
            ):
                continue

            # Get screen position
            screen_x, screen_y = projectile.get_screen_position(
                camera_x, camera_y, view_width, view_height
            )

            # Draw the projectile as a small circle
            painter.drawEllipse(
                int(screen_x - projectile.radius),
                int(screen_y - projectile.radius),
                int(projectile.radius * 2),
                int(projectile.radius * 2),
            )

    @staticmethod
    def draw_purple_dot(painter, dot, camera_x, camera_y, view_center_x, view_center_y):
        """
        Draw the purple dot with momentum indicator.

        Args:
            painter: QPainter instance
            dot: PurpleDot instance
            camera_x, camera_y: Camera position in world coordinates
            view_center_x, view_center_y: Center coordinates of the current view
        """
        # Get screen position relative to camera
        screen_x = dot.virtual_x - (camera_x - view_center_x)
        screen_y = dot.virtual_y - (camera_y - view_center_y)

        # Only draw if visible on screen
        if (
            screen_x + dot.radius >= 0
            and screen_x - dot.radius <= (view_center_x * 2)
            and screen_y + dot.radius >= 0
            and screen_y - dot.radius <= (view_center_y * 2)
        ):

            # Choose color based on pulse state
            if dot.is_pulsing():
                purple_color = HP_DAMAGE_PULSE_COLOR  # Yellow when taking HP damage
            else:
                purple_color = (128, 0, 128)  # Normal purple color

            # Draw the dot
            painter.setPen(QPen(QColor(*purple_color), 2))
            painter.setBrush(QBrush(QColor(*purple_color)))
            painter.drawEllipse(
                int(screen_x - dot.radius),
                int(screen_y - dot.radius),
                dot.radius * 2,
                dot.radius * 2,
            )

            # Draw momentum indicator if moving
            momentum_info = dot.get_momentum_info()
            if momentum_info:
                Renderer._draw_purple_momentum_indicator(
                    painter, screen_x, screen_y, momentum_info
                )

    @staticmethod
    def _draw_purple_momentum_indicator(painter, center_x, center_y, momentum_info):
        """
        Draw the triangular momentum indicator for purple dot.

        Args:
            painter: QPainter instance
            center_x, center_y: Center position for the indicator
            momentum_info: Dictionary with angle, size, and speed information
        """
        angle = momentum_info["angle"]
        triangle_size = momentum_info["size"]
        speed = momentum_info["speed"]

        # Calculate color intensity based on speed
        intensity = min(255, int(100 + (speed / MAX_SPEED) * 155))

        # Set triangle color (purple with varying intensity)
        painter.setPen(QPen(QColor(intensity, 0, intensity), 1))
        painter.setBrush(QBrush(QColor(intensity, 0, intensity, 150)))

        # Calculate triangle points (identical to red dot behavior)
        triangle_distance = DOT_RADIUS + MOMENTUM_DISTANCE

        # Tip of triangle (pointing in direction of movement)
        tip_x = center_x + math.cos(angle) * (triangle_distance + triangle_size)
        tip_y = center_y + math.sin(angle) * (triangle_distance + triangle_size)

        # Base points of triangle
        base_angle1 = angle + (2 * math.pi / 3)  # 120 degrees from tip
        base_angle2 = angle - (2 * math.pi / 3)  # 120 degrees from tip (other side)

        base1_x = center_x + math.cos(base_angle1) * triangle_distance
        base1_y = center_y + math.sin(base_angle1) * triangle_distance
        base2_x = center_x + math.cos(base_angle2) * triangle_distance
        base2_y = center_y + math.sin(base_angle2) * triangle_distance

        # Create and draw triangle (using float precision like red dot)
        triangle = QPolygonF(
            [
                QPointF(tip_x, tip_y),
                QPointF(base1_x, base1_y),
                QPointF(base2_x, base2_y),
            ]
        )
        painter.drawPolygon(triangle)

    @staticmethod
    def draw_purple_dot_centered(painter, dot, view_center_x, view_center_y):
        """
        Draw the purple dot at screen center with momentum indicator.

        Args:
            painter: QPainter instance
            dot: PurpleDot instance
            view_center_x, view_center_y: Center coordinates of the current view
        """
        # Get screen position (always at center)
        screen_x, screen_y = view_center_x, view_center_y

        # Choose color based on pulse state
        if dot.is_pulsing():
            purple_color = HP_DAMAGE_PULSE_COLOR  # Yellow when taking HP damage
        else:
            purple_color = (128, 0, 128)  # Normal purple color

        # Draw the dot
        painter.setPen(QPen(QColor(*purple_color), 2))
        painter.setBrush(QBrush(QColor(*purple_color)))
        painter.drawEllipse(
            int(screen_x - dot.radius),
            int(screen_y - dot.radius),
            dot.radius * 2,
            dot.radius * 2,
        )

        # Draw momentum indicator if moving
        momentum_info = dot.get_momentum_info()
        if momentum_info:
            Renderer._draw_purple_momentum_indicator(
                painter, screen_x, screen_y, momentum_info
            )

    @staticmethod
    def draw_red_dot_world(
        painter, dot, camera_x, camera_y, view_center_x, view_center_y
    ):
        """
        Draw the red dot in world coordinates with momentum indicator.

        Args:
            painter: QPainter instance
            dot: RedDot instance
            camera_x, camera_y: Camera position in world coordinates
            view_center_x, view_center_y: Center coordinates of the current view
        """
        # Get screen position relative to camera
        screen_x = dot.virtual_x - (camera_x - view_center_x)
        screen_y = dot.virtual_y - (camera_y - view_center_y)

        # Only draw if visible on screen
        if (
            screen_x + dot.radius >= 0
            and screen_x - dot.radius <= (view_center_x * 2)
            and screen_y + dot.radius >= 0
            and screen_y - dot.radius <= (view_center_y * 2)
        ):

            # Choose color based on pulse state
            if dot.is_pulsing():
                color = HP_DAMAGE_PULSE_COLOR  # Yellow when taking HP damage
            else:
                color = DOT_COLOR  # Normal red color

            # Draw the dot
            painter.setPen(QPen(QColor(*color), 2))
            painter.setBrush(QBrush(QColor(*color)))
            painter.drawEllipse(
                int(screen_x - dot.radius),
                int(screen_y - dot.radius),
                dot.radius * 2,
                dot.radius * 2,
            )

            # Draw momentum indicator if moving
            momentum_info = dot.get_momentum_info()
            if momentum_info:
                Renderer._draw_momentum_indicator(
                    painter, screen_x, screen_y, momentum_info
                )

    @staticmethod
    def draw_off_screen_indicator(
        painter,
        square,
        camera_x,
        camera_y,
        view_width=WINDOW_WIDTH,
        view_height=WINDOW_HEIGHT,
    ):
        """
        Draw an off-screen indicator arrow when the blue square is outside the view.

        Args:
            painter: QPainter instance
            square: BlueSquare instance
            camera_x, camera_y: Camera position in world coordinates
            view_width, view_height: Dimensions of the view area
        """
        if square.is_visible(camera_x, camera_y):
            return  # Don't draw indicator if square is visible

        # Calculate the direction from camera (player) to blue square
        dx = square.x - camera_x
        dy = square.y - camera_y

        # Calculate angle from camera to square
        angle = math.atan2(dy, dx)

        # Define margins from the edge of the screen
        margin = 20
        arrow_size = 12

        # Calculate where the arrow should be positioned on the edge
        center_x = view_width / 2
        center_y = view_height / 2

        # Convert angle to screen edge position
        # We need to determine which edge the arrow should be on
        edge_x = center_x
        edge_y = center_y

        # Normalize direction vector
        distance = math.sqrt(dx * dx + dy * dy)
        if distance > 0:
            norm_dx = dx / distance
            norm_dy = dy / distance

            # Calculate intersection with screen boundaries
            # Check intersection with vertical edges (left/right)
            if norm_dx != 0:
                t_vertical = (view_width / 2 - margin) / abs(norm_dx)
                y_at_vertical = center_y + norm_dy * t_vertical * (
                    1 if norm_dx > 0 else -1
                )

                if abs(y_at_vertical - center_y) <= view_height / 2 - margin:
                    # Arrow goes on left or right edge
                    edge_x = center_x + (view_width / 2 - margin) * (
                        1 if norm_dx > 0 else -1
                    )
                    edge_y = y_at_vertical
                else:
                    # Arrow goes on top or bottom edge
                    t_horizontal = (view_height / 2 - margin) / abs(norm_dy)
                    edge_x = center_x + norm_dx * t_horizontal * (
                        1 if norm_dy > 0 else -1
                    )
                    edge_y = center_y + (view_height / 2 - margin) * (
                        1 if norm_dy > 0 else -1
                    )
            else:
                # Vertical line case
                edge_x = center_x
                edge_y = center_y + (view_height / 2 - margin) * (
                    1 if norm_dy > 0 else -1
                )

        # Draw the arrow indicator
        painter.save()

        # Set up pen and brush for the arrow
        painter.setPen(QPen(QColor(*SQUARE_COLOR), 3))
        painter.setBrush(QBrush(QColor(*SQUARE_COLOR)))

        # Create arrow polygon pointing in the direction of the square
        arrow_points = []

        # Arrow pointing towards the square
        # Base of arrow (back end)
        base_angle1 = angle + math.pi - 0.5
        base_angle2 = angle + math.pi + 0.5

        # Arrow tip (front end)
        tip_x = edge_x + math.cos(angle) * arrow_size
        tip_y = edge_y + math.sin(angle) * arrow_size

        # Arrow base points
        base_x1 = edge_x + math.cos(base_angle1) * arrow_size * 0.6
        base_y1 = edge_y + math.sin(base_angle1) * arrow_size * 0.6
        base_x2 = edge_x + math.cos(base_angle2) * arrow_size * 0.6
        base_y2 = edge_y + math.sin(base_angle2) * arrow_size * 0.6

        # Create arrow polygon
        arrow_polygon = QPolygonF(
            [
                QPointF(tip_x, tip_y),  # Arrow tip
                QPointF(base_x1, base_y1),  # Arrow base left
                QPointF(base_x2, base_y2),  # Arrow base right
            ]
        )

        # Draw the arrow
        painter.drawPolygon(arrow_polygon)

        # Draw a small circle at the base to make it more visible
        painter.setPen(QPen(QColor(*SQUARE_OUTLINE_COLOR), 2))
        painter.setBrush(QBrush(QColor(*SQUARE_COLOR)))
        painter.drawEllipse(int(edge_x - 4), int(edge_y - 4), 8, 8)

        painter.restore()

    @staticmethod
    def draw_static_circles(painter, camera_x, camera_y, view_width, view_height):
        """
        Draw the static decorative circles (red and purple).

        Args:
            painter: QPainter instance
            camera_x, camera_y: Camera position in world coordinates
            view_width, view_height: Dimensions of the view area
        """
        # Import here to avoid circular imports
        from objects import StaticRedCircle, StaticPurpleCircle

        # Create the static circles
        red_circle = StaticRedCircle()
        purple_circle = StaticPurpleCircle()

        # Draw red circle if visible
        if red_circle.is_visible(camera_x, camera_y, view_width, view_height):
            Renderer._draw_static_circle(
                painter, red_circle, camera_x, camera_y, view_width, view_height
            )

        # Draw purple circle if visible
        if purple_circle.is_visible(camera_x, camera_y, view_width, view_height):
            Renderer._draw_static_circle(
                painter, purple_circle, camera_x, camera_y, view_width, view_height
            )

    @staticmethod
    def _draw_static_circle(
        painter, circle, camera_x, camera_y, view_width, view_height
    ):
        """
        Draw a single static circle.

        Args:
            painter: QPainter instance
            circle: StaticCircle instance
            camera_x, camera_y: Camera position in world coordinates
            view_width, view_height: Dimensions of the view area
        """
        # Get screen position
        screen_x, screen_y = circle.get_screen_position(
            camera_x, camera_y, view_width, view_height
        )

        # Set up pen and brush
        painter.setPen(QPen(QColor(*circle.outline_color), 3))
        painter.setBrush(QBrush(QColor(*circle.color)))

        # Draw the circle
        painter.drawEllipse(
            int(screen_x - circle.radius),
            int(screen_y - circle.radius),
            int(circle.radius * 2),
            int(circle.radius * 2),
        )

    @staticmethod
    def draw_gravitational_dots(painter, camera_x, camera_y, view_width, view_height):
        """
        Draw the gravitational dots inside the static circles.

        Args:
            painter: QPainter instance
            camera_x, camera_y: Camera position in world coordinates
            view_width, view_height: Dimensions of the view area
        """
        # Import here to avoid circular imports
        from objects import RedGravitationalDot, PurpleGravitationalDot

        # Create the gravitational dots
        red_gravity_dot = RedGravitationalDot()
        purple_gravity_dot = PurpleGravitationalDot()

        # Draw red gravitational dot if visible
        if red_gravity_dot.is_visible(camera_x, camera_y, view_width, view_height):
            Renderer._draw_gravitational_dot(
                painter, red_gravity_dot, camera_x, camera_y, view_width, view_height
            )

        # Draw purple gravitational dot if visible
        if purple_gravity_dot.is_visible(camera_x, camera_y, view_width, view_height):
            Renderer._draw_gravitational_dot(
                painter, purple_gravity_dot, camera_x, camera_y, view_width, view_height
            )

    @staticmethod
    def _draw_gravitational_dot(
        painter, gravity_dot, camera_x, camera_y, view_width, view_height
    ):
        """
        Draw a single gravitational dot with transparency.

        Args:
            painter: QPainter instance
            gravity_dot: GravitationalDot instance
            camera_x, camera_y: Camera position in world coordinates
            view_width, view_height: Dimensions of the view area
        """
        # Get screen position
        screen_x, screen_y = gravity_dot.get_screen_position(
            camera_x, camera_y, view_width, view_height
        )

        # Set up pen and brush with transparency
        painter.setPen(QPen(QColor(*GRAVITY_DOT_OUTLINE), 2))
        painter.setBrush(QBrush(QColor(*GRAVITY_DOT_COLOR)))

        # Draw the gravitational dot
        painter.drawEllipse(
            int(screen_x - gravity_dot.radius),
            int(screen_y - gravity_dot.radius),
            int(gravity_dot.radius * 2),
            int(gravity_dot.radius * 2),
        )

    @staticmethod
    def draw_score(
        painter,
        red_score,
        purple_score,
        view_width=WINDOW_WIDTH,
        view_height=WINDOW_HEIGHT,
    ):
        """
        Draw the score display at the bottom of the view.

        Args:
            painter: QPainter instance
            red_score: Red player's score
            purple_score: Purple player's score (0 if single player)
            view_width, view_height: Dimensions of the view area
        """
        from PyQt6.QtGui import QFont

        # Set up font and pen for score text
        font = QFont()
        font.setPointSize(SCORE_TEXT_SIZE)
        painter.setFont(font)
        painter.setPen(QPen(QColor(*SCORE_TEXT_COLOR), 2))

        # Calculate positions
        score_y = view_height - SCORE_POSITION_Y_OFFSET

        # Single player mode vs multiplayer mode
        if purple_score is None:
            # Single player mode - just show red score
            score_text = f"Score: {red_score}"
            text_width = painter.fontMetrics().horizontalAdvance(score_text)
            score_x = (view_width - text_width) // 2  # Center horizontally
            painter.drawText(score_x, score_y, score_text)
        else:
            # Multiplayer mode - show both scores
            red_text = f"Red: {red_score}"
            purple_text = f"Purple: {purple_score}"

            # Position red score on left
            red_x = 10
            painter.setPen(QPen(QColor(200, 0, 0), 2))  # Red color for red score
            painter.drawText(red_x, score_y, red_text)

            # Position purple score on right
            purple_width = painter.fontMetrics().horizontalAdvance(purple_text)
            purple_x = view_width - purple_width - 10
            painter.setPen(
                QPen(QColor(128, 0, 128), 2)
            )  # Purple color for purple score
            painter.drawText(purple_x, score_y, purple_text)

    @staticmethod
    def draw_status_display(
        painter,
        red_score,
        purple_score,
        red_hp,
        purple_hp,
        view_width=WINDOW_WIDTH,
        view_height=WINDOW_HEIGHT,
    ):
        """
        Draw score and hit points display at the bottom of the view.

        Args:
            painter: QPainter instance
            red_score: Red player's score
            purple_score: Purple player's score
            red_hp: Red player's hit points
            purple_hp: Purple player's hit points
            view_width: Width of the view
            view_height: Height of the view
        """
        from PyQt6.QtGui import QFont

        # Set up font and pen
        font = QFont()
        font.setPointSize(SCORE_TEXT_SIZE)
        painter.setFont(font)

        # Calculate positions
        score_y = (
            view_height - SCORE_POSITION_Y_OFFSET - 20
        )  # Move up to make room for HP
        hp_y = view_height - SCORE_POSITION_Y_OFFSET

        # Single player mode vs multiplayer mode
        if purple_score is None:
            # Single player mode - show red score and HP
            score_text = f"Score: {red_score}"
            hp_text = f"HP: {red_hp}"

            score_width = painter.fontMetrics().horizontalAdvance(score_text)
            hp_width = painter.fontMetrics().horizontalAdvance(hp_text)

            score_x = (view_width - score_width) // 2
            hp_x = (view_width - hp_width) // 2

            painter.setPen(QPen(QColor(*SCORE_TEXT_COLOR), 2))
            painter.drawText(score_x, score_y, score_text)
            painter.drawText(hp_x, hp_y, hp_text)
        else:
            # Multiplayer mode - show both scores and HP
            red_score_text = f"Red: {red_score}"
            red_hp_text = f"HP: {red_hp}"
            purple_score_text = f"Purple: {purple_score}"
            purple_hp_text = f"HP: {purple_hp}"

            # Position red player info on left
            red_x = 10
            painter.setPen(QPen(QColor(200, 0, 0), 2))  # Red color
            painter.drawText(red_x, score_y, red_score_text)
            painter.drawText(red_x, hp_y, red_hp_text)

            # Position purple player info on right
            purple_score_width = painter.fontMetrics().horizontalAdvance(
                purple_score_text
            )
            purple_hp_width = painter.fontMetrics().horizontalAdvance(purple_hp_text)
            purple_score_x = view_width - purple_score_width - 10
            purple_hp_x = view_width - purple_hp_width - 10

            painter.setPen(QPen(QColor(128, 0, 128), 2))  # Purple color
            painter.drawText(purple_score_x, score_y, purple_score_text)
            painter.drawText(purple_hp_x, hp_y, purple_hp_text)
