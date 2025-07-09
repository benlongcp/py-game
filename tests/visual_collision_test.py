#!/usr/bin/env python3
"""
Visual verification script for boundary collision fixes.
Creates a simple test that shows objects bouncing naturally off the elliptical boundary.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pygame
import math
from physics import PhysicsEngine
from config import *

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Boundary Collision Test")
clock = pygame.time.Clock()


class TestDot:
    def __init__(self, x, y, vx, vy):
        self.x = float(x)
        self.y = float(y)
        self.velocity_x = float(vx)
        self.velocity_y = float(vy)
        self.radius = DOT_RADIUS
        self.trail = []  # Store position history for trail

    def update(self):
        # Store current position for trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > 30:  # Keep last 30 positions
            self.trail.pop(0)

        # Update position
        new_x = self.x + self.velocity_x
        new_y = self.y + self.velocity_y

        # Check boundary
        is_outside, corrected_x, corrected_y, normal_x, normal_y = (
            PhysicsEngine.check_elliptical_boundary(
                new_x, new_y, self.radius, GRID_RADIUS_X, GRID_RADIUS_Y
            )
        )

        if is_outside:
            # Apply correction and bounce
            self.x = corrected_x
            self.y = corrected_y

            # Bounce calculation
            dot_product = self.velocity_x * normal_x + self.velocity_y * normal_y
            self.velocity_x -= 2 * dot_product * normal_x * BOUNCE_FACTOR
            self.velocity_y -= 2 * dot_product * normal_y * BOUNCE_FACTOR
        else:
            self.x = new_x
            self.y = new_y

    def draw(self, screen, camera_x, camera_y):
        # Convert world coordinates to screen coordinates
        screen_x = self.x - camera_x + 400
        screen_y = self.y - camera_y + 300

        # Draw trail
        for i, (trail_x, trail_y) in enumerate(self.trail):
            trail_screen_x = trail_x - camera_x + 400
            trail_screen_y = trail_y - camera_y + 300
            alpha = i / len(self.trail)
            color = (int(255 * alpha), int(100 * alpha), int(100 * alpha))
            if 0 <= trail_screen_x < 800 and 0 <= trail_screen_y < 600:
                pygame.draw.circle(
                    screen, color, (int(trail_screen_x), int(trail_screen_y)), 2
                )

        # Draw dot
        if 0 <= screen_x < 800 and 0 <= screen_y < 600:
            pygame.draw.circle(
                screen, (255, 100, 100), (int(screen_x), int(screen_y)), self.radius
            )


def main():
    # Create test dots with different starting positions and velocities
    dots = [
        TestDot(700, 300, 12, 8),  # Diagonal movement
        TestDot(-600, 200, 10, -5),  # Coming from left
        TestDot(400, -400, -8, 12),  # Coming from bottom
        TestDot(-200, -300, 15, 15),  # Diagonal from bottom-left
    ]

    camera_x, camera_y = 0, 0
    running = True

    print("Boundary Collision Visual Test")
    print("You should see dots bouncing naturally off the elliptical boundary")
    print("without any sudden teleportation jumps.")
    print("Press ESC to exit.")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Update dots
        for dot in dots:
            dot.update()

        # Simple camera following the first dot
        camera_x = dots[0].x
        camera_y = dots[0].y

        # Clear screen
        screen.fill((20, 20, 20))

        # Draw elliptical boundary
        boundary_screen_x = -camera_x + 400
        boundary_screen_y = -camera_y + 300

        # Draw ellipse outline (approximate with polygon)
        ellipse_points = []
        for i in range(64):
            angle = 2 * math.pi * i / 64
            x = GRID_RADIUS_X * math.cos(angle)
            y = GRID_RADIUS_Y * math.sin(angle)
            screen_x = x - camera_x + 400
            screen_y = y - camera_y + 300
            ellipse_points.append((screen_x, screen_y))

        if len(ellipse_points) > 2:
            pygame.draw.polygon(screen, (100, 100, 100), ellipse_points, 2)

        # Draw dots
        for dot in dots:
            dot.draw(screen, camera_x, camera_y)

        # Draw instructions
        font = pygame.font.Font(None, 36)
        text = font.render(
            "Boundary Collision Test - ESC to exit", True, (255, 255, 255)
        )
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
