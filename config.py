"""
Configuration constants for the Topographical Plane application.
Contains all physics parameters, display settings, and game constants.
"""

# Window and display settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
WINDOW_CENTER_X = 400
WINDOW_CENTER_Y = 400
FPS = 60  # Target frames per second
FRAME_TIME_MS = 16  # Milliseconds per frame (1000/60 ≈ 16)

# Grid settings
GRID_SPACING = 30
GRID_DOT_RADIUS = 2
GRID_RADIUS = 1000  # 2000px diameter = 1000px radius
GRID_COLOR = (200, 200, 200)  # Light grey

# Red dot settings
DOT_RADIUS = 5
DOT_COLOR = (255, 0, 0)  # Red
DOT_MASS = 5.0  # Increased from 1.0 to 5.0 for more impactful collisions

# Purple dot settings (Player 2)
PURPLE_DOT_COLOR = (128, 0, 128)  # Purple

# HP damage pulse settings
HP_DAMAGE_PULSE_COLOR = (255, 255, 0)  # Yellow for HP damage pulse

# Red dot physics
ACCELERATION = 0.1  # How quickly velocity increases when keys are held
DECELERATION = (
    0.99  # Friction factor (0.99 = 1% speed loss per frame, ~10 second stop time)
)
MAX_SPEED = 60.0  # Maximum velocity in any direction (increased 10x from 6.0 for high-speed gameplay)

# Projectile settings
PROJECTILE_RADIUS = 2  # Smaller than the red dot
PROJECTILE_COLOR = (0, 255, 0)  # Green
PROJECTILE_MIN_SPEED = 5.0  # Minimum projectile speed
PROJECTILE_MASS = 5  # Light mass for projectiles
PROJECTILE_MAX_COUNT = 20  # Maximum number of projectiles on screen

# Blue square settings
SQUARE_SIZE_MULTIPLIER = 10  # Square is 10x the size of the red dot
SQUARE_COLOR = (0, 100, 255)  # Blue
SQUARE_OUTLINE_COLOR = (0, 0, 255)  # Darker blue outline
SQUARE_PULSE_COLOR = (100, 200, 255)  # Lighter blue for collision pulse
SQUARE_PULSE_DURATION = 20  # Duration of pulse effect in frames
SQUARE_MASS = 5.0

# Blue square physics
SQUARE_FRICTION = 0.995  # Friction for the blue square

# Rotational physics for blue square
ANGULAR_FRICTION = 0.98  # Rotational friction (similar to linear friction)
MAX_ANGULAR_VELOCITY = 5.0  # Maximum rotation speed (radians per frame)
MOMENT_OF_INERTIA_FACTOR = (
    0.5  # Factor for calculating moment of inertia (I = factor * mass * radius^2)
)

# Collision physics
BOUNCE_FACTOR = 0.6  # Energy loss on boundary collision
RESTITUTION = 0.8  # Bounciness in collisions (0 = no bounce, 1 = perfect bounce)

# Momentum indicator settings
MOMENTUM_MIN_SPEED = 0.1  # Minimum speed to show momentum indicator
MOMENTUM_MIN_SIZE = 8  # Minimum triangle size
MOMENTUM_MAX_SIZE = 20  # Maximum triangle size
MOMENTUM_DISTANCE = 3  # Distance from dot center to triangle

# Vignette settings
VIGNETTE_INNER_RADIUS = 150  # Inner radius where vignette starts
VIGNETTE_OUTER_RADIUS = 200  # Outer radius where vignette is fully opaque
VIGNETTE_COLOR = (255, 255, 255, 0)  # White, transparent at center
VIGNETTE_EDGE_COLOR = (255, 255, 255, 200)  # White, mostly opaque at edge

# Starting positions
# Red player starts in purple circle goal, purple player starts in red circle goal
# Note: Static circles are at (-800, 0) for red and (800, 0) for purple
RED_PLAYER_INITIAL_X = 800.0  # Red player starts in purple goal (right side)
RED_PLAYER_INITIAL_Y = 0.0
PURPLE_PLAYER_INITIAL_X = -800.0  # Purple player starts in red goal (left side)
PURPLE_PLAYER_INITIAL_Y = 0.0

