# Creating New Scripts - Quick Reference

## 📋 RULE: All test, debug, and demo scripts MUST go in tests/ folder

### ✅ Correct Script Placement

```bash
# Test scripts
tests/test_new_feature.py
tests/test_performance.py
tests/test_collision.py

# Debug scripts  
tests/debug_gamepad.py
tests/debug_physics.py
tests/debug_rendering.py

# Demo scripts
tests/demo_new_feature.py
tests/demo_scaling.py
```

### ❌ WRONG - Don't put these in main directory
```bash
# These are WRONG locations:
test_something.py          # Should be tests/test_something.py
debug_issue.py            # Should be tests/debug_issue.py
demo_feature.py           # Should be tests/demo_feature.py
```

## 🚀 Quick Start

### 1. Copy the template:
```bash
cp tests/template_test.py tests/test_your_feature.py
```

### 2. Edit your new script with the proper imports:
```python
#!/usr/bin/env python3
"""
Description of what this script tests/debugs/demos.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import normally
from game_engine import GameEngine
from split_screen import SplitScreenView
# ... other imports
```

### 3. Verify organization:
```bash
python tests/check_organization.py
```

## 📚 More Info

- See `tests/ORGANIZATION_GUIDELINES.md` for detailed rules
- Use `tests/template_test.py` as a starting point
- Run `tests/check_organization.py` to verify compliance

## 🔧 Automation

The `check_organization.py` script will automatically detect any misplaced files and provide move commands to fix them.
