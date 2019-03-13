from PIL import Image
import sys

target_image = sys.argv[1]

image = Image.open(target_image)
pixels = image.load()

width, height = image.size

colors_dict = {}
colors = []

for x in range(0, width):
    for y in range(0, height):
        color = pixels[x, y]

        color_key = str(color)
        if color_key in colors_dict:
            colors[colors_dict[color_key]]['value'] += 1
        else:
            colors_dict[color_key] = len(colors)
            colors.append({"color": color_key, "value": 1})

colors = sorted(colors, key=lambda x: x["value"])

for c in colors:
    print("%s: %s" % (c["color"], c["value"]))
