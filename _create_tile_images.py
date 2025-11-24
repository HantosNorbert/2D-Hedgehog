# This script is only here to create the tile images used in the main Hedgehog 2D application.
# The images are already created in the `tile_images` folder, so it is not necessary to run this script.
# However, if you want to modify the tile images (for example, you want different colors),
# you can alter this script accordingly and run it to generate new images.

from PIL import Image, ImageDraw
import math

# the tile colors, row-by-row. Each tile is tilted with a multiple of 30 degrees in the end.
CONFIGS = [("orange", "blue",   "white",   0),
           ("green",  "orange", "white", -30),
           ("red",    "green",  "white",   0),
           ("blue",   "red",    "white", -30),
           ("yellow", "blue",   "orange", 30),
           ("yellow", "orange", "green",  60),
           ("yellow", "green",  "red",    30),
           ("yellow", "red",    "blue",   60)]

IMAGE_SIZE = 280
SQUARE_SIZE = 100


def draw_rotated_square(draw: ImageDraw.Draw, angle_deg: int, color: tuple[int, int, int]):
    """Draw a rotated square with one corner at the center, with a black border."""
    angle_rad = math.radians(angle_deg)
    corner_points = [(0, 0), (SQUARE_SIZE, 0), (SQUARE_SIZE, SQUARE_SIZE), (0, SQUARE_SIZE)]

    rotated_points = []
    for x, y in corner_points:
        xr = x * math.cos(angle_rad) - y * math.sin(angle_rad)
        yr = x * math.sin(angle_rad) + y * math.cos(angle_rad)
        rotated_points.append((IMAGE_SIZE // 2 + xr, IMAGE_SIZE // 2 + yr))

    draw.polygon(rotated_points, fill=color, outline="black", width=5)


def main():
    for img_idx, config in enumerate(CONFIGS):
        # Create a blank image; the alpha channel must be 0 for a transparent background
        img = Image.new("RGBA", (IMAGE_SIZE, IMAGE_SIZE), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # draw the three rotated squares
        for i in range (3):
            angle = i * 120 + config[3]
            draw_rotated_square(draw, angle, color=config[i])

        img.save(f"tile_images/{img_idx+1}.png")


if __name__ == "__main__":
    main()
