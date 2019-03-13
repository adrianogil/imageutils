from PIL import Image
import sys

target_image = sys.argv[1]
output_image = sys.argv[2]
boundingbox_str = sys.argv[3]

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


boundingbox = convert_from_str(boundingbox_str)

image = Image.open(target_image)
cropped_image = image.crop(boundingbox)
cropped_image.save(output_image)
