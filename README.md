
# HOLE BALL: Topographical Plane Physics Game

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
   - Displays "HOLE BALL" title, SVG ships/cubes, and instructions.
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

## 🗂️ File/Folder Structure

- `main.py` — Entry point, game/launch screen logic
- `split_screen.py` — Multi-window management
- `objects.py` — All game object classes (players, black holes, projectiles, etc.)
- `physics.py` — Physics and collision logic
- `rendering.py` — All drawing and visual effects
- `config.py` — All game constants and settings
- `tests/` — All test, debug, and demo scripts (see below)
- `README.md` — This file

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

Enjoy HOLE BALL — the ultimate topographical physics arena!
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
