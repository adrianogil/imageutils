from PIL import Image

import os

try:
    range = xrange
except NameError:
    pass

def crop(image_path, crop_horizontal, crop_vertical, save_path = ""):

    image_basename = os.path.basename(image_path)
    image_splitext = os.path.splitext(image_basename)
    image_basename = image_splitext[0]
    image_extension = image_splitext[1]

    img = Image.open(image_path)
    img_width, img_height = img.size

    crop_width = img_width / crop_horizontal
    crop_height = img_height / crop_vertical

    for i in range(0, crop_horizontal):
        for j in range(0, crop_vertical):
            box = (i*crop_width, j*crop_height, (i+1)*crop_width, (j+1)*crop_height)
            a = img.crop(box)
            a.load()
            a.save(save_path + image_basename + "_" + str(i) + "_" + str(j) + image_extension)
            a.close()

if __name__ == "__main__":
    import sys

    target_image_path = sys.argv[1]
    crop_horizontal = int(sys.argv[2]) # 1,2,...
    crop_vertical = int(sys.argv[3]) # 1,2,...

    crop(target_image_path, crop_horizontal, crop_vertical)
