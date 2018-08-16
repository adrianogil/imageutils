import sys, os

import fnmatch
from os.path import join

from PIL import Image

input_path = sys.argv[1]

all_images = {}

def parse_file(file_path):
    im = Image.open(file_path)
    width, height = im.size

    resolution_str = str(width) + 'x' + str(height)

    # all_images.append(, file))
    if resolution_str in all_images:
        cur_list = all_images[resolution_str]
        cur_list.append(file_path)
        all_images[resolution_str] = cur_list
    else:
        all_images[resolution_str] = [file_path]

def parse_project(project_path, file_extension):
    for root, subFolders, files in os.walk(project_path):
        for filename in files:
            if filename.endswith(file_extension):
                parse_file(join(root, filename))

parse_project(input_path, ('.jpg', '.jpeg', '.gif', '.png'))

for i in all_images:
    print(i + ":  (" + str(len(all_images[i])) + ' images)' )
    for a in all_images[i]:
        print('\t\t' + a)

# def get_key(item):
#     return int(item[0])

# images_count = sorted(branches_count, key=get_key, reverse=True)

# for b in branches_count:
#     print(b[0] + ": " + b[1])
