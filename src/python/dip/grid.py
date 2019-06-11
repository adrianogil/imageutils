from PIL import Image

import sys
import os

try:
    range = xrange
except NameError:
    pass

target_folder = sys.argv[1]

images_path = [os.path.join(target_folder, img)
               for img in os.listdir(target_folder)
               if '.png' in img or '.jpeg' in img or '.jpg' in img or '.gif' in img]

images = []

max_w = 0
max_h = 0

for path in images_path:
    img = Image.open(path)
    w, h = img.size

    max_w = max(w, max_w)
    max_h = max(h, max_h)

    images.append(img)

print(max_w)
print(max_h)
