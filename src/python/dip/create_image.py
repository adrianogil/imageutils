import numpy as np
import cv2
import sys


image_path = sys.argv[1]
width = int(sys.argv[2])
height = int(sys.argv[3])

channel_values = [0, 0, 0]

i = 0
for c in sys.argv[4:6]:
    channel_values[i] = int(c)
    i += 1

image = np.ones((width, height, 3))
for c in range(3):
    image[:, :, c] = channel_values[2 - c]

cv2.imwrite(image_path, image)
