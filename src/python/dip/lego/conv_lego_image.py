import os
import sys
import csv
import math
import random
import argparse
from typing import List, Tuple
from PIL import Image  # for image loading, resizing, and pixel access


class LegoColor:
    def __init__(self, hex_code: str, lego_id: int, name: str, r: int, g: int, b: int):
        self.hex = hex_code
        self.lego_id = lego_id
        self.name = name
        self.r = r
        self.g = g
        self.b = b


def load_colors_from_csv(csv_path: str) -> List[LegoColor]:
    colors = []
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        # Assuming the CSV structure matches: legoid,name,hex,r,g,b
        header = next(reader, None)  # Skip header
        for row in reader:
            lego_id = int(row[0])
            name = row[1]
            hex_code = row[2]
            r = int(row[3])
            g = int(row[4])
            b = int(row[5])
            colors.append(LegoColor(hex_code, lego_id, name, r, g, b))
    return colors

def load_default_colors() -> List[LegoColor]:
    # A small subset of the default colors from the original code
    # Add more if needed
    return [
        LegoColor("FFE371", 1027, "Modulex Light Yellow", 255, 227, 113),
        LegoColor("C91A09", 4, "Red", 201, 26, 9),
        LegoColor("FFFFFF", 15, "White", 255, 255, 255),
        LegoColor("05131D", 0, "Black", 5, 19, 29),
        LegoColor("F2CD37", 14, "Yellow", 242, 205, 55),
        LegoColor("0055BF", 1, "Blue", 0, 85, 191),
        LegoColor("237841", 2, "Green", 35, 120, 65),
    ]

def calculate_distance(p1: Tuple[int, int, int], p2: Tuple[int, int, int]) -> float:
    # p1 and p2 are (R, G, B) tuples of ints
    # Distance as in the original: weighted Euclidean
    return math.sqrt(((p2[0]-p1[0]) * 0.30)**2 +
                     ((p2[1]-p1[1]) * 0.59)**2 +
                     ((p2[2]-p1[2]) * 0.11)**2)

def resize_image(input_path: str, x_len: int, y_len: int) -> Image.Image:
    img = Image.open(input_path).convert("RGBA")
    # Use nearest neighbor to mimic original behavior
    resized = img.resize((x_len, y_len), resample=Image.Resampling.NEAREST)
    return resized

def map_image_to_lego(img: Image.Image, colors: List[LegoColor], block_size: int) -> Tuple[Image.Image, List[List[str]]]:
    width, height = img.size
    result_img = Image.new("RGBA", (width, height))
    pixels = img.load()
    result_pixels = result_img.load()

    build_map = []
    unique_colors = set()

    # Iterate over blocks
    for block_x in range(0, width, block_size):
        row_map = []
        for block_y in range(0, height, block_size):
            # Determine block boundaries
            bx_end = min(block_x + block_size, width)
            by_end = min(block_y + block_size, height)

            # Compute average color of the block
            total_r = total_g = total_b = 0
            count = 0
            for x in range(block_x, bx_end):
                for y in range(block_y, by_end):
                    r, g, b, a = pixels[x, y]
                    if a == 0:
                        # Treat transparent as white
                        r, g, b = 255, 255, 255
                    total_r += r
                    total_g += g
                    total_b += b
                    count += 1

            avg_r = total_r // count
            avg_g = total_g // count
            avg_b = total_b // count

            # Find closest LegoColor for the average
            min_dist = float('inf')
            best_color = None
            for c in colors:
                dist = calculate_distance((avg_r, avg_g, avg_b), (c.r, c.g, c.b))
                if dist < min_dist:
                    min_dist = dist
                    best_color = c

            # Fill the entire block with the best match color
            for x in range(block_x, bx_end):
                for y in range(block_y, by_end):
                    result_pixels[x, y] = (best_color.r, best_color.g, best_color.b, 255)
                    row_map.append(f"[{x}][{y}] = R:{best_color.r}, G:{best_color.g}, B:{best_color.b}\t-{best_color.name}\n")

            unique_colors.add(best_color.name)
        build_map.append(row_map)

    return result_img, build_map

def save_results(out_dir: str, result_img: Image.Image, build_map: List[List[str]]):
    # Generate random string for file name
    rand_str = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))

    if out_dir and not out_dir.endswith(os.sep):
        out_dir += os.sep

    # Save build map
    build_map_file = out_dir + rand_str + "_build_map.txt"
    with open(build_map_file, "w", encoding="utf-8") as f:
        for row in build_map:
            for cell in row:
                f.write(cell)

    # Save image
    image_result_file = out_dir + rand_str + "_out.png"
    result_img.save(image_result_file, "PNG")

    # Calculate stats
    piece_count = sum(len(r) for r in build_map)
    color_count = len({c.split('-')[-1].strip() for row in build_map for c in row})
    print(f"For this Lego conversion we used {piece_count} pieces and {color_count} colors")
    print(f"The image preview has been generated at {image_result_file}")
    print(f"The building map has been generated at {build_map_file}")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert an image to a LEGO color approximation.")
    parser.add_argument("--colors", type=str, default="", help="CSV file with colors data.")
    parser.add_argument("--image", type=str, required=True, help="Target image path (PNG).")
    parser.add_argument("--out", type=str, default="", help="Output directory.")
    parser.add_argument("--xlen", type=int, help="Resize width.")
    parser.add_argument("--ylen", type=int, help="Resize height.")
    parser.add_argument("--scale", type=float, help="Scale factor for resizing.")
    parser.add_argument("--block-size", type=int, default=1, help="Size of the block for more 'blocky' results.")
    return parser.parse_args()

def main():
    args = parse_args()

    if not os.path.exists(args.image):
        print(f"Error: Image file not found: {args.image}")

    if not os.path.exists(args.out):
        os.makedirs(args.out)

    # Load colors
    if args.colors:
        colors = load_colors_from_csv(args.colors)
    else:
        colors = load_default_colors()

    # If xlen or ylen aren't provided, use original image size
    if not args.xlen or not args.ylen:
        with Image.open(args.image) as tmp_img:
            args.xlen, args.ylen = tmp_img.size
    if args.scale:
        args.xlen = int(args.xlen * args.scale)
        args.ylen = int(args.ylen * args.scale)



    # Process the image
    resized_img = resize_image(args.image, args.xlen, args.ylen)
    result_img, build_map = map_image_to_lego(resized_img, colors, args.block_size)

    # Save the results
    save_results(args.out, result_img, build_map)

if __name__ == "__main__":
    main()
