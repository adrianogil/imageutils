from PIL import Image
import sys

target_image = sys.argv[1]
output_image = sys.argv[2]
original_color_str = sys.argv[3]
new_color_str = sys.argv[4]

flags = []
if len(sys.argv) >= 5:
    for i in range(5, len(sys.argv)):
        flags.append(sys.argv[i])

inversed_mode = "-i" in flags


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

for x in range(0, width):
    for y in range(0, height):
        color = pixels[x, y]

        should_switch_color = color[0] == original_color[0] and \
            (len(original_color) <= 1 or color[1] == original_color[1]) and \
            (len(original_color) <= 2 or color[2] == original_color[2]) and \
            (len(original_color) <= 3 or color[3] == original_color[3])

        if inversed_mode:
            should_switch_color = not should_switch_color

        if should_switch_color:
            color = tuple(new_color)
            pixels[x, y] = color
        # print('replaced color')

image.save(output_image)
