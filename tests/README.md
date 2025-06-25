# Tests

This directory contains the essential test suite for the Topographical Plane application.

## Core Test Scripts

### `test_alignment.py`
Tests the alignment between visual rendering and collision detection boundaries. Useful for verifying that objects collide exactly where they appear to touch visually.

### `test_direct_collision.py`
Direct test of the player collision physics function to verify momentum conservation during player-to-player collisions.

### `test_momentum_alignment.py`
Tests momentum indicator consistency between red and purple dots to ensure both players have identical visual momentum feedback.

### `test_multiplayer.py`
Quick validation script that tests all imports and basic multiplayer functionality including GameEngine and Purple Dot creation.

### `test_player_physics.py`
Comprehensive test of Newtonian mechanics between red and purple dots, including collision physics and momentum conservation.

### `test_player_max_speeds.py`
Verifies that both players have identical maximum speeds and physics behavior to ensure fair gameplay.

### `test_player_starting_positions.py`
Tests that players start in their opponent's goal circles (red player in purple goal, purple player in red goal) for strategic gameplay.

### `test_rendering_functions.py`
Verifies that all rendering functions are working correctly and tests the rendering system components.

### `test_split_screen_multiplayer.py`
Tests the split-screen functionality and ensures both players can be rendered correctly in the dual-view system.

## Feature-Specific Tests

### `test_off_screen_indicator.py`
Tests the off-screen indicator logic that shows blue arrows pointing toward the blue square when it's outside a player's view.

### `test_static_circle_sizes.py`
Tests the static circle size calculations and positioning to ensure they fit within the grid boundaries.

### `test_gravitational_physics.py`
Tests the gravitational physics system that pulls the blue square toward the center of static circles when overlapping.

### `test_central_gravity.py`
Tests the invisible central gravitational point at the center of the grid that provides a gentle pull toward the center.

### `test_central_gravity_integration.py`
Tests the integration of the central gravity point with the full game engine to ensure proper functionality.

### `test_extended_gravitational_range.py`
Demonstrates the extended gravitational field range that now affects the blue square when adjacent to static circles.

### `test_scoring_system.py`
Tests the complete scoring system functionality including overlap detection, score tracking, blue square respawn, and timing requirements for scoring.

### `test_view_swap.py`
Verifies that the split-screen views are correctly arranged with purple player on the left and red player on the right.

### `test_hit_points_system.py`
Tests the complete hit points system including damage from collisions, boundary hits, HP depletion scoring, and 2-point static circle scoring.

### `test_hp_damage_pulse.py`
Tests the yellow pulse visual effect that appears when players take HP damage.

### `test_self_projectile_damage.py`
Tests that players cannot damage themselves with their own projectiles.

### `test_status_display_consistency.py`
Tests the consistency of status displays (HP, score) across different game modes.

## Running Tests

All test scripts can be run from the main project directory:

```bash
# From py-widget/ directory
python tests/test_name.py
```

Or navigate to the tests directory:

```bash
cd tests
python test_name.py
```

**Note:** All test scripts include the necessary path setup to import modules from the parent directory.

## Test Categories

- **Core Tests**: Essential functionality tests that should pass for basic game operation
- **Feature-Specific Tests**: Tests for specific game features like scoring, HP system, etc.

These tests ensure the game's physics, rendering, and gameplay mechanics work correctly across all features and game modes.
2. Add the following import path setup at the top of your script:

```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

3. Then import your modules normally:

```python
from game_engine import GameEngine
from config import *
# etc.
```

## Organization

All test and debug files have been moved from the root directory to maintain a clean project structure:
- Main application code remains in the root directory
- All testing and debugging utilities are contained in this `tests/` directory
- Import conflicts have been resolved (e.g., `test_alignment.py` renamed to `test_momentum_alignment.py` for momentum testing)

1. Place them in this `tests/` directory
2. Follow the naming convention: `test_*.py` for tests, `debug_*.py` for debug utilities
3. Add documentation to this README
4. Include usage instructions and brief description of what the test validates
