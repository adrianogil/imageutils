from PIL import Image
import math
import sys


target_image = sys.argv[1]
output_image = sys.argv[2]
original_color_str = sys.argv[3]
distance = float(sys.argv[4])
new_color_str = sys.argv[5]


def convert_from_str(list_str):
    list_data = []

    values = list_str.split(',')
    for v in values:
        list_data.append(int(v))

    return list_data


original_color = convert_from_str(original_color_str)
new_color = convert_from_str(new_color_str)

image = Image.open(target_image)
pixels = image.load()

width, height = image.size


def color_dist(colorA, colorB):
    comp_size = len(colorA)

    dist = 0.0

    for i in range(0, comp_size):
        dist += (colorA[i] - colorB[i]) * (colorA[i] - colorB[i])

    return math.sqrt(dist)


for x in range(0, width):
    for y in range(0, height):
        color = pixels[x, y]
        # print(color)

        if color_dist(color, original_color) < distance:
            color = tuple(new_color)
            pixels[x, y] = color

image.save(output_image)
