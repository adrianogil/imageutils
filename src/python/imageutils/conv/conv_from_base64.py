import base64
from PIL import Image
from io import BytesIO
import sys

# Function to convert Base64 to Image
def base64_to_image(base64_string, output_file):
    img_data = base64.b64decode(base64_string)
    img = Image.open(BytesIO(img_data))
    img.save(output_file)

target_base64_file = sys.argv[1]

# Read Base64 string from a file or directly assign it here
with open(target_base64_file, "r") as file:
    base64_str = file.read().replace('data:image/png;base64,', '')

# Convert and save the image
base64_to_image(base64_str, 'output_image.png')
