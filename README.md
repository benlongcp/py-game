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

- **`tests/`** - **⚠️ ALL test, debug, and demo scripts MUST go here ⚠️**
  - Contains all `test_*.py`, `debug_*.py`, and `demo_*.py` files
  - Includes experimental and prototype scripts
  - **NO test/debug/demo files should EVER be in the main directory**
  - See `tests/ORGANIZATION_GUIDELINES.md` for detailed rules
  - Use `python tests/check_organization.py` to verify compliance
  - Use `python check_org.py` for quick organization checks

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
- **Static decorative circles**: Red and purple circles positioned on opposite ends of the grid
- **Gravitational physics**: Blue square gets pulled toward gravitational dots when overlapping static circles
- **FPS Counter**: Real-time frame rate display at bottom of window for performance monitoring
- **Dynamic Scaling**: Fully resizable window with automatic content scaling

## Usage

### Single Player Mode
Run the application using:
```bash
python main.py
```

### Multi-Player Split-Screen Mode
For two-player split-screen mode, see `MULTIPLAYER_README.md` for detailed instructions.

### Demo and Testing

**⚠️ IMPORTANT: All test, debug, and demo scripts MUST be placed in the `tests/` folder**

```bash
# Test dynamic scaling functionality
python tests/test_dynamic_scaling.py

# Demo the resizable window features
python tests/demo_dynamic_scaling.py

# Test and demo FPS counter
python tests/test_fps_counter.py
python tests/demo_fps_counter.py

# Test gamepad functionality
python tests/test_gamepad_detection.py

# Verify project organization
python tests/check_organization.py

# Run any other test
python tests/test_name.py
```

### Controls

**Single Player Mode:**
- **Arrow Keys**: Move the red dot
- **Enter**: Shoot projectiles

**Multi-Player Mode (Split-Screen):**
- **Player 1 (Red)**: Arrow Keys + Enter
- **Player 2 (Purple)**: WASD + Ctrl

### Movement Physics
- Acceleration while keys are held
- Momentum continues when keys are released
- Deceleration brings dot to stop over ~10 seconds

### FPS Counter
- Real-time frame rate display at the bottom center of the window
- Updates every second showing current performance
- Semi-transparent background for easy reading
- Can be enabled/disabled via `SHOW_FPS_COUNTER` in `config.py`
- Target: ~60 FPS for smooth gameplay
- Useful for performance monitoring and optimization

### Off-Screen Indicators
When the blue square is outside a player's view, a small blue arrow appears on the edge of the screen pointing in the direction of the blue square. This helps players locate the target when it moves off-screen.

### Gravitational Physics
- Two large static circles (red and purple) are positioned on opposite ends of the grid
- Each static circle contains a transparent gravitational dot at its center
- Gravitational field extends beyond the static circle boundary by a distance equal to the circle's radius
- Total gravitational range is 2x the static circle radius (~94 pixels) for extensive strategic influence
- When the blue square enters the gravitational field, it gets pulled toward the gravitational dot
- Gravitational force decreases with distance from the center, creating realistic orbital mechanics
- Use projectiles to push the blue square into gravitational fields and observe the effects

## Configuration

All physics parameters, display settings, and game constants can be adjusted in `config.py`:

- Movement physics (acceleration, max speed, friction)
- Object properties (sizes, masses, colors)
- Collision behavior (restitution, bounce factors)
- Visual settings (grid spacing, vignette effects)
- FPS counter (enable/disable, colors, positioning)

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
