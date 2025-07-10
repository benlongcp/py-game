
# BOXHOLE: Topographical Plane Physics Game

An advanced PyQt6-based multi-player physics sandbox featuring split-screen play, black holes with massive gravitational fields, dynamic projectiles, and visually rich effects. Designed for both competitive and cooperative play, with robust modular architecture and extensive test coverage.

---

## 🚀 Quick Start

1. **Install Python 3.10+** (recommended: 3.11+)
2. **Install dependencies:**
   ```bash
   pip install PyQt6
   ```
3. **Run the game:**
   ```bash
   python main.py
   ```

---

## 🕹️ Controls

**Player 1 (Red Dot Window):**
- Move: Arrow Keys (↑↓←→)
- Shoot: Enter

**Player 2 (Purple Dot Window):**
- Move: WASD
- Shoot: Left Ctrl

**Gamepad support:** Both Xbox and compatible controllers supported (see config.py for mappings).

---

## 🎮 Gameplay Overview

- **Split-Screen Multiplayer:** Each player has their own camera and window.
- **Black Holes:** Massive, pulsing gravity fields dominate the arena. Objects are pulled with constant force within the field.
- **Projectiles:** Both players can shoot; projectiles interact with all objects and are affected by gravity.
- **Blue Square:** Central object with rotational physics and collision effects.
- **Decorative Circles:** Red and purple static circles act as scoring zones.
- **Dynamic Grid & Vignette:** Triangular grid and edge-fade for visual depth.
- **Pulse & Momentum Effects:** Visual feedback for movement, collisions, and gravity.

---

## 🏗️ Program Flow

1. **Launch Screen:**
   - Displays "BOXHOLE" title, SVG ships/cubes, and instructions.
   - Any key, mouse, or gamepad input starts the game.
2. **Game Initialization:**
   - Loads configuration and sets up all objects (players, black holes, blue square, static circles).
   - Initializes physics engine and rendering system.
3. **Main Game Loop:**
   - Each player window updates independently but shares the same game state.
   - Handles input, updates physics, processes collisions, and applies gravity.
   - Renders all objects, effects, and overlays (FPS, momentum, pulses, etc.).
4. **Gameplay:**
   - Players move, shoot, and interact with all arena objects.
   - Black holes exert constant gravitational pull within their massive fields.
   - Scoring, hit points, and visual feedback update in real time.
5. **Testing & Debugging:**
   - All test/demo scripts are in `tests/` and can be run independently.

---

## 🛠️ Features & Enhancements

- **Black Hole Enhancements:**
  - Gravitational field radius increased to 18x (675 units, 36x area).
  - Constant gravitational pull within field (no distance falloff).
  - Pulsing gray overlay for visual feedback (smooth sine wave, 0.5s cycle).
- **Launch Screen:**
  - Animated, SVG-based, with instant input detection.
- **Multi-Player System:**
  - Dual windows, independent cameras, synchronized physics.
- **Physics:**
  - Newtonian collisions, rotational inertia, momentum conservation.
- **Visuals:**
  - Triangular grid, vignette, momentum indicators, pulse effects, off-screen arrows.
- **Performance:**
  - Resolution capping, efficient rendering, 60 FPS target.
- **Testing:**
  - 40+ test/demo scripts in `tests/` for every feature and bugfix.

---

## 🗂️ Repository Structure & Information Flow

### Core Architecture

The codebase follows a modular architecture with clear separation of concerns:

```
py-widget/
├── main.py                     # Entry point & launch screen
├── split_screen.py             # Multi-window management
├── game_engine.py              # Centralized game state & logic
├── objects.py                  # Game object classes & SVG data
├── physics.py                  # Physics calculations & collisions
├── rendering.py                # Drawing operations & visual effects
├── config.py                   # All configuration constants
├── gamepad_manager.py          # Input device management
├── rate_limiter.py             # Projectile rate limiting
├── rate_limiter_ui.py          # Rate limiter visualization
├── performance_manager.py      # Performance monitoring
├── powerup_view.py             # Powerup system (unused)
├── topographical_plane.py      # Legacy single-player mode
├── py-widget.py                # Original monolithic version
└── tests/                      # All test/debug/demo scripts
```

### Information Flow

