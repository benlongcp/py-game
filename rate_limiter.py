"""
Rate limiter for projectile firing to prevent spam.
Tracks firing timestamps and implements cooldown mechanics.
"""

import time
from config import *


class ProjectileRateLimiter:
    """Manages rate limiting for projectile firing."""

    def __init__(self):
        """Initialize the rate limiter."""
        self.firing_timestamps = []  # List of recent firing times
        self.cooldown_start_time = None  # When cooldown period started
        self.is_in_cooldown = False
        self.max_rate = PROJECTILE_RATE_LIMIT

    def can_fire(self):
        """Check if the player can fire a projectile right now."""
        current_time = time.time()

        # If in cooldown, check if cooldown period has expired
        if self.is_in_cooldown:
            if current_time - self.cooldown_start_time >= PROJECTILE_COOLDOWN_DURATION:
                # Cooldown expired, reset state
                self.is_in_cooldown = False
                self.cooldown_start_time = None
                self.firing_timestamps.clear()  # Clear old timestamps
                return True
            else:
                # Still in cooldown
                return False

        # Clean up old timestamps outside the rate window
        self._cleanup_old_timestamps(current_time)

        # Check if firing would exceed the rate limit
        if len(self.firing_timestamps) >= self.max_rate:
            # Rate limit exceeded, enter cooldown
            self.is_in_cooldown = True
            self.cooldown_start_time = current_time
            return False

        return True

    def record_shot(self):
        """Record that a projectile was fired."""
        if not self.is_in_cooldown:
            self.firing_timestamps.append(time.time())

    def _cleanup_old_timestamps(self, current_time):
        """Remove timestamps older than the rate window."""
        cutoff_time = current_time - PROJECTILE_RATE_WINDOW
        self.firing_timestamps = [
            timestamp for timestamp in self.firing_timestamps if timestamp > cutoff_time
        ]

    def get_progress(self):
        """
        Get the progress for UI display.

        Returns:
            dict: Contains 'type', 'progress', and 'time_remaining'
                 - type: 'normal', 'warning', 'cooldown'
                 - progress: 0.0 to 1.0 for pie chart fill
                 - time_remaining: seconds until next state change
        """
        current_time = time.time()

        # Check if cooldown has expired (same logic as can_fire)
        if self.is_in_cooldown:
            if current_time - self.cooldown_start_time >= PROJECTILE_COOLDOWN_DURATION:
                # Cooldown expired, reset state
                self.is_in_cooldown = False
                self.cooldown_start_time = None
                self.firing_timestamps.clear()  # Clear old timestamps
                # Continue to normal processing below
            else:
                # Still in cooldown - show countdown
                elapsed = current_time - self.cooldown_start_time
                progress = elapsed / PROJECTILE_COOLDOWN_DURATION
                time_remaining = max(0, PROJECTILE_COOLDOWN_DURATION - elapsed)

                return {
                    "type": "cooldown",
                    "progress": min(1.0, progress),
                    "time_remaining": time_remaining,
                }

        # Not in cooldown - show usage relative to limit
        self._cleanup_old_timestamps(current_time)
        usage_ratio = len(self.firing_timestamps) / PROJECTILE_RATE_LIMIT

        # Determine color based on usage
        if usage_ratio >= 0.8:  # 80% or more = warning
            limiter_type = "warning"
        else:
            limiter_type = "normal"

        # Calculate time until oldest shot expires (for dynamic updates)
        time_remaining = 0
        if self.firing_timestamps:
            oldest_shot = min(self.firing_timestamps)
            time_remaining = max(
                0, PROJECTILE_RATE_WINDOW - (current_time - oldest_shot)
            )

        return {
            "type": limiter_type,
            "progress": usage_ratio,
            "time_remaining": time_remaining,
        }

    def reset(self):
        """Reset the rate limiter state."""
        self.firing_timestamps.clear()
        self.is_in_cooldown = False
        self.cooldown_start_time = None
