"""
Object pooling system for projectiles to reduce garbage collection overhead.
Reuses projectile instances instead of creating/destroying them repeatedly.
"""

from typing import List, Optional
from objects import Projectile


class ProjectilePool:
    """Object pool for efficient projectile management."""
    
    def __init__(self, initial_size: int = 50, max_size: int = 100):
        """
        Initialize the projectile pool.
        
        Args:
            initial_size: Number of projectiles to pre-allocate
            max_size: Maximum number of pooled projectiles
        """
        self.max_size = max_size
        self.available_projectiles: List[Projectile] = []
        self.active_projectiles: List[Projectile] = []
        
        # Pre-allocate projectiles
        for _ in range(initial_size):
            projectile = Projectile(0, 0, 0, 0)
            projectile.is_active = False
            self.available_projectiles.append(projectile)
        
        # Statistics
        self.total_created = initial_size
        self.total_reused = 0
        self.peak_active = 0
    
    def acquire_projectile(self, x: float, y: float, velocity_x: float, velocity_y: float, 
                          owner_id: str = "red") -> Optional[Projectile]:
        """
        Get a projectile from the pool or create a new one.
        
        Args:
            x, y: Initial position
            velocity_x, velocity_y: Initial velocity
            owner_id: Owner of the projectile ("red" or "purple")
            
        Returns:
            Projectile instance or None if pool is at capacity
        """
        if len(self.active_projectiles) >= self.max_size:
            return None  # Pool at capacity
        
        # Try to reuse an existing projectile
        if self.available_projectiles:
            projectile = self.available_projectiles.pop()
            self.total_reused += 1
        else:
            # Create new projectile if pool is empty
            projectile = Projectile(0, 0, 0, 0)
            self.total_created += 1
        
        # Reset/initialize the projectile
        self._reset_projectile(projectile, x, y, velocity_x, velocity_y, owner_id)
        
        # Move to active list
        self.active_projectiles.append(projectile)
        
        # Update peak statistics
        if len(self.active_projectiles) > self.peak_active:
            self.peak_active = len(self.active_projectiles)
        
        return projectile
    
    def release_projectile(self, projectile: Projectile) -> bool:
        """
        Return a projectile to the pool.
        
        Args:
            projectile: Projectile to return to pool
            
        Returns:
            bool: True if successfully returned to pool
        """
        if projectile not in self.active_projectiles:
            return False
        
        # Remove from active list
        self.active_projectiles.remove(projectile)
        
        # Clean up the projectile
        self._cleanup_projectile(projectile)
        
        # Return to pool if we have space
        if len(self.available_projectiles) < self.max_size:
            self.available_projectiles.append(projectile)
            return True
        
        # Pool is full, let GC handle it
        return False
    
    def release_inactive_projectiles(self) -> int:
        """
        Automatically release all inactive projectiles back to the pool.
        
        Returns:
            int: Number of projectiles released
        """
        released = 0
        active_copy = self.active_projectiles.copy()
        
        for projectile in active_copy:
            if not projectile.is_active:
                if self.release_projectile(projectile):
                    released += 1
        
        return released
    
    def get_active_projectiles(self) -> List[Projectile]:
        """Get list of all active projectiles."""
        return [p for p in self.active_projectiles if p.is_active]
    
    def get_stats(self) -> dict:
        """Get pool statistics."""
        active_count = len(self.active_projectiles)
        available_count = len(self.available_projectiles)
        
        reuse_rate = 0.0
        if self.total_created > 0:
            reuse_rate = self.total_reused / (self.total_created + self.total_reused)
        
        return {
            'active_projectiles': active_count,
            'available_projectiles': available_count,
            'total_created': self.total_created,
            'total_reused': self.total_reused,
            'peak_active': self.peak_active,
            'reuse_rate': reuse_rate,
            'pool_utilization': active_count / self.max_size if self.max_size > 0 else 0
        }
    
    def clear_all(self):
        """Clear all projectiles from the pool."""
        for projectile in self.active_projectiles:
            self._cleanup_projectile(projectile)
        
        self.active_projectiles.clear()
        
        # Reset available projectiles
        for projectile in self.available_projectiles:
            self._cleanup_projectile(projectile)
    
    def _reset_projectile(self, projectile: Projectile, x: float, y: float, 
                         velocity_x: float, velocity_y: float, owner_id: str):
        """Reset a projectile to initial state."""
        # Position
        projectile.x = float(x)
        projectile.y = float(y)
        
        # Velocity
        projectile.velocity_x = float(velocity_x)
        projectile.velocity_y = float(velocity_y)
        
        # State
        projectile.is_active = True
        projectile.owner_id = owner_id
        projectile.has_made_contact = False
        projectile.bounce_count = 0
        projectile.just_launched = True
        
        # Reset physics properties to defaults
        from config import PROJECTILE_MASS, PROJECTILE_RADIUS
        projectile.mass = PROJECTILE_MASS
        projectile.radius = PROJECTILE_RADIUS
        projectile.damage = 1  # Default damage
    
    def _cleanup_projectile(self, projectile: Projectile):
        """Clean up a projectile before returning to pool."""
        projectile.is_active = False
        projectile.has_made_contact = False
        projectile.bounce_count = 0
        projectile.just_launched = False
        
        # Reset position to origin
        projectile.x = 0.0
        projectile.y = 0.0
        projectile.velocity_x = 0.0
        projectile.velocity_y = 0.0


# Global projectile pool instance
_projectile_pool = None

def get_projectile_pool() -> ProjectilePool:
    """Get the global projectile pool instance."""
    global _projectile_pool
    if _projectile_pool is None:
        _projectile_pool = ProjectilePool()
    return _projectile_pool

def reset_projectile_pool():
    """Reset the global projectile pool."""
    global _projectile_pool
    if _projectile_pool is not None:
        _projectile_pool.clear_all()
    _projectile_pool = ProjectilePool()
