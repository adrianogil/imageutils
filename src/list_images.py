import os
import sys
import fnmatch
from os.path import join
from PIL import Image

input_path = sys.argv[1]

verbose_mode = '-v' in sys.argv

all_images = {}

def parse_file(file_path):
    im = Image.open(file_path)
    width, height = im.size

    resolution_str = str(width) + 'x' + str(height)

    # all_images.append(, file))
    if resolution_str in all_images:
        cur_list = all_images[resolution_str]["images"]
        cur_list.append(file_path)
    else:
        all_images[resolution_str] = {
            "width": width,
            "height": height,
            "images": [file_path]
        }

def parse_project(project_path, file_extension):
    for root, subFolders, files in os.walk(project_path):
        for filename in files:
            if filename.endswith(file_extension):
                parse_file(join(root, filename))

parse_project(input_path, ('.jpg', '.jpeg', '.gif', '.png'))

sorted_all_images = sorted(all_images.keys(), key=lambda x: len(all_images[x]["images"]), reverse=True)

mean_width = 0
mean_height = 0
total = 0

for i in sorted_all_images:
    number_images = len(all_images[i]["images"])
    print(i + ":  (" + str(number_images) + ' images)')

    mean_height += number_images * all_images[i]["height"]
    mean_width += number_images * all_images[i]["width"]
    total += number_images

    if verbose_mode:
        for a in all_images[i]["images"]:
            print('\t\t' + a)

mean_width = mean_width * 1.0 / total
mean_height = mean_height * 1.0 / total

print("Mean size: %sx%s" % (mean_width, mean_height))
