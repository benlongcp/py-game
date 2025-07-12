"""
Advanced performance management system with Level-of-Detail (LOD) and optimization strategies.
Provides dynamic performance scaling based on real-time metrics.
"""

import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class PerformanceMetrics:
    """Container for performance metrics."""
    fps: float = 60.0
    frame_time_ms: float = 16.67
    collision_checks: int = 0
    active_projectiles: int = 0
    render_objects: int = 0
    grid_points: int = 0
    memory_usage_mb: float = 0.0


@dataclass
class LODSettings:
    """Level-of-Detail settings for different performance levels."""
    projectile_limit: int = 50
    grid_density_multiplier: float = 1.0
    collision_cell_size: int = 100
    gravity_calculation_skip: int = 1  # Skip every N frames
    render_distance_multiplier: float = 1.0
    particle_effects: bool = True
    high_quality_rendering: bool = True


class PerformanceManager:
    """Advanced performance management with LOD and adaptive optimization."""
    
    def __init__(self):
        """Initialize the performance manager."""
        self.metrics = PerformanceMetrics()
        self.frame_times: List[float] = []
        self.max_frame_history = 30
        
        # Performance levels
        self.lod_levels = {
            'ultra': LODSettings(
                projectile_limit=75,
                grid_density_multiplier=1.0,
                collision_cell_size=80,
                gravity_calculation_skip=1,
                render_distance_multiplier=1.0,
                particle_effects=True,
                high_quality_rendering=True
            ),
            'high': LODSettings(
                projectile_limit=50,
                grid_density_multiplier=0.8,
                collision_cell_size=100,
                gravity_calculation_skip=1,
                render_distance_multiplier=1.0,
                particle_effects=True,
                high_quality_rendering=True
            ),
            'medium': LODSettings(
                projectile_limit=35,
                grid_density_multiplier=0.6,
                collision_cell_size=120,
                gravity_calculation_skip=2,
                render_distance_multiplier=0.8,
                particle_effects=True,
                high_quality_rendering=False
            ),
            'low': LODSettings(
                projectile_limit=25,
                grid_density_multiplier=0.4,
                collision_cell_size=150,
                gravity_calculation_skip=3,
                render_distance_multiplier=0.6,
                particle_effects=False,
                high_quality_rendering=False
            ),
            'potato': LODSettings(
                projectile_limit=15,
                grid_density_multiplier=0.25,
                collision_cell_size=200,
                gravity_calculation_skip=4,
                render_distance_multiplier=0.4,
                particle_effects=False,
                high_quality_rendering=False
            )
        }
        
        self.current_lod = 'high'
        self.target_fps = 45.0
        self.lod_switch_cooldown = 60  # Frames before switching LOD again
        self.lod_cooldown_timer = 0
        
        # Dirty flags for cache invalidation
        self.dirty_flags = {
            'grid_cache': False,
            'collision_cache': False,
            'render_cache': False,
            'visibility_cache': False
        }
        
        # Performance tracking
        self.performance_history: List[float] = []
        self.last_optimization_time = time.time()
        
    def update_frame_time(self, frame_time: float):
        """Update frame timing metrics."""
        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.max_frame_history:
            self.frame_times.pop(0)
        
        # Calculate rolling average
        if self.frame_times:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            self.metrics.frame_time_ms = avg_frame_time * 1000
            self.metrics.fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 60.0
        
        # Update performance history
        self.performance_history.append(self.metrics.fps)
        if len(self.performance_history) > 120:  # Keep 2 seconds at 60fps
            self.performance_history.pop(0)
        
        # Update LOD cooldown
        if self.lod_cooldown_timer > 0:
            self.lod_cooldown_timer -= 1
    
    def should_adjust_lod(self) -> bool:
        """Determine if LOD should be adjusted based on performance."""
        if self.lod_cooldown_timer > 0:
            return False
        
        if len(self.performance_history) < 10:
            return False
        
        # Calculate recent performance trend
        recent_fps = sum(self.performance_history[-10:]) / 10
        
        # Check if we need to lower LOD
        if recent_fps < self.target_fps * 0.8:  # 20% below target
            return self._can_lower_lod()
        
        # Check if we can raise LOD
        elif recent_fps > self.target_fps * 1.1:  # 10% above target
            return self._can_raise_lod()
        
        return False
    
    def adjust_lod(self):
        """Automatically adjust LOD based on performance."""
        if not self.should_adjust_lod():
            return
        
        recent_fps = sum(self.performance_history[-10:]) / 10
        lod_order = ['potato', 'low', 'medium', 'high', 'ultra']
        current_index = lod_order.index(self.current_lod)
        
        if recent_fps < self.target_fps * 0.8 and current_index > 0:
            # Lower LOD
            new_lod = lod_order[current_index - 1]
            self._switch_lod(new_lod)
            
        elif recent_fps > self.target_fps * 1.1 and current_index < len(lod_order) - 1:
            # Raise LOD
            new_lod = lod_order[current_index + 1]
            self._switch_lod(new_lod)
    
    def _switch_lod(self, new_lod: str):
        """Switch to a new LOD level."""
        if new_lod == self.current_lod:
            return
        
        old_lod = self.current_lod
        self.current_lod = new_lod
        self.lod_cooldown_timer = self.lod_switch_cooldown
        
        # Invalidate relevant caches
        self.invalidate_cache('grid_cache')
        self.invalidate_cache('collision_cache')
        self.invalidate_cache('render_cache')
        
        print(f"Performance: LOD switched from {old_lod} to {new_lod} (FPS: {self.metrics.fps:.1f})")
    
    def _can_lower_lod(self) -> bool:
        """Check if LOD can be lowered."""
        lod_order = ['potato', 'low', 'medium', 'high', 'ultra']
        current_index = lod_order.index(self.current_lod)
        return current_index > 0
    
    def _can_raise_lod(self) -> bool:
        """Check if LOD can be raised."""
        lod_order = ['potato', 'low', 'medium', 'high', 'ultra']
        current_index = lod_order.index(self.current_lod)
        return current_index < len(lod_order) - 1
    
    def get_current_settings(self) -> LODSettings:
        """Get current LOD settings."""
        return self.lod_levels[self.current_lod]
    
    def invalidate_cache(self, cache_name: str):
        """Mark a cache as dirty for regeneration."""
        if cache_name in self.dirty_flags:
            self.dirty_flags[cache_name] = True
    
    def is_cache_dirty(self, cache_name: str) -> bool:
        """Check if a cache needs regeneration."""
        return self.dirty_flags.get(cache_name, False)
    
    def clear_cache_flag(self, cache_name: str):
        """Clear a cache dirty flag."""
        if cache_name in self.dirty_flags:
            self.dirty_flags[cache_name] = False
    
    def should_skip_expensive_operation(self, operation_type: str, frame_count: int) -> bool:
        """Determine if an expensive operation should be skipped this frame."""
        settings = self.get_current_settings()
        
        if operation_type == 'gravity_calculation':
            return frame_count % settings.gravity_calculation_skip != 0
        
        elif operation_type == 'detailed_collision':
            # Skip detailed collision for distant objects in lower LOD
            return self.current_lod in ['low', 'potato'] and frame_count % 2 == 0
        
        elif operation_type == 'particle_effects':
            return not settings.particle_effects
        
        elif operation_type == 'high_quality_render':
            return not settings.high_quality_rendering
        
        return False
    
    def get_render_distance_multiplier(self) -> float:
        """Get the current render distance multiplier for LOD."""
        return self.get_current_settings().render_distance_multiplier
    
    def get_grid_density_multiplier(self) -> float:
        """Get the current grid density multiplier for LOD."""
        return self.get_current_settings().grid_density_multiplier
    
    def get_performance_report(self) -> Dict:
        """Generate a comprehensive performance report."""
        settings = self.get_current_settings()
        
        # Calculate performance trend
        trend = "stable"
        if len(self.performance_history) >= 20:
            recent_avg = sum(self.performance_history[-10:]) / 10
            older_avg = sum(self.performance_history[-20:-10]) / 10
            
            if recent_avg > older_avg * 1.05:
                trend = "improving"
            elif recent_avg < older_avg * 0.95:
                trend = "declining"
        
        return {
            'current_fps': self.metrics.fps,
            'target_fps': self.target_fps,
            'frame_time_ms': self.metrics.frame_time_ms,
            'lod_level': self.current_lod,
            'projectile_limit': settings.projectile_limit,
            'collision_cell_size': settings.collision_cell_size,
            'grid_density': settings.grid_density_multiplier,
            'performance_trend': trend,
            'active_projectiles': self.metrics.active_projectiles,
            'collision_checks': self.metrics.collision_checks,
            'dirty_caches': [k for k, v in self.dirty_flags.items() if v],
            'memory_usage_mb': self.metrics.memory_usage_mb
        }
    
    def force_lod_level(self, lod_level: str):
        """Force a specific LOD level (for testing or user preference)."""
        if lod_level in self.lod_levels:
            self._switch_lod(lod_level)
        else:
            raise ValueError(f"Invalid LOD level: {lod_level}")
    
    def reset_performance_tracking(self):
        """Reset all performance tracking data."""
        self.frame_times.clear()
        self.performance_history.clear()
        self.metrics = PerformanceMetrics()
        self.lod_cooldown_timer = 0
        
        # Clear all dirty flags
        for key in self.dirty_flags:
            self.dirty_flags[key] = False


# Global performance manager instance
_performance_manager = None

def get_performance_manager() -> PerformanceManager:
    """Get the global performance manager instance."""
    global _performance_manager
    if _performance_manager is None:
        _performance_manager = PerformanceManager()
    return _performance_manager