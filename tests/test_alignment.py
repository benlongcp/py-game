#!/usr/bin/env python3
"""
Test script to verify alignment between drawing and collision detection
"""


def test_alignment():
    # Simulate the square properties
    square_size = 50  # 10 * 5 (dot_radius)
    square_x = 300.0
    square_y = 150.0

    # Drawing calculation
    half_size = square_size / 2
    window_center_x, window_center_y = 200, 200
    virtual_x, virtual_y = 200, 200  # Red dot at center

    screen_square_x = square_x - (virtual_x - window_center_x)
    screen_square_y = square_y - (virtual_y - window_center_y)

    exact_left = screen_square_x - half_size
    exact_top = screen_square_y - half_size
    exact_width = square_size
    exact_height = square_size

    print("DRAWING COORDINATES:")
    print(f"Square center: ({screen_square_x}, {screen_square_y})")
    print(
        f"Square bounds: left={exact_left}, top={exact_top}, width={exact_width}, height={exact_height}"
    )
    print(
        f"Square rect: ({int(round(exact_left))}, {int(round(exact_top))}, {int(round(exact_width))}, {int(round(exact_height))})"
    )

    # Collision detection calculation
    half_square = square_size / 2
    square_left = square_x - half_square
    square_right = square_x + half_square
    square_top = square_y - half_square
    square_bottom = square_y + half_square

    print("\nCOLLISION DETECTION COORDINATES:")
    print(f"Square center: ({square_x}, {square_y})")
    print(
        f"Square bounds: left={square_left}, right={square_right}, top={square_top}, bottom={square_bottom}"
    )

    # Check alignment
    print("\nALIGNMENT CHECK:")
    print(f"half_size == half_square: {half_size == half_square}")
    print(f"Drawing uses screen coords, collision uses world coords - this is CORRECT")

    # Test collision detection for red dot at center
    dot_radius = 5
    collision_left = square_left - dot_radius
    collision_right = square_right + dot_radius
    collision_top = square_top - dot_radius
    collision_bottom = square_bottom + dot_radius

    print(f"\nCOLLISION BOUNDARIES (accounting for dot radius):")
    print(
        f"Collision zone: left={collision_left}, right={collision_right}, top={collision_top}, bottom={collision_bottom}"
    )

    # Test if red dot at center would collide
    dot_virtual_x, dot_virtual_y = 200.0, 200.0
    is_collision = (
        dot_virtual_x > collision_left
        and dot_virtual_x < collision_right
        and dot_virtual_y > collision_top
        and dot_virtual_y < collision_bottom
    )
    print(
        f"Red dot at center ({dot_virtual_x}, {dot_virtual_y}) collides: {is_collision}"
    )


if __name__ == "__main__":
    test_alignment()
