"""
Master Volume Slider component for controlling game audio.
Displays at the bottom of the split-screen view opposite to the FPS counter.
"""

import pygame
from PyQt6.QtCore import QRect, QPoint, Qt
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush
from config import *


class MasterVolumeSlider:
    """A master volume slider UI component for controlling all sound effects."""
    
    def __init__(self, initial_volume=MASTER_VOLUME):
        """
        Initialize the master volume slider.
        
        Args:
            initial_volume: Initial volume level (0.0 to 1.0)
        """
        self.volume = max(0.0, min(1.0, initial_volume))
        self.is_dragging = False
        self.slider_rect = None
        self.handle_rect = None
        
        # Visual states
        self.hover = False
        self.last_interaction_time = 0
        self.fade_delay = 3000  # Hide after 3 seconds of no interaction
        
        # Initialize pygame mixer volume
        self._apply_volume()
        
    def get_slider_position(self, screen_width, screen_height):
        """Calculate the position of the slider on screen (bottom right, opposite FPS counter)."""
        # Position on the right side, similar to how FPS counter is positioned on left
        slider_x = screen_width - VOLUME_SLIDER_WIDTH - 10  # 10px margin from right edge
        slider_y = screen_height - VOLUME_SLIDER_HEIGHT - 8  # 8px margin from bottom edge, same as FPS
        return slider_x, slider_y
    
    def get_handle_position(self, slider_x):
        """Calculate the position of the slider handle based on volume."""
        handle_x = slider_x + int(self.volume * (VOLUME_SLIDER_WIDTH - 10)) + 2
        return handle_x
    
    def update_rects(self, screen_width, screen_height):
        """Update slider and handle rectangles for collision detection."""
        slider_x, slider_y = self.get_slider_position(screen_width, screen_height)
        self.slider_rect = QRect(slider_x, slider_y, VOLUME_SLIDER_WIDTH, VOLUME_SLIDER_HEIGHT)
        
        handle_x = self.get_handle_position(slider_x)
        self.handle_rect = QRect(handle_x, slider_y + 2, 6, VOLUME_SLIDER_HEIGHT - 4)
    
    def handle_mouse_press(self, mouse_pos, screen_width, screen_height):
        """
        Handle mouse press event for the volume slider.
        
        Args:
            mouse_pos: QPoint of mouse position
            screen_width, screen_height: Screen dimensions
            
        Returns:
            bool: True if the event was handled by the slider
        """
        if not pygame.mixer.get_init():
            return False  # Audio not initialized
            
        self.update_rects(screen_width, screen_height)
        
        # Check if mouse is over slider area
        extended_rect = QRect(
            self.slider_rect.x() - 20, self.slider_rect.y() - 10,
            self.slider_rect.width() + 40, self.slider_rect.height() + 20
        )
        
        if self.slider_rect.contains(mouse_pos):
            self.is_dragging = True
            self._update_volume_from_mouse(mouse_pos.x())
            self.last_interaction_time = pygame.time.get_ticks() if pygame.get_init() else 0
            return True
                
        return False
    
    def handle_mouse_release(self):
        """Handle mouse release event."""
        if self.is_dragging:
            self.is_dragging = False
            return True
        return False
    
    def handle_mouse_move(self, mouse_pos, screen_width, screen_height):
        """
        Handle mouse move event for the volume slider.
        
        Args:
            mouse_pos: QPoint of mouse position
            screen_width, screen_height: Screen dimensions
            
        Returns:
            bool: True if the event was handled by the slider
        """
        if not pygame.mixer.get_init():
            return False
            
        self.update_rects(screen_width, screen_height)
        
        # Check if mouse is over slider area
        extended_rect = QRect(
            self.slider_rect.x() - 20, self.slider_rect.y() - 10,
            self.slider_rect.width() + 40, self.slider_rect.height() + 20
        )
        self.hover = extended_rect.contains(mouse_pos)
        
        if self.hover:
            self.last_interaction_time = pygame.time.get_ticks() if pygame.get_init() else 0
        
        if self.is_dragging:
            self._update_volume_from_mouse(mouse_pos.x())
            self.last_interaction_time = pygame.time.get_ticks() if pygame.get_init() else 0
            return True
                
        return False
    
    def _update_volume_from_mouse(self, mouse_x):
        """Update volume based on mouse x position."""
        if self.slider_rect:
            relative_x = mouse_x - self.slider_rect.x() - 5
            self.volume = max(0.0, min(1.0, relative_x / (VOLUME_SLIDER_WIDTH - 10)))
            self._apply_volume()
    
    def _apply_volume(self):
        """Apply the current volume to pygame mixer."""
        if pygame.mixer.get_init():
            pygame.mixer.music.set_volume(self.volume)
            # Set master volume for all sound channels
            for i in range(pygame.mixer.get_num_channels()):
                channel = pygame.mixer.Channel(i)
                if channel.get_busy():
                    # Note: Individual sounds need to be scaled when played
                    pass
    
    def should_show(self):
        """Determine if the slider should be visible - always show for consistent UI."""
        return True  # Always visible for consistent UI, like FPS counter
    
    def draw(self, painter, screen_width, screen_height):
        """
        Draw the volume slider using QPainter.
        
        Args:
            painter: QPainter instance
            screen_width, screen_height: Screen dimensions
        """
        if not pygame.mixer.get_init():
            return  # Don't draw if audio not initialized
            
        if not self.should_show():
            return
            
        self.update_rects(screen_width, screen_height)
        slider_x, slider_y = self.get_slider_position(screen_width, screen_height)
        
        # Use full alpha since it's always visible
        alpha = 255 if (self.hover or self.is_dragging) else 200
        
        # Draw volume icon
        icon_x = slider_x - VOLUME_ICON_SIZE - 5
        icon_y = slider_y + (VOLUME_SLIDER_HEIGHT - VOLUME_ICON_SIZE) // 2
        self._draw_volume_icon(painter, icon_x, icon_y, alpha)
        
        # Draw "Volume:" label to the left of the icon
        painter.setPen(QPen(QColor(255, 255, 255, int(alpha))))
        painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        label_text = "Volume:"
        font_metrics = painter.fontMetrics()
        label_width = font_metrics.horizontalAdvance(label_text)
        label_x = icon_x - label_width - 8  # 8px spacing between label and icon
        label_y = slider_y + VOLUME_SLIDER_HEIGHT - 2  # Align with slider baseline
        painter.drawText(label_x, label_y, label_text)
        
        # Draw slider background
        bg_color = QColor(*VOLUME_SLIDER_BACKGROUND_COLOR, int(alpha))
        painter.fillRect(QRect(slider_x, slider_y, VOLUME_SLIDER_WIDTH, VOLUME_SLIDER_HEIGHT), bg_color)
        
        # Draw border
        border_color = QColor(*VOLUME_SLIDER_BORDER_COLOR, int(alpha))
        painter.setPen(QPen(border_color, 1))
        painter.drawRect(QRect(slider_x, slider_y, VOLUME_SLIDER_WIDTH, VOLUME_SLIDER_HEIGHT))
        
        # Draw volume fill
        fill_width = int((VOLUME_SLIDER_WIDTH - 4) * self.volume)
        if fill_width > 0:
            fill_color = QColor(*VOLUME_SLIDER_FILL_COLOR, int(alpha))
            painter.fillRect(QRect(slider_x + 2, slider_y + 2, fill_width, VOLUME_SLIDER_HEIGHT - 4), fill_color)
        
        # Draw handle
        handle_x = slider_x + int(self.volume * (VOLUME_SLIDER_WIDTH - 10)) + 2
        handle_color = QColor(*VOLUME_SLIDER_HANDLE_COLOR, int(alpha))
        painter.fillRect(QRect(handle_x, slider_y + 2, 6, VOLUME_SLIDER_HEIGHT - 4), handle_color)
        
        # Draw volume percentage text
        if self.hover or self.is_dragging:
            painter.setPen(QPen(QColor(255, 255, 255, int(alpha))))
            painter.setFont(QFont("Arial", 10))
            volume_text = f"{int(self.volume * 100)}%"
            text_rect = QRect(slider_x, slider_y - 25, VOLUME_SLIDER_WIDTH, 20)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, volume_text)
    
    def _draw_volume_icon(self, painter, x, y, alpha):
        """Draw a simple volume icon using QPainter."""
        icon_color = QColor(200, 200, 200, int(alpha))
        painter.setPen(QPen(icon_color, 1))
        painter.setBrush(QBrush(icon_color))
        
        # Draw speaker base
        painter.fillRect(QRect(x + 2, y + 4, 4, 8), icon_color)
        
        # Draw speaker cone (simplified as triangle)
        painter.fillRect(QRect(x + 6, y + 6, 4, 4), icon_color)
        
        # Draw sound waves based on volume level
        if self.volume > 0.0:
            wave_color = QColor(150, 150, 150, int(alpha * 0.8))
            painter.setPen(QPen(wave_color, 1))
            painter.drawArc(QRect(x + 10, y + 4, 8, 8), 16 * -30, 16 * 60)  # Qt uses 16ths of degrees
        
        if self.volume > 0.5:
            painter.drawArc(QRect(x + 12, y + 2, 8, 12), 16 * -30, 16 * 60)
        
        if self.volume > 0.8:
            painter.drawArc(QRect(x + 14, y, 8, 16), 16 * -30, 16 * 60)
    
    def set_volume(self, volume):
        """
        Set the volume level.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        self._apply_volume()
        if pygame.get_init():
            self.last_interaction_time = pygame.time.get_ticks()
    
    def get_volume(self):
        """
        Get the current volume level.
        
        Returns:
            float: Current volume (0.0 to 1.0)
        """
        return self.volume
    
    def show_temporarily(self):
        """Show the slider temporarily (useful for keyboard volume controls)."""
        if pygame.get_init():
            self.last_interaction_time = pygame.time.get_ticks()


# Global volume slider instance
_master_volume_slider = None

def get_master_volume_slider():
    """Get the global master volume slider instance."""
    global _master_volume_slider
    if _master_volume_slider is None:
        _master_volume_slider = MasterVolumeSlider()
    return _master_volume_slider

def set_master_volume(volume):
    """Set the master volume globally."""
    slider = get_master_volume_slider()
    slider.set_volume(volume)

def get_master_volume():
    """Get the current master volume."""
    slider = get_master_volume_slider()
    return slider.get_volume()
