# Projectile Bounce Configuration Update

## What was added:

### config.py
Added a new configuration option in the projectile settings section:
```python
PROJECTILE_MAX_BOUNCES = 6  # Maximum number of bounces before projectile expires
```

### objects.py
Updated the hardcoded bounce limit to use the configuration:
```python
# Old code:
if self.bounce_count >= 6:

# New code:
if self.bounce_count >= PROJECTILE_MAX_BOUNCES:
```

## How to use:

You can now easily adjust the number of times projectiles can bounce off boundaries before they expire by changing the `PROJECTILE_MAX_BOUNCES` value in `config.py`.

**Examples:**
- `PROJECTILE_MAX_BOUNCES = 3` - Projectiles expire after 3 bounces (shorter range)
- `PROJECTILE_MAX_BOUNCES = 10` - Projectiles expire after 10 bounces (longer range) 
- `PROJECTILE_MAX_BOUNCES = 1` - Projectiles expire after first bounce (very short range)

## Benefits:

1. **Easy gameplay tuning** - Adjust projectile range without touching code
2. **Consistent configuration** - All game parameters in one place
3. **Better maintainability** - No more hardcoded magic numbers

## Status:
✅ **Implementation complete and tested**  
✅ All systems working correctly with the new configurable bounce count
