# Tests and Debug Scripts

This directory contains test utilities and debug scripts for the Topographical Plane application.

## Files

### `test_alignment.py`
Tests the alignment between visual rendering and collision detection boundaries. Useful for verifying that objects collide exactly where they appear to touch visually.

**Usage:**
```bash
python tests/test_alignment.py
```

### `debug_coordinates.py`
Analyzes coordinate system calculations to ensure consistency between world coordinates, screen coordinates, and physics calculations.

**Usage:**
```bash
python tests/debug_coordinates.py
```

### `debug_moving_scenario.py`
Simulates coordinate transformations when the camera moves to debug potential offset issues between visual and collision boundaries.

**Usage:**
```bash
python tests/debug_moving_scenario.py
```

## Running Tests

To run any test from the main project directory:

```bash
# From py-widget/ directory
python tests/test_name.py
```

Or navigate to the tests directory:

```bash
cd tests
python test_name.py
```

## Adding New Tests

When adding new test or debug scripts:

1. Place them in this `tests/` directory
2. Follow the naming convention: `test_*.py` for tests, `debug_*.py` for debug utilities
3. Add documentation to this README
4. Include usage instructions and brief description of what the test validates
