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
    def draw_triangular_grid(painter, camera_x, camera_y):
        """
        Draw the triangular grid of dots.

        Args:
            painter: QPainter instance
            camera_x, camera_y: Camera position in world coordinates
        """
        # Set pen and brush for grid dots
        painter.setPen(QPen(QColor(*GRID_COLOR), 2))
        painter.setBrush(
            QBrush(QColor(*GRID_COLOR))
        )  # Calculate grid center position on screen
        # The world origin (0,0) should appear at screen coordinates that account for camera offset
        world_origin_screen_x = WINDOW_CENTER_X - camera_x
        world_origin_screen_y = WINDOW_CENTER_Y - camera_y

        grid_center_x = world_origin_screen_x
        grid_center_y = world_origin_screen_y

        # Calculate vertical offset for triangular pattern
        vertical_offset = GRID_SPACING * math.sqrt(3) / 2

        # Calculate visible range
        min_y = grid_center_y - GRID_RADIUS
        max_y = grid_center_y + GRID_RADIUS

        start_row = int((min_y - grid_center_y) / vertical_offset) - 2
        end_row = int((max_y - grid_center_y) / vertical_offset) + 2

        # Draw grid rows
        for row in range(start_row, end_row + 1):
            y = grid_center_y + (row * vertical_offset)

            # Skip rows outside the window
            if y < -GRID_DOT_RADIUS or y > WINDOW_HEIGHT + GRID_DOT_RADIUS:
                continue

            # Calculate horizontal offset for triangular pattern
            x_offset = 0 if row % 2 == 0 else GRID_SPACING / 2

            # Calculate visible columns for this row
            min_x = grid_center_x - GRID_RADIUS
            max_x = grid_center_x + GRID_RADIUS

            start_col = int((min_x - grid_center_x - x_offset) / GRID_SPACING) - 1
            end_col = int((max_x - grid_center_x - x_offset) / GRID_SPACING) + 1

            # Draw dots in this row
            for col in range(start_col, end_col + 1):
                x = grid_center_x + (col * GRID_SPACING) + x_offset

                # Skip dots outside the window
                if x < -GRID_DOT_RADIUS or x > WINDOW_WIDTH + GRID_DOT_RADIUS:
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
    def draw_vignette_gradient(painter, camera_x, camera_y):
        """
        Draw the vignette gradient effect at the grid boundary.

        Args:
            painter: QPainter instance
            camera_x, camera_y: Camera position in world coordinates
        """  # Calculate grid center position on screen (same as triangular grid)
        # The world origin (0,0) should appear at screen coordinates that account for camera offset
        world_origin_screen_x = WINDOW_CENTER_X - camera_x
        world_origin_screen_y = WINDOW_CENTER_Y - camera_y

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
    def draw_blue_square(painter, square, camera_x, camera_y):
        """
        Draw the blue square object.

        Args:
            painter: QPainter instance
            square: BlueSquare instance
            camera_x, camera_y: Camera position in world coordinates
        """
        if not square.is_visible(camera_x, camera_y):
            return  # Get screen position
        screen_x, screen_y = square.get_screen_position(camera_x, camera_y)

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
    def draw_red_dot(painter, dot):
        """
        Draw the red dot with momentum indicator.

        Args:
            painter: QPainter instance
            dot: RedDot instance
        """
        # Get screen position (always at center)
        screen_x, screen_y = dot.get_screen_position()

        # Draw the dot
        painter.setPen(QPen(QColor(*DOT_COLOR), 2))
        painter.setBrush(QBrush(QColor(*DOT_COLOR)))
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
    def draw_projectiles(painter, projectiles, camera_x, camera_y):
        """
        Draw all active projectiles.

        Args:
            painter: QPainter instance
            projectiles: List of Projectile instances
            camera_x, camera_y: Camera position in world coordinates
        """
        # Set pen and brush for projectiles
        painter.setPen(QPen(QColor(*PROJECTILE_COLOR), 1))
        painter.setBrush(QBrush(QColor(*PROJECTILE_COLOR)))

        for projectile in projectiles:
            if not projectile.is_active or not projectile.is_visible(
                camera_x, camera_y
            ):
                continue

            # Get screen position
            screen_x, screen_y = projectile.get_screen_position(camera_x, camera_y)

            # Draw the projectile as a small circle
            painter.drawEllipse(
                int(screen_x - projectile.radius),
                int(screen_y - projectile.radius),
                projectile.radius * 2,
                projectile.radius * 2,
            )

    @staticmethod
    def draw_purple_dot(painter, dot, camera_x, camera_y):
        """
        Draw the purple dot with momentum indicator.

        Args:
            painter: QPainter instance
            dot: PurpleDot instance
            camera_x, camera_y: Camera position in world coordinates
        """
        # Get screen position relative to camera
        screen_x = dot.virtual_x - (camera_x - WINDOW_CENTER_X)
        screen_y = dot.virtual_y - (camera_y - WINDOW_CENTER_Y)

        # Only draw if visible on screen
        if (
            screen_x + dot.radius >= 0
            and screen_x - dot.radius <= WINDOW_WIDTH
            and screen_y + dot.radius >= 0
            and screen_y - dot.radius <= WINDOW_HEIGHT
        ):

            # Draw the dot in purple
            purple_color = (128, 0, 128)  # Purple
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
    def draw_purple_dot_centered(painter, dot):
        """
        Draw the purple dot at screen center with momentum indicator.

        Args:
            painter: QPainter instance
            dot: PurpleDot instance
        """
        # Get screen position (always at center)
        screen_x, screen_y = WINDOW_CENTER_X, WINDOW_CENTER_Y

        # Draw the dot in purple
        purple_color = (128, 0, 128)  # Purple
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
    def draw_red_dot_world(painter, dot, camera_x, camera_y):
        """
        Draw the red dot in world coordinates with momentum indicator.

        Args:
            painter: QPainter instance
            dot: RedDot instance
            camera_x, camera_y: Camera position in world coordinates
        """
        # Get screen position relative to camera
        screen_x = dot.virtual_x - (camera_x - WINDOW_CENTER_X)
        screen_y = dot.virtual_y - (camera_y - WINDOW_CENTER_Y)

        # Only draw if visible on screen
        if (
            screen_x + dot.radius >= 0
            and screen_x - dot.radius <= WINDOW_WIDTH
            and screen_y + dot.radius >= 0
            and screen_y - dot.radius <= WINDOW_HEIGHT
        ):

            # Draw the dot in red
            painter.setPen(QPen(QColor(*DOT_COLOR), 2))
            painter.setBrush(QBrush(QColor(*DOT_COLOR)))
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
    def draw_static_circles(painter, camera_x, camera_y):
        """
        Draw the static decorative circles (red and purple).

        Args:
            painter: QPainter instance
            camera_x, camera_y: Camera position in world coordinates
        """
        # Import here to avoid circular imports
        from objects import StaticRedCircle, StaticPurpleCircle

        # Create the static circles
        red_circle = StaticRedCircle()
        purple_circle = StaticPurpleCircle()

        # Draw red circle if visible
        if red_circle.is_visible(camera_x, camera_y):
            Renderer._draw_static_circle(painter, red_circle, camera_x, camera_y)

        # Draw purple circle if visible
        if purple_circle.is_visible(camera_x, camera_y):
            Renderer._draw_static_circle(painter, purple_circle, camera_x, camera_y)

    @staticmethod
    def _draw_static_circle(painter, circle, camera_x, camera_y):
        """
        Draw a single static circle.

        Args:
            painter: QPainter instance
            circle: StaticCircle instance
            camera_x, camera_y: Camera position in world coordinates
        """
        # Get screen position
        screen_x, screen_y = circle.get_screen_position(camera_x, camera_y)

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
