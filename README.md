# Topographical Plane Application

A PyQt6-based interactive simulation featuring a red dot that moves on a triangular grid with physics-based collision detection against a blue square obstacle.

## Architecture

The application has been modularized into the following components:

### Core Modules

- **`main.py`** - Application entry point
- **`topographical_plane.py`** - Main widget class that orchestrates the simulation
- **`config.py`** - All configuration constants and settings
- **`objects.py`** - Game object classes (RedDot, BlueSquare)
- **`physics.py`** - Physics calculations and collision detection
- **`rendering.py`** - All drawing/rendering operations

### Testing & Debug

- **`tests/`** - Directory containing test and debug scripts
  - **`test_alignment.py`** - Tests coordinate alignment between drawing and collision
  - **`debug_coordinates.py`** - Debug script for coordinate system analysis
  - **`debug_moving_scenario.py`** - Debug script for camera movement scenarios

### Legacy Files

- **`py-widget.py`** - Original monolithic implementation (kept for reference)

## Features

- **Smooth movement**: Red dot moves with momentum-based physics
- **Collision detection**: Realistic collision between red dot and blue square
- **Boundary constraints**: Both objects respect circular grid boundaries
- **Visual feedback**: Momentum indicator shows direction and speed
- **Camera system**: View follows the red dot with coordinate transformation
- **Triangular grid**: Procedurally generated dot pattern with vignette effect
- **Multi-player support**: Two players can play simultaneously with split-screen view
- **Projectile system**: Players can shoot projectiles that interact with all objects
- **Off-screen indicators**: Blue arrows point toward the blue square when it's outside view
- **Newtonian physics**: All interactions follow conservation of momentum

## Usage

### Single Player Mode
Run the application using:
```bash
python main.py
```

### Multi-Player Split-Screen Mode
For two-player split-screen mode, see `MULTIPLAYER_README.md` for detailed instructions.

### Demo and Testing
```bash
# Test off-screen indicators
python tests/demo_off_screen_indicator.py

# Run other tests
python tests/test_name.py
```

### Controls

**Single Player Mode:**
- **Arrow Keys**: Move the red dot
- **Space**: Shoot projectiles

**Multi-Player Mode (Split-Screen):**
- **Player 1 (Red)**: Arrow Keys + Space
- **Player 2 (Purple)**: WASD + Ctrl

### Movement Physics
- Acceleration while keys are held
- Momentum continues when keys are released
- Deceleration brings dot to stop over ~10 seconds

### Off-Screen Indicators
When the blue square is outside a player's view, a small blue arrow appears on the edge of the screen pointing in the direction of the blue square. This helps players locate the target when it moves off-screen.

## Configuration

All physics parameters, display settings, and game constants can be adjusted in `config.py`:

- Movement physics (acceleration, max speed, friction)
- Object properties (sizes, masses, colors)
- Collision behavior (restitution, bounce factors)
- Visual settings (grid spacing, vignette effects)

## Physics

The simulation implements:

- **Conservation of momentum** in collisions
- **Circular boundary constraints** for both objects
- **Realistic collision response** with energy transfer
- **Friction and deceleration** for natural movement

## Development

The modular architecture makes it easy to:

- Adjust physics parameters in `config.py`
- Add new object types in `objects.py`
- Implement new rendering effects in `rendering.py`
- Extend physics calculations in `physics.py`

Each module has clear responsibilities and minimal coupling, making the codebase maintainable and extensible.
