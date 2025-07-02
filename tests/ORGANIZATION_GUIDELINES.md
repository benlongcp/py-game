# Tests Folder Organization Guidelines

## ⚠️ CRITICAL RULE ⚠️
**ALL test, debug, and demo scripts MUST be placed in the `tests/` folder!**
**NEVER create test/debug/demo files in the main project directory!**

## Purpose
This folder contains all test scripts, debug tools, demos, and experimental code for the Topographical Plane game project.

## File Organization

### Test Scripts (`test_*.py`)
- **Purpose**: Test specific features or functionality
- **Naming**: `test_<feature_name>.py`
- **Examples**: 
  - `test_dynamic_scaling.py` - Test window scaling
  - `test_performance_comparison.py` - Performance testing
  - `test_multiplayer.py` - Multiplayer functionality

### Debug Scripts (`debug_*.py`)
- **Purpose**: Debug specific issues or behaviors
- **Naming**: `debug_<issue_or_component>.py`
- **Examples**:
  - `debug_gamepad.py` - Gamepad input debugging
  - `debug_velocity.py` - Physics velocity debugging
  - `debug_raw_hardware.py` - Low-level hardware debugging

### Demo Scripts (`demo_*.py`)
- **Purpose**: Demonstrate features or showcase functionality
- **Naming**: `demo_<feature_name>.py`
- **Examples**:
  - `demo_dynamic_scaling.py` - Show off window scaling

### Documentation (`.md` files)
- Implementation details and technical documentation
- Performance analysis and optimization notes
- Feature specifications and requirements

## File Location Rules

### ✅ Files that SHOULD be in tests/
- All `test_*.py` files
- All `debug_*.py` files  
- All `demo_*.py` files
- Experimental or prototype scripts
- Performance testing tools
- Feature validation scripts
- Documentation related to testing/debugging

### ❌ Files that should NOT be in tests/
- `main.py` - Main application entry point
- Core game modules (`game_engine.py`, `physics.py`, etc.)
- Production configuration files
- README.md for the main project

## Import Guidelines

### For test scripts in tests/ folder:
```python
# Add parent directory to path for imports
import sys
sys.path.append('..')

# Then import normally
from game_engine import GameEngine
from split_screen import SplitScreenView
```

### Alternative approach:
```python
# Use relative imports from tests folder
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import GameEngine
```

## Running Tests

### From main project directory:
```bash
python tests/test_dynamic_scaling.py
python tests/demo_dynamic_scaling.py
python tests/debug_gamepad.py
```

### From tests directory:
```bash
cd tests
python test_dynamic_scaling.py
python demo_dynamic_scaling.py
python debug_gamepad.py
```

## Organizational Tools

### Quick Compliance Checking
- `python check_org.py` - Quick organization check from main directory
- `python tests/check_organization.py` - Full organization analysis

### Script Creation Helpers
- `tests/template_test.py` - Template for new test scripts
- `tests/new_script_template.py` - Template with organization reminder
- `new_test.bat script_name` - Windows batch file to create scripts in correct location

### Version Control Protection
- `.gitignore` - Prevents committing misplaced test files

## Best Practices

### 1. Descriptive Names
- Use clear, descriptive names that explain what the script does
- Include the type prefix: `test_`, `debug_`, `demo_`

### 2. Documentation
- Include docstrings explaining the purpose
- Add comments for complex test scenarios
- Document expected results or behaviors

### 3. Self-Contained
- Each script should be runnable independently
- Include necessary imports and setup
- Provide clear output or feedback

### 4. Cleanup
- Remove temporary files or test data when done
- Reset system state if modified during testing
- Provide cleanup instructions if manual cleanup needed

## Current Test Categories

### Performance Tests
- `test_performance_comparison.py` - Compare different approaches
- `test_maximized_performance.py` - Test at maximum window size
- `test_quick_performance.py` - Fast performance validation

### Feature Tests  
- `test_dynamic_scaling.py` - Window scaling functionality
- `test_multiplayer.py` - Multi-player features
- `test_gamepad_detection.py` - Gamepad support

### Physics Tests
- `test_gravitational_physics.py` - Physics engine validation
- `test_collision.py` - Collision detection
- `test_momentum_alignment.py` - Physics calculations

### Rendering Tests
- `test_rendering_functions.py` - Rendering system
- `test_status_display_consistency.py` - UI rendering

### Debug Tools
- `debug_gamepad.py` - Gamepad input debugging
- `debug_velocity.py` - Movement debugging
- `debug_player1.py` - Player-specific debugging

## Maintenance

### Regular Cleanup
- Remove obsolete test scripts
- Update documentation as features change
- Consolidate similar tests when possible

### Organization Review
- Periodically review file organization
- Move misplaced files to correct locations
- Update import paths as needed

## Future Additions

When adding new test/debug/demo scripts:

1. **Check naming convention** - Use appropriate prefix
2. **Place in tests/ folder** - Keep main directory clean
3. **Update this README** - Add to relevant category
4. **Test imports** - Ensure script runs from both locations
5. **Document purpose** - Add clear description and usage

This organization keeps the main project directory clean while providing a comprehensive testing and debugging toolkit in the tests folder.
