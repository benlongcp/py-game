# Import the sys module for system-specific parameters and functions
import sys

# Import math module for mathematical calculations (sin, cos, etc.)
import math

# Import PyQt6 widgets and classes needed for creating the GUI application
from PyQt6.QtWidgets import QApplication, QWidget

# Import QtGui classes for painting, colors, and graphics
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QRadialGradient, QPolygonF

# Import QtCore classes for geometry and points
from PyQt6.QtCore import Qt, QTimer, QPointF


# Define a custom widget class for the topographical plane view
class TopographicalPlane(QWidget):
    # Constructor method that initializes the widget when an instance is created
    def __init__(self):
        # Call the parent class (QWidget) constructor to properly initialize the widget
        super().__init__()

        # Set the fixed window size to 400x400 pixels
        self.setFixedSize(400, 400)
        # Set the window title that appears in the title bar
        self.setWindowTitle("Topographical Plane View")
        # Set the background color to white
        self.setStyleSheet(
            "background-color: white;"
        )  # Initialize the position of the red dot (starts at center of window)
        self.red_dot_x = 200.0  # X coordinate of red dot (center horizontally) - using float for smooth movement
        self.red_dot_y = 200.0  # Y coordinate of red dot (center vertically) - using float for smooth movement
        # Set the radius of the red dot in pixels
        self.dot_radius = (
            5  # Momentum system variables for acceleration and deceleration
        )
        self.velocity_x = 0.0  # Current velocity in X direction
        self.velocity_y = 0.0  # Current velocity in Y direction
        self.acceleration = 0.1  # How quickly velocity increases when keys are held (reduced for smoother buildup)
        self.deceleration = 0.99  # Friction factor when keys are released (0.99 = 1% speed loss per frame, ~10 second stop time)
        self.max_speed = (
            6.0  # Maximum velocity in any direction (increased for faster top speed)
        )

        # Blue square object properties
        self.square_size = (
            self.dot_radius * 10
        )  # 10x the size of the red dot (50 pixels)
        self.square_x = 300.0  # X coordinate of blue square center (positioned to the right of starting position)
        self.square_y = 150.0  # Y coordinate of blue square center (positioned above starting position)
        self.square_velocity_x = 0.0  # Current velocity of blue square in X direction
        self.square_velocity_y = 0.0  # Current velocity of blue square in Y direction
        self.square_mass = (
            5.0  # Mass of the blue square (heavier than the dot for realistic physics)
        )
        self.dot_mass = (
            1.0  # Mass of the red dot (lighter, more affected by collisions)
        )

        # Set to track which keys are currently pressed for continuous movement
        self.keys_pressed = set()  # Store currently pressed keys

        # Create a timer for smooth continuous movement updates
        self.movement_timer = QTimer()
        # Connect the timer timeout signal to the movement update method
        self.movement_timer.timeout.connect(self.update_movement)
        # Set timer to trigger every 16ms (approximately 60 FPS for smooth animation)
        self.movement_timer.start(16)

        # Enable keyboard focus so the widget can receive key events
        self.setFocusPolicy(
            Qt.FocusPolicy.StrongFocus
        )  # Override the paintEvent method to draw custom graphics on the widget

    def paintEvent(self, event):
        # Create a QPainter object for drawing on this widget
        painter = QPainter(self)
        # Enable antialiasing for smoother drawing
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )  # Draw the triangular grid of light grey dots
        self.draw_triangular_grid(painter)

        # Draw the vignette gradient effect
        self.draw_vignette_gradient(painter)

        # Draw the blue square object
        self.draw_blue_square(painter)

        # Draw the movable red dot (on top of everything)
        self.draw_red_dot(painter)

    def draw_triangular_grid(self, painter):
        # Set the pen color to light grey for drawing the grid dots
        painter.setPen(QPen(QColor(200, 200, 200), 2))
        # Set the brush color to light grey for filling the dots
        painter.setBrush(QBrush(QColor(200, 200, 200)))

        # Define the spacing between grid points
        spacing = 30
        # Define the radius of each grid dot
        grid_dot_radius = 2

        # Calculate the vertical offset for triangular pattern (equilateral triangle height)
        vertical_offset = (
            spacing * math.sqrt(3) / 2
        )  # Define the virtual grid area (2000px diameter circle centered on the window)
        grid_radius = 1000  # 2000px diameter = 1000px radius
        window_center_x, window_center_y = (
            200,
            200,
        )  # Center of the 400x400 window        # Calculate the bounds of the virtual grid relative to the virtual position
        # This creates the illusion that the grid extends beyond the window
        # Use virtual position if it exists, otherwise fall back to red dot position
        virtual_x = getattr(self, "virtual_x", self.red_dot_x)
        virtual_y = getattr(self, "virtual_y", self.red_dot_y)

        grid_center_x = window_center_x - (virtual_x - window_center_x)
        grid_center_y = window_center_y - (virtual_y - window_center_y)

        # Calculate the range of rows and columns to draw (only those visible in window)
        min_y = grid_center_y - grid_radius
        max_y = grid_center_y + grid_radius

        # Start from a row that might be visible and iterate through potential rows
        start_row = int((min_y - grid_center_y) / vertical_offset) - 2
        end_row = int((max_y - grid_center_y) / vertical_offset) + 2

        # Loop through rows to create the triangular grid
        for row in range(start_row, end_row + 1):
            # Calculate the Y position for this row
            y = grid_center_y + (row * vertical_offset)

            # Skip rows that are completely outside the window
            if y < -grid_dot_radius or y > 400 + grid_dot_radius:
                continue

            # Calculate horizontal offset for alternating rows (creates triangular pattern)
            if row % 2 == 0:
                x_offset = 0  # Even rows have no offset
            else:
                x_offset = spacing / 2  # Odd rows are offset by half spacing

            # Calculate the range of columns for this row
            min_x = grid_center_x - grid_radius
            max_x = grid_center_x + grid_radius

            start_col = int((min_x - grid_center_x - x_offset) / spacing) - 1
            end_col = int((max_x - grid_center_x - x_offset) / spacing) + 1

            # Draw dots across the current row
            for col in range(start_col, end_col + 1):
                # Calculate the X position for this column
                x = grid_center_x + x_offset + (col * spacing)

                # Skip dots that are completely outside the window
                if x < -grid_dot_radius or x > 400 + grid_dot_radius:
                    continue  # Check if this dot is within the 2000px diameter circle
                distance_from_grid_center = math.sqrt(
                    (x - grid_center_x) ** 2 + (y - grid_center_y) ** 2
                )
                if distance_from_grid_center > grid_radius:
                    continue  # Skip dots outside the circular grid area

                # Calculate the fade factor based on distance from center for vignette effect
                # This makes dots closer to the edge appear whiter (closer to background)
                fade_start_distance = grid_radius * 0.6  # Start fading at 60% of radius
                if distance_from_grid_center > fade_start_distance:
                    # Calculate how much to fade (0.0 = no fade, 1.0 = full fade to white)
                    fade_factor = (distance_from_grid_center - fade_start_distance) / (
                        grid_radius - fade_start_distance
                    )
                    fade_factor = min(1.0, fade_factor)  # Clamp to maximum of 1.0

                    # Interpolate between gray (200,200,200) and white (255,255,255)
                    gray_value = 200
                    white_value = 255
                    faded_color_value = int(
                        gray_value + (white_value - gray_value) * fade_factor
                    )

                    # Set the faded color for both pen and brush
                    faded_color = QColor(
                        faded_color_value, faded_color_value, faded_color_value
                    )
                    painter.setPen(QPen(faded_color, 2))
                    painter.setBrush(QBrush(faded_color))
                else:
                    # Use original gray color for dots in the center area
                    painter.setPen(QPen(QColor(200, 200, 200), 2))
                    painter.setBrush(QBrush(QColor(200, 200, 200)))

                # Draw a small circle (dot) at the current position
                painter.drawEllipse(
                    int(x - grid_dot_radius),
                    int(y - grid_dot_radius),
                    grid_dot_radius * 2,
                    grid_dot_radius * 2,
                )  # Method to draw a vignette gradient that fades the grid to white near the edges

    def draw_vignette_gradient(self, painter):
        # Calculate the grid center relative to the virtual position
        window_center_x, window_center_y = 200, 200  # Center of the 400x400 window

        # Use virtual position if it exists, otherwise fall back to red dot position
        virtual_x = getattr(self, "virtual_x", self.red_dot_x)
        virtual_y = getattr(self, "virtual_y", self.red_dot_y)

        grid_center_x = window_center_x - (virtual_x - window_center_x)
        grid_center_y = window_center_y - (
            virtual_y - window_center_y
        )  # Define the grid radius (1000px for 2000px diameter)
        grid_radius = 1000

        # Create a radial gradient that provides additional white overlay at the very edges
        gradient = QRadialGradient(grid_center_x, grid_center_y, grid_radius)
        # Most of the area remains transparent since we're now handling fading in the dot drawing
        gradient.setColorAt(0.0, QColor(255, 255, 255, 0))  # Center: fully transparent
        gradient.setColorAt(
            0.85, QColor(255, 255, 255, 0)
        )  # 85% radius: still transparent
        gradient.setColorAt(
            0.95, QColor(255, 255, 255, 50)
        )  # 95% radius: slight white overlay
        gradient.setColorAt(
            1.0, QColor(255, 255, 255, 100)
        )  # Edge: stronger white overlay

        # Set the gradient as the brush for drawing
        painter.setBrush(
            QBrush(gradient)
        )  # Remove the pen (no outline) for the gradient overlay
        painter.setPen(Qt.PenStyle.NoPen)

        # Draw the gradient as a large circle that covers the entire window and beyond
        # We draw it larger than the window to ensure it covers all visible areas
        painter.drawEllipse(
            int(grid_center_x - grid_radius - 200),  # X position (with extra margin)
            int(grid_center_y - grid_radius - 200),  # Y position (with extra margin)
            int((grid_radius + 200) * 2),  # Width (with extra margin)
            int((grid_radius + 200) * 2),  # Height (with extra margin)
        )

    # Method to draw the blue square object
    def draw_blue_square(self, painter):
        # Calculate the square's position relative to the virtual position (for scrolling effect)
        window_center_x, window_center_y = 200, 200
        virtual_x = getattr(self, "virtual_x", self.red_dot_x)
        virtual_y = getattr(self, "virtual_y", self.red_dot_y)

        # Calculate the square's screen position based on virtual camera position
        screen_square_x = self.square_x - (virtual_x - window_center_x)
        screen_square_y = self.square_y - (virtual_y - window_center_y)

        # Only draw the square if it's visible (or partially visible) on screen
        half_size = self.square_size / 2
        if (
            screen_square_x + half_size >= 0
            and screen_square_x - half_size <= 400
            and screen_square_y + half_size >= 0
            and screen_square_y - half_size <= 400
        ):  # Set the pen and brush for the blue square
            painter.setPen(QPen(QColor(0, 0, 255), 2))  # Blue outline
            painter.setBrush(
                QBrush(QColor(0, 100, 255))
            )  # Slightly lighter blue fill            # Calculate exact positions to ensure perfect alignment with collision detection
            # The square center is at (screen_square_x, screen_square_y)
            # The collision detection uses square boundaries as:
            # left = square_x - half_size, right = square_x + half_size
            # top = square_y - half_size, bottom = square_y + half_size

            # For drawing, we need the top-left corner position for drawRect
            # This MUST match exactly with the collision detection boundaries
            exact_left = screen_square_x - half_size
            exact_top = screen_square_y - half_size
            exact_width = self.square_size
            exact_height = self.square_size
            # Draw the rectangle using the exact same coordinate system as collision detection
            # Use QRectF for float coordinates to ensure sub-pixel precision matching collision detection
            from PyQt6.QtCore import QRectF

            rect = QRectF(exact_left, exact_top, exact_width, exact_height)
            painter.drawRect(rect)

    # Method to draw the movable red dot with momentum direction indicator
    def draw_red_dot(self, painter):
        # Set the pen color to red for the dot outline
        painter.setPen(QPen(QColor(255, 0, 0), 2))
        # Set the brush color to red for filling the dot
        painter.setBrush(QBrush(QColor(255, 0, 0)))

        # Calculate the dot's screen position using the same coordinate transform as the blue square
        window_center_x, window_center_y = 200, 200
        virtual_x = getattr(self, "virtual_x", self.red_dot_x)
        virtual_y = getattr(self, "virtual_y", self.red_dot_y)

        # The red dot should always be at the center of the screen (camera follows it)
        # But we'll use the transformation for consistency with the blue square
        screen_dot_x = virtual_x - (
            virtual_x - window_center_x
        )  # This equals window_center_x
        screen_dot_y = virtual_y - (
            virtual_y - window_center_y
        )  # This equals window_center_y

        # Since the camera follows the red dot, it should always be at screen center
        # But let's use the consistent coordinate system
        screen_dot_x = window_center_x  # Red dot is always at screen center
        screen_dot_y = window_center_y  # Red dot is always at screen center

        # Draw the red dot as a circle at the screen position
        painter.drawEllipse(
            int(screen_dot_x - self.dot_radius),  # Convert float to int for drawing
            int(screen_dot_y - self.dot_radius),  # Convert float to int for drawing
            self.dot_radius * 2,
            self.dot_radius * 2,
        )

        # Draw triangular momentum indicator if there's significant velocity
        total_velocity = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        if total_velocity > 0.1:  # Only show pointer if moving with reasonable speed
            # Calculate the angle of movement direction
            angle = math.atan2(self.velocity_y, self.velocity_x)

            # Calculate the size of the triangle based on velocity (larger = faster)
            # Scale between 8 and 20 pixels based on velocity
            triangle_size = min(
                20, max(8, 8 + (total_velocity / self.max_speed) * 12)
            )  # Calculate triangle points relative to the red dot center (using screen coordinates)
            # The triangle points in the direction of momentum
            center_x, center_y = screen_dot_x, screen_dot_y

            # Distance from dot center to triangle tip
            triangle_distance = self.dot_radius + 3

            # Calculate the tip of the triangle (pointing in direction of movement)
            tip_x = center_x + math.cos(angle) * (triangle_distance + triangle_size)
            tip_y = center_y + math.sin(angle) * (triangle_distance + triangle_size)

            # Calculate the base points of the triangle (perpendicular to movement direction)
            base_angle1 = angle + (2 * math.pi / 3)  # 120 degrees from tip
            base_angle2 = angle - (2 * math.pi / 3)  # 120 degrees from tip (other side)

            base1_x = center_x + math.cos(base_angle1) * triangle_distance
            base1_y = center_y + math.sin(base_angle1) * triangle_distance

            base2_x = center_x + math.cos(base_angle2) * triangle_distance
            base2_y = center_y + math.sin(base_angle2) * triangle_distance

            # Create the triangle polygon
            triangle = QPolygonF(
                [
                    QPointF(
                        tip_x, tip_y
                    ),  # Triangle tip (points in direction of movement)
                    QPointF(base1_x, base1_y),  # Base point 1
                    QPointF(base2_x, base2_y),  # Base point 2
                ]
            )  # Set triangle color to match the red dot
            painter.setPen(QPen(QColor(255, 0, 0), 1))
            painter.setBrush(QBrush(QColor(255, 0, 0)))

            # Draw the triangular momentum indicator
            painter.drawPolygon(
                triangle
            )  # Method called by timer to update movement continuously with momentum

    def update_movement(self):
        # Define the grid boundaries for a 2000px diameter circle (1000px radius)
        grid_radius = 1000
        window_center_x, window_center_y = 200, 200  # Center of the 400x400 window

        # Calculate the maximum distance the red dot can move from window center
        max_distance_from_center = (
            grid_radius - window_center_x
        )  # 1000 - 200 = 800 pixels

        # Keep the red dot within the visible window bounds while allowing grid exploration
        min_x = self.dot_radius  # Left edge of window + dot radius
        max_x = 400 - self.dot_radius  # Right edge of window - dot radius
        min_y = self.dot_radius  # Top edge of window + dot radius
        max_y = 400 - self.dot_radius  # Bottom edge of window - dot radius

        # Track the virtual position for grid calculations (can extend beyond window)
        if not hasattr(self, "virtual_x"):
            self.virtual_x = 200.0  # Initialize virtual position at window center
        if not hasattr(self, "virtual_y"):
            self.virtual_y = 200.0  # Initialize virtual position at window center

        # Store old virtual position for comparison
        virtual_old_x, virtual_old_y = self.virtual_x, self.virtual_y

        # Update velocity based on key presses (acceleration) or release (deceleration)
        # Handle horizontal movement
        if Qt.Key.Key_Left in self.keys_pressed:
            # Accelerate left (negative direction)
            self.velocity_x = max(-self.max_speed, self.velocity_x - self.acceleration)
        elif Qt.Key.Key_Right in self.keys_pressed:
            # Accelerate right (positive direction)
            self.velocity_x = min(self.max_speed, self.velocity_x + self.acceleration)
        else:
            # No horizontal keys pressed - apply deceleration (friction)
            self.velocity_x *= self.deceleration
            # Stop very small movements to prevent infinite tiny movements
            if abs(self.velocity_x) < 0.01:
                self.velocity_x = 0.0

        # Handle vertical movement
        if Qt.Key.Key_Up in self.keys_pressed:
            # Accelerate up (negative direction)
            self.velocity_y = max(-self.max_speed, self.velocity_y - self.acceleration)
        elif Qt.Key.Key_Down in self.keys_pressed:
            # Accelerate down (positive direction)
            self.velocity_y = min(self.max_speed, self.velocity_y + self.acceleration)
        else:
            # No vertical keys pressed - apply deceleration (friction)
            self.velocity_y *= (
                self.deceleration
            )  # Stop very small movements to prevent infinite tiny movements
            if abs(self.velocity_y) < 0.01:
                self.velocity_y = 0.0

        # Calculate proposed new position
        new_virtual_x = self.virtual_x + self.velocity_x
        new_virtual_y = self.virtual_y + self.velocity_y

        # Check if the proposed movement would cause collision with the square
        # and prevent the movement if it would cause overlap
        new_virtual_x, new_virtual_y = self.prevent_square_overlap(
            new_virtual_x, new_virtual_y
        )

        # Improved circular boundary detection for the red dot
        # Calculate distance from grid center (200, 200) to new position
        distance_from_center = math.sqrt(
            (new_virtual_x - window_center_x) ** 2
            + (new_virtual_y - window_center_y) ** 2
        )
        max_dot_distance = (
            max_distance_from_center - self.dot_radius
        )  # Account for dot radius

        if distance_from_center > max_dot_distance:
            # Calculate the angle to the new position
            angle = math.atan2(
                new_virtual_y - window_center_y, new_virtual_x - window_center_x
            )

            # Place the dot at the maximum allowed distance in that direction
            self.virtual_x = window_center_x + math.cos(angle) * max_dot_distance
            self.virtual_y = window_center_y + math.sin(angle) * max_dot_distance

            # Calculate velocity components along and perpendicular to the boundary
            velocity_magnitude = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
            if velocity_magnitude > 0:
                # Normalize velocity vector
                vel_x_norm = self.velocity_x / velocity_magnitude
                vel_y_norm = self.velocity_y / velocity_magnitude

                # Calculate normal vector pointing outward from center
                normal_x = math.cos(angle)
                normal_y = math.sin(angle)

                # Calculate dot product (velocity component along normal)
                dot_product = vel_x_norm * normal_x + vel_y_norm * normal_y

                # Remove velocity component pointing into the boundary (bounce effect)
                bounce_factor = 0.6  # Some energy loss on boundary collision
                self.velocity_x = (
                    (vel_x_norm - 2 * dot_product * normal_x)
                    * velocity_magnitude
                    * bounce_factor
                )
                self.velocity_y = (
                    (vel_y_norm - 2 * dot_product * normal_y)
                    * velocity_magnitude
                    * bounce_factor
                )
        else:
            # No boundary collision, apply normal movement
            self.virtual_x = new_virtual_x
            self.virtual_y = new_virtual_y

        # Map the virtual position to the visible red dot position
        # When virtual position is at center (200,200), red dot is at center (200,200)
        # When virtual position is at edges, red dot moves toward window edges
        virtual_distance_from_center_x = self.virtual_x - window_center_x
        virtual_distance_from_center_y = self.virtual_y - window_center_y

        # Scale the red dot position based on virtual position
        # Maximum red dot offset from center is (window_center - dot_radius)
        max_red_dot_offset_x = window_center_x - self.dot_radius  # 195
        max_red_dot_offset_y = window_center_y - self.dot_radius  # 195

        # Calculate red dot position with proportional scaling
        if max_distance_from_center > 0:
            red_dot_offset_x = (
                virtual_distance_from_center_x / max_distance_from_center
            ) * max_red_dot_offset_x
            red_dot_offset_y = (
                virtual_distance_from_center_y / max_distance_from_center
            ) * max_red_dot_offset_y
        else:
            red_dot_offset_x = 0
            red_dot_offset_y = 0

        # Set the actual red dot position (always within window bounds)
        self.red_dot_x = window_center_x + red_dot_offset_x
        self.red_dot_y = (
            window_center_y + red_dot_offset_y
        )  # Ensure red dot stays within window bounds (safety check)
        self.red_dot_x = max(min_x, min(max_x, self.red_dot_x))
        self.red_dot_y = max(min_y, min(max_y, self.red_dot_y))

        # Check for collision between red dot and blue square
        self.check_collision()

        # Update blue square physics (apply deceleration to square)
        self.update_square_physics()

        # If the position changed or there's still velocity, repaint the widget
        if (
            (virtual_old_x, virtual_old_y) != (self.virtual_x, self.virtual_y)
            or abs(self.velocity_x) > 0.01
            or abs(self.velocity_y) > 0.01
            or abs(self.square_velocity_x) > 0.01
            or abs(self.square_velocity_y) > 0.01
        ):
            self.update()  # Trigger a repaint of the widget    # Method to check collision between red dot and blue square with hard boundaries

    def check_collision(self):
        # Get the virtual positions for accurate collision detection
        dot_virtual_x = getattr(self, "virtual_x", 200.0)
        dot_virtual_y = getattr(self, "virtual_y", 200.0)

        # Calculate the boundaries of the square
        half_square = self.square_size / 2
        square_left = self.square_x - half_square
        square_right = self.square_x + half_square
        square_top = self.square_y - half_square
        square_bottom = self.square_y + half_square

        # Calculate the boundaries where the dot center can be (accounting for dot radius)
        collision_left = square_left - self.dot_radius
        collision_right = square_right + self.dot_radius
        collision_top = square_top - self.dot_radius
        collision_bottom = square_bottom + self.dot_radius

        # Check if dot is within the collision zone
        if (
            dot_virtual_x > collision_left
            and dot_virtual_x < collision_right
            and dot_virtual_y > collision_top
            and dot_virtual_y < collision_bottom
        ):

            # Collision detected - determine which side and create hard boundary

            # Calculate distances to each edge
            dist_to_left = abs(dot_virtual_x - collision_left)
            dist_to_right = abs(dot_virtual_x - collision_right)
            dist_to_top = abs(dot_virtual_y - collision_top)
            dist_to_bottom = abs(dot_virtual_y - collision_bottom)

            # Find the closest edge (most recent collision)
            min_distance = min(dist_to_left, dist_to_right, dist_to_top, dist_to_bottom)

            if min_distance == dist_to_left:
                # Hit left side - push dot to the left
                self.virtual_x = collision_left
                collision_normal_x, collision_normal_y = -1, 0
            elif min_distance == dist_to_right:
                # Hit right side - push dot to the right
                self.virtual_x = collision_right
                collision_normal_x, collision_normal_y = 1, 0
            elif min_distance == dist_to_top:
                # Hit top side - push dot up
                self.virtual_y = collision_top
                collision_normal_x, collision_normal_y = 0, -1
            else:  # min_distance == dist_to_bottom
                # Hit bottom side - push dot down
                self.virtual_y = collision_bottom
                collision_normal_x, collision_normal_y = 0, 1

            # Apply collision physics with hard boundary constraint
            self.apply_collision_physics(collision_normal_x, collision_normal_y)

            # Additional check: ensure dot never overlaps square after physics
            self.enforce_hard_boundary()

    # Method to apply classical mechanics collision physics
    def apply_collision_physics(self, normal_x, normal_y):
        # Calculate relative velocity
        relative_velocity_x = self.velocity_x - self.square_velocity_x
        relative_velocity_y = self.velocity_y - self.square_velocity_y

        # Calculate relative velocity in collision normal direction
        relative_velocity_normal = (
            relative_velocity_x * normal_x + relative_velocity_y * normal_y
        )

        # Don't resolve if velocities are separating
        if relative_velocity_normal > 0:
            return

        # Calculate restitution (bounciness) - 0.8 for slightly bouncy collisions
        restitution = 0.8

        # Calculate impulse scalar
        impulse_scalar = -(1 + restitution) * relative_velocity_normal
        impulse_scalar /= 1 / self.dot_mass + 1 / self.square_mass

        # Calculate impulse vector
        impulse_x = impulse_scalar * normal_x
        impulse_y = impulse_scalar * normal_y

        # Apply impulse to dot (reduce its velocity)
        self.velocity_x += impulse_x / self.dot_mass
        self.velocity_y += impulse_y / self.dot_mass

        # Apply opposite impulse to square (increase its velocity)
        self.square_velocity_x -= impulse_x / self.square_mass
        self.square_velocity_y -= (
            impulse_y / self.square_mass
        )  # Cap velocities to reasonable limits
        max_square_speed = 3.0
        square_speed = math.sqrt(self.square_velocity_x**2 + self.square_velocity_y**2)
        if square_speed > max_square_speed:
            self.square_velocity_x = (
                self.square_velocity_x / square_speed
            ) * max_square_speed
            self.square_velocity_y = (
                self.square_velocity_y / square_speed
            ) * max_square_speed

    # Method to enforce hard boundary - ensures dot never overlaps square
    def enforce_hard_boundary(self):
        # Get current dot position
        dot_virtual_x = getattr(self, "virtual_x", 200.0)
        dot_virtual_y = getattr(self, "virtual_y", 200.0)

        # Calculate the boundaries of the square
        half_square = self.square_size / 2
        square_left = self.square_x - half_square
        square_right = self.square_x + half_square
        square_top = self.square_y - half_square
        square_bottom = self.square_y + half_square

        # Calculate the boundaries where the dot center can be (accounting for dot radius)
        collision_left = square_left - self.dot_radius
        collision_right = square_right + self.dot_radius
        collision_top = square_top - self.dot_radius
        collision_bottom = square_bottom + self.dot_radius

        # Check if dot is still overlapping and force it out
        if (
            dot_virtual_x > collision_left
            and dot_virtual_x < collision_right
            and dot_virtual_y > collision_top
            and dot_virtual_y < collision_bottom
        ):

            # Calculate distances to each boundary
            dist_to_left = dot_virtual_x - collision_left
            dist_to_right = collision_right - dot_virtual_x
            dist_to_top = dot_virtual_y - collision_top
            dist_to_bottom = collision_bottom - dot_virtual_y

            # Find the closest boundary and push dot to that side
            min_distance = min(dist_to_left, dist_to_right, dist_to_top, dist_to_bottom)

            if min_distance == dist_to_left:
                # Push to left boundary
                self.virtual_x = collision_left
                # Stop velocity components that would push into the square
                if self.velocity_x > 0:
                    self.velocity_x = 0
            elif min_distance == dist_to_right:
                # Push to right boundary
                self.virtual_x = collision_right
                # Stop velocity components that would push into the square
                if self.velocity_x < 0:
                    self.velocity_x = 0
            elif min_distance == dist_to_top:
                # Push to top boundary
                self.virtual_y = collision_top
                # Stop velocity components that would push into the square
                if self.velocity_y > 0:
                    self.velocity_y = 0
            else:  # min_distance == dist_to_bottom
                # Push to bottom boundary
                self.virtual_y = collision_bottom  # Stop velocity components that would push into the square
                if self.velocity_y < 0:
                    self.velocity_y = 0

    # Method to prevent movement that would cause overlap with the square
    def prevent_square_overlap(self, proposed_x, proposed_y):
        # Calculate the boundaries of the square
        half_square = self.square_size / 2
        square_left = self.square_x - half_square
        square_right = self.square_x + half_square
        square_top = self.square_y - half_square
        square_bottom = self.square_y + half_square

        # Calculate the boundaries where the dot center can be (accounting for dot radius)
        collision_left = square_left - self.dot_radius
        collision_right = square_right + self.dot_radius
        collision_top = square_top - self.dot_radius
        collision_bottom = square_bottom + self.dot_radius

        # Check if proposed position would overlap
        if (
            proposed_x > collision_left
            and proposed_x < collision_right
            and proposed_y > collision_top
            and proposed_y < collision_bottom
        ):

            # Proposed position would cause overlap - find safe position
            current_x = getattr(self, "virtual_x", 200.0)
            current_y = getattr(self, "virtual_y", 200.0)

            # Try moving only in X direction
            if (
                current_x <= collision_left
                or current_x >= collision_right
                or proposed_y <= collision_top
                or proposed_y >= collision_bottom
            ):
                # Safe to move in X direction
                safe_x = proposed_x
                safe_y = current_y
            # Try moving only in Y direction
            elif (
                current_y <= collision_top
                or current_y >= collision_bottom
                or proposed_x <= collision_left
                or proposed_x >= collision_right
            ):
                # Safe to move in Y direction
                safe_x = current_x
                safe_y = proposed_y
            else:
                # Can't move in either direction safely - stay put
                safe_x = current_x
                safe_y = current_y
                # Stop velocity to prevent constant collision attempts
                self.velocity_x *= 0.5
                self.velocity_y *= 0.5

            return safe_x, safe_y
        else:
            # Proposed position is safe
            return proposed_x, proposed_y

    # Method to update blue square physics
    def update_square_physics(self):
        # Apply position update based on velocity
        self.square_x += self.square_velocity_x
        self.square_y += self.square_velocity_y

        # Apply deceleration to square (more friction than the dot)
        square_deceleration = 0.95  # More friction for the square
        self.square_velocity_x *= square_deceleration
        self.square_velocity_y *= square_deceleration  # Stop very small movements
        if abs(self.square_velocity_x) < 0.01:
            self.square_velocity_x = 0.0
        if abs(self.square_velocity_y) < 0.01:
            self.square_velocity_y = 0.0

        # Improved circular boundary detection for the blue square
        grid_radius = 1000
        window_center_x, window_center_y = 200, 200
        half_square = self.square_size / 2

        # Calculate the new position after applying velocity
        new_square_x = self.square_x + self.square_velocity_x
        new_square_y = self.square_y + self.square_velocity_y

        # Check if any corner of the square would be outside the circular boundary
        square_corners = [
            (new_square_x - half_square, new_square_y - half_square),  # Top-left
            (new_square_x + half_square, new_square_y - half_square),  # Top-right
            (new_square_x - half_square, new_square_y + half_square),  # Bottom-left
            (new_square_x + half_square, new_square_y + half_square),  # Bottom-right
        ]

        collision_detected = False
        max_allowed_distance = grid_radius

        # Check each corner for boundary collision
        for corner_x, corner_y in square_corners:
            distance_from_center = math.sqrt(
                (corner_x - window_center_x) ** 2 + (corner_y - window_center_y) ** 2
            )
            if distance_from_center > max_allowed_distance:
                collision_detected = True
                break

        if collision_detected:
            # Find the closest valid position for the square center
            # Calculate distance from center to square center
            center_distance = math.sqrt(
                (new_square_x - window_center_x) ** 2
                + (new_square_y - window_center_y) ** 2
            )

            if center_distance > 0:
                # Calculate the angle to the square center
                angle = math.atan2(
                    new_square_y - window_center_y, new_square_x - window_center_x
                )

                # Calculate maximum distance for square center (accounting for square corners)
                # The farthest corner is at distance half_square * sqrt(2) from center
                max_square_center_distance = max_allowed_distance - (
                    half_square * math.sqrt(2)
                )

                # Clamp square to valid position
                self.square_x = (
                    window_center_x + math.cos(angle) * max_square_center_distance
                )
                self.square_y = (
                    window_center_y + math.sin(angle) * max_square_center_distance
                )

                # Apply realistic bounce physics
                velocity_magnitude = math.sqrt(
                    self.square_velocity_x**2 + self.square_velocity_y**2
                )
                if velocity_magnitude > 0:
                    # Normalize velocity vector
                    vel_x_norm = self.square_velocity_x / velocity_magnitude
                    vel_y_norm = self.square_velocity_y / velocity_magnitude

                    # Calculate normal vector pointing outward from center
                    normal_x = math.cos(angle)
                    normal_y = math.sin(angle)

                    # Calculate dot product (velocity component along normal)
                    dot_product = vel_x_norm * normal_x + vel_y_norm * normal_y

                    # Apply bounce with energy loss
                    bounce_factor = 0.5  # More energy loss for the heavier square
                    self.square_velocity_x = (
                        (vel_x_norm - 2 * dot_product * normal_x)
                        * velocity_magnitude
                        * bounce_factor
                    )
                    self.square_velocity_y = (
                        (vel_y_norm - 2 * dot_product * normal_y)
                        * velocity_magnitude
                        * bounce_factor
                    )
        else:
            # No boundary collision, apply normal movement
            self.square_x = new_square_x
            self.square_y = new_square_y  # Override the keyPressEvent method to handle when keys are pressed down

    def keyPressEvent(self, event):
        # Add the pressed key to our set of currently pressed keys
        if event.key() in [
            Qt.Key.Key_Left,
            Qt.Key.Key_Right,
            Qt.Key.Key_Up,
            Qt.Key.Key_Down,
        ]:
            self.keys_pressed.add(event.key())

        # Call the parent class method to handle any other key events
        super().keyPressEvent(event)

    # Override the keyReleaseEvent method to handle when keys are released
    def keyReleaseEvent(self, event):
        # Remove the released key from our set of currently pressed keys
        if event.key() in self.keys_pressed:
            self.keys_pressed.remove(event.key())

        # Call the parent class method to handle any other key events
        super().keyReleaseEvent(event)


# Create a QApplication instance, which manages the GUI application's control flow
# sys.argv passes command-line arguments to the application
app = QApplication(sys.argv)
# Create an instance of our custom TopographicalPlane widget
window = TopographicalPlane()
# Make the window visible on the screen
window.show()
# Start the application's event loop and exit when the application is closed
# app.exec() runs the main event loop, sys.exit() ensures clean program termination
sys.exit(app.exec())
