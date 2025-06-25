#!/usr/bin/env python3


def debug_moving_coordinates():
    # Simulate when red dot has moved
    square_x, square_y = 300.0, 150.0  # World coordinates (fixed)
    window_center_x, window_center_y = 200, 200
    square_size = 50
    dot_radius = 5

    # Simulate red dot moved to different position
    red_dot_x, red_dot_y = 250.0, 180.0  # Red dot screen position
    virtual_x, virtual_y = 250.0, 180.0  # Virtual position matches red dot

    print("=== MOVING DOT SCENARIO ===")
    print(f"Red dot screen position: ({red_dot_x}, {red_dot_y})")
    print(f"Virtual position: ({virtual_x}, {virtual_y})")
    print(f"Square world position: ({square_x}, {square_y})")
    print()

    # DRAWING COORDINATES (what we see on screen)
    screen_square_x = square_x - (virtual_x - window_center_x)
    screen_square_y = square_y - (virtual_y - window_center_y)
    print("=== DRAWING (what you see) ===")
    print(f"Square drawn at screen position: ({screen_square_x}, {screen_square_y})")

    half_size = square_size / 2
    draw_left = screen_square_x - half_size
    draw_top = screen_square_y - half_size
    print(f"Square visual boundaries: left={draw_left}, top={draw_top}")
    print()

    # COLLISION DETECTION (uses world coordinates)
    print("=== COLLISION DETECTION (world space) ===")
    print(f"Dot virtual position: ({virtual_x}, {virtual_y})")
    print(f"Square world position: ({square_x}, {square_y})")

    half_square = square_size / 2
    collision_square_left = square_x - half_square
    collision_square_top = square_y - half_square
    print(
        f"Square collision boundaries: left={collision_square_left}, top={collision_square_top}"
    )

    collision_left = collision_square_left - dot_radius
    collision_top = collision_square_top - dot_radius
    print(f"Dot collision zone: left={collision_left}, top={collision_top}")
    print()

    # Show the problem
    print("=== THE PROBLEM ===")
    visual_vs_collision_x = draw_left - collision_square_left
    visual_vs_collision_y = draw_top - collision_square_top
    print(
        f"Visual square vs Collision square offset: x={visual_vs_collision_x}, y={visual_vs_collision_y}"
    )

    if visual_vs_collision_x != 0 or visual_vs_collision_y != 0:
        print("❌ OFFSET DETECTED!")
        print(
            "The square is drawn with camera transform, but collision uses world coordinates"
        )
        print("This creates the visual/collision mismatch you're seeing")

        print("\n=== SOLUTION ===")
        print("Both drawing AND collision should use the same coordinate system")
        print("Either both use world coordinates, or both use screen coordinates")


if __name__ == "__main__":
    debug_moving_coordinates()
