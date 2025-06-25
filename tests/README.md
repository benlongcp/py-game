# Tests and Debug Scripts

This directory contains all test utilities and debug scripts for the Topographical Plane application.

## Test Scripts

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

### `test_rendering_functions.py`
Verifies that all rendering functions are working correctly and tests the rendering system components.

### `test_split_screen_multiplayer.py`
Tests the split-screen functionality and ensures both players can be rendered correctly in the dual-view system.

### `test_off_screen_indicator.py`
Tests the off-screen indicator logic that shows blue arrows pointing toward the blue square when it's outside a player's view.

### `test_static_circle_sizes.py`
Tests the static circle size calculations and positioning to ensure they fit within the grid boundaries.

### `test_gravitational_physics.py`
Tests the gravitational physics system that pulls the blue square toward the center of static circles when overlapping.

### `test_extended_gravitational_range.py`
Demonstrates the extended gravitational field range that now affects the blue square when adjacent to static circles.

### `test_gravitational_field_boundaries.py`
Verifies that the gravitational field extends exactly one radius distance beyond the static circle boundaries.

## Demo Scripts

### `demo_off_screen_indicator.py`
Interactive demo showcasing the off-screen indicator feature. Move players around to see blue arrows pointing toward the off-screen blue square.

### `demo_gravitational_physics.py`
Interactive demo showcasing the gravitational dots feature. Shoot the blue square toward static circles to see gravitational pull effects.

## Debug Scripts

### `debug_collision.py`
Debug utility for analyzing collision detection issues.

### `debug_coordinates.py`
Analyzes coordinate system calculations to ensure consistency between world coordinates, screen coordinates, and physics calculations.

### `debug_moving_scenario.py`
Simulates coordinate transformations when the camera moves to debug potential offset issues between visual and collision boundaries.

## Running Tests

All test scripts have been updated with proper import paths. To run any test from the main project directory:

```bash
# From py-widget/ directory
python tests/test_name.py

```

Or navigate to the tests directory:

```bash
cd tests
python test_name.py
```

**Note:** All test scripts include the necessary path setup to import modules from the parent directory, so they can be run from either location.

## Adding New Tests

When adding new test or debug scripts:

1. Place them in this `tests/` directory
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
