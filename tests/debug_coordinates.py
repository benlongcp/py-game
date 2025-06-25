#!/usr/bin/env python3

# Debug script to show the coordinate discrepancy


def debug_coordinates():
    # Simulate the values from the widget
    square_x, square_y = 300.0, 150.0  # World coordinates
    red_dot_x, red_dot_y = 200.0, 200.0  # Current red dot position
    window_center_x, window_center_y = 200, 200
    square_size = 50
    dot_radius = 5

    # Virtual coordinates (same as red dot initially)
    virtual_x = red_dot_x
    virtual_y = red_dot_y

    print("=== COORDINATE SYSTEM ANALYSIS ===")
    print(f"World square position: ({square_x}, {square_y})")
    print(f"Virtual position (camera): ({virtual_x}, {virtual_y})")
    print(f"Red dot position: ({red_dot_x}, {red_dot_y})")
    print()

    # DRAWING COORDINATES (what we see on screen)
    screen_square_x = square_x - (virtual_x - window_center_x)
    screen_square_y = square_y - (virtual_y - window_center_y)
    print("=== DRAWING SYSTEM ===")
    print(f"Screen square center: ({screen_square_x}, {screen_square_y})")

    half_size = square_size / 2
    draw_left = screen_square_x - half_size
    draw_top = screen_square_y - half_size
    print(
        f"Drawing boundaries: left={draw_left}, top={draw_top}, width={square_size}, height={square_size}"
    )
    print()

    # COLLISION DETECTION COORDINATES (world space)
    print("=== COLLISION DETECTION SYSTEM ===")
    print(f"World square center: ({square_x}, {square_y})")

    half_square = square_size / 2
    collision_square_left = square_x - half_square
    collision_square_top = square_y - half_square
    print(
        f"Collision square boundaries: left={collision_square_left}, top={collision_square_top}"
    )

    # Dot collision boundaries
    collision_left = collision_square_left - dot_radius
    collision_top = collision_square_top - dot_radius
    print(f"Dot collision boundaries: left={collision_left}, top={collision_top}")
    print()

    # Show the discrepancy
    print("=== DISCREPANCY ANALYSIS ===")
    x_offset = draw_left - collision_square_left
    y_offset = draw_top - collision_square_top
    print(f"Drawing vs Collision offset: x={x_offset}, y={y_offset}")

    if x_offset != 0 or y_offset != 0:
        print("❌ MISALIGNMENT DETECTED!")
        print(
            "The drawing uses screen coordinates, but collision uses world coordinates"
        )
        print(
            "This creates a visual offset between the drawn square and collision boundaries"
        )
    else:
        print("✅ Coordinates are aligned")


if __name__ == "__main__":
    debug_coordinates()