#### 1. **Application Startup**
```
main.py → LaunchScreen → MultiPlayerController → SplitScreenView
```
- `main.py` creates QApplication and MultiPlayerController
- LaunchScreen displays title, captures input, triggers game start
- MultiPlayerController manages game lifecycle
- SplitScreenView creates dual-window split-screen interface

#### 2. **Game Initialization**
```
game_engine.py ← objects.py ← config.py
```
- GameEngine loads configuration from `config.py`
- Creates all game objects (players, black holes, projectiles) from `objects.py`
- Initializes physics systems, timers, and state management

#### 3. **Game Loop (60 FPS)**
```
QTimer → game_engine.update_game_state() → 
├── Input Processing (gamepad_manager.py)
├── Physics Updates (physics.py)
├── Object Updates (objects.py)
├── Collision Detection (physics.py)
├── Rate Limiting (rate_limiter.py)
└── Rendering (rendering.py via split_screen.py)
```

#### 4. **Split-Screen Rendering**
```
split_screen.py → rendering.py → objects.py
```
- Each player window independently calls rendering functions
- Shared GameEngine state ensures synchronized visuals
- Individual cameras follow respective players

### Dependencies & Modules

#### **External Dependencies**
- `PyQt6` — GUI framework, widgets, graphics, SVG rendering
- `math` — Mathematical calculations for physics
- `sys` — System operations and application lifecycle
- `time` — Performance timing and FPS calculations

#### **Internal Module Dependencies**
```
main.py
├── game_engine.py
├── split_screen.py
├── objects.py (SVG data)
├── gamepad_manager.py
└── config.py

split_screen.py
├── rendering.py
├── physics.py
├── objects.py
├── performance_manager.py
└── config.py

game_engine.py
├── objects.py
├── physics.py
├── rate_limiter.py
├── gamepad_manager.py
└── config.py

rendering.py
├── objects.py
├── config.py
└── PyQt6.QtGui

physics.py
├── objects.py
├── config.py
└── math

objects.py
├── config.py
├── physics.py
└── math
```

### Data Flow Patterns

#### **Input Processing**
```
Keyboard/Mouse/Gamepad → gamepad_manager.py → game_engine.py → objects.py (player movement)
```

#### **Physics Pipeline**
```
objects.py (positions) → physics.py (calculations) → objects.py (updated positions/velocities)
```

#### **Rendering Pipeline**
```
objects.py (state) → rendering.py (drawing) → split_screen.py (display) → PyQt6 (screen)
```

#### **Configuration Flow**
```
config.py → all modules (constants, settings, physics parameters)
```

### Testing & Debugging Structure

The `tests/` folder contains isolated test scripts that import and test specific functionality:
- **Feature Tests**: `test_*.py` — Test specific game features
- **Demo Scripts**: `demo_*.py` — Demonstrate functionality
- **Debug Tools**: `check_*.py` — Organization and validation tools

### Performance Considerations

- **Resolution Capping**: Limits render resolution for high-DPI displays
- **Object Pooling**: Reuses projectile objects to reduce garbage collection
- **Efficient Rendering**: Only draws visible objects, cached grid points
- **Modular Updates**: Independent systems update only when necessary

This architecture enables easy maintenance, testing, and feature expansion while maintaining 60 FPS performance across dual windows.

---

## 🧪 Testing & Debugging

All test, debug, and demo scripts are in the `tests/` folder. Example usage:

```bash
# Run a test
python tests/test_black_hole.py

# Demo dynamic scaling
python tests/demo_dynamic_scaling.py

# Check project organization
python tests/check_organization.py
```

---

## 🖥️ Installation & Setup (New System)

1. **Install Python 3.10+** (https://www.python.org/downloads/)
2. **Install PyQt6:**
   ```bash
   pip install PyQt6
   ```
3. **(Optional) Gamepad Support:**
   - For advanced gamepad features, install `inputs` or `pygame` as needed.
4. **Run the game:**
   ```bash
   python main.py
   ```

---

## ℹ️ Notes & Credits

- Designed and developed by Ben Long
- For bug reports, feature requests, or contributions, open an issue or pull request.
- Special thanks to all testers and contributors!

---

Enjoy BOXHOLE — the ultimate topographical physics arena!
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