# Legacy starting position (for backward compatibility)
INITIAL_DOT_X = RED_PLAYER_INITIAL_X  # Default to red player position
INITIAL_DOT_Y = RED_PLAYER_INITIAL_Y

INITIAL_SQUARE_X = 0.0  # Start at center of grid (same as central gravity point)
INITIAL_SQUARE_Y = 0.0  # Start at center of grid (same as central gravity point)

# Static decorative circles
# Blue square diagonal: sqrt(2) * (DOT_RADIUS * SQUARE_SIZE_MULTIPLIER)
# Circle diameter should be 10% larger than square diagonal
import math

SQUARE_DIAGONAL = math.sqrt(2) * (DOT_RADIUS * SQUARE_SIZE_MULTIPLIER)
STATIC_CIRCLE_DIAMETER = SQUARE_DIAGONAL * 2.66  # Doubled from 1.33 to 2.66
STATIC_CIRCLE_RADIUS = STATIC_CIRCLE_DIAMETER / 2

# Static circle positions (on equator line, opposite ends)
STATIC_CIRCLE_DISTANCE = GRID_RADIUS * 0.8  # 80% of grid radius to stay within bounds
STATIC_RED_CIRCLE_X = -STATIC_CIRCLE_DISTANCE
STATIC_RED_CIRCLE_Y = 0.0
STATIC_PURPLE_CIRCLE_X = STATIC_CIRCLE_DISTANCE
STATIC_PURPLE_CIRCLE_Y = 0.0

# Static circle colors
STATIC_RED_CIRCLE_COLOR = (255, 50, 50)  # Red circle
STATIC_RED_CIRCLE_OUTLINE = (200, 0, 0)  # Darker red outline
STATIC_PURPLE_CIRCLE_COLOR = (200, 50, 255)  # Purple circle
STATIC_PURPLE_CIRCLE_OUTLINE = (150, 0, 200)  # Darker purple outline

# Gravitational dots inside static circles
GRAVITY_DOT_RADIUS = DOT_RADIUS * 1.5  # 1.5x the size of player dots
GRAVITY_DOT_COLOR = (100, 100, 100, 100)  # Semi-transparent gray (with alpha)
GRAVITY_DOT_OUTLINE = (80, 80, 80, 150)  # Slightly more opaque outline

# Gravitational physics
GRAVITY_STRENGTH = 25.0  # Force multiplier for gravitational pull
GRAVITY_MAX_DISTANCE = (
    STATIC_CIRCLE_RADIUS
    * 8  # Circle radius + three radius extensions beyond boundary (total 4x radius)
)
GRAVITY_FALLOFF_POWER = (
    1.5  # How quickly gravity falls off with distance (higher = more focused)
)

# Central gravity point (invisible)
CENTRAL_GRAVITY_X = 0.0  # Center of grid
CENTRAL_GRAVITY_Y = 0.0  # Center of grid
CENTRAL_GRAVITY_RADIUS = (
    GRAVITY_DOT_RADIUS  # Same size as other gravity dots (but invisible)
)
CENTRAL_GRAVITY_MAX_DISTANCE = (
    STATIC_CIRCLE_RADIUS * 4
)  # Half the range of static circle gravity
CENTRAL_GRAVITY_STRENGTH = (
    GRAVITY_STRENGTH * 0.5
)  # Half the strength of static circle gravity

# Scoring system
SCORE_OVERLAP_TIME = (
    0.5  # Seconds the blue square must be fully inside a static circle to score
)
SCORE_OVERLAP_FRAMES = int(SCORE_OVERLAP_TIME * FPS)  # Convert to frames
BLUE_SQUARE_RESPAWN_X = 0.0  # Center of grid
BLUE_SQUARE_RESPAWN_Y = 0.0  # Center of grid
STATIC_CIRCLE_SCORE_POINTS = 2  # Points awarded for static circle scoring

# Hit Points system
INITIAL_HIT_POINTS = 10  # Starting hit points for each player
HIT_POINT_DAMAGE = 1  # Damage per collision/contact

# Score display
SCORE_TEXT_SIZE = 14
SCORE_TEXT_COLOR = (0, 0, 0)  # Black text
SCORE_POSITION_Y_OFFSET = 10  # Distance from bottom of screen
