import os
import importlib.util
import tempfile
import unittest

from PIL import Image

from dip.crop import crop_image
from dip.lego.conv_lego_image import resize_image
from dip.orientation import open_oriented_image


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
CROP_IMAGE_PATH = os.path.join(PROJECT_ROOT, 'src', 'crop_image.py')


def load_crop_image_script():
    spec = importlib.util.spec_from_file_location('crop_image_script', CROP_IMAGE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def create_exif_oriented_image(image_path):
    image = Image.new('RGB', (2, 3))
    pixels = {
        (0, 0): (255, 0, 0),
        (1, 0): (0, 255, 0),
        (0, 1): (0, 0, 255),
        (1, 1): (255, 255, 0),
        (0, 2): (255, 0, 255),
        (1, 2): (0, 255, 255),
    }

    for position, color in pixels.items():
        image.putpixel(position, color)

    exif = Image.Exif()
    exif[274] = 6
    image.save(image_path, exif=exif)


class ExifOrientationTest(unittest.TestCase):
    def test_open_oriented_image_applies_exif_orientation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, 'oriented.png')
            create_exif_oriented_image(input_path)

            with open_oriented_image(input_path) as image:
                self.assertEqual(image.size, (3, 2))
                self.assertEqual(image.getpixel((0, 0)), (255, 0, 255))
                self.assertEqual(image.getpixel((2, 1)), (0, 255, 0))

    def test_crop_image_uses_oriented_dimensions_and_pixels(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, 'oriented.png')
            output_path = os.path.join(tmpdir, 'cropped.png')
            create_exif_oriented_image(input_path)

            crop_image(input_path, output_path, [0, 0, 1, 1])

            with Image.open(output_path) as output_image:
                self.assertEqual(output_image.size, (1, 1))
                self.assertEqual(output_image.getpixel((0, 0)), (255, 0, 255))

    def test_resize_image_uses_oriented_pixels_before_resizing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, 'oriented.png')
            create_exif_oriented_image(input_path)

            resized = resize_image(input_path, 3, 2)

            self.assertEqual(resized.size, (3, 2))
            self.assertEqual(resized.getpixel((0, 0)), (255, 0, 255, 255))
            self.assertEqual(resized.getpixel((2, 1)), (0, 255, 0, 255))

    def test_grid_crop_script_uses_oriented_dimensions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, 'oriented.png')
            create_exif_oriented_image(input_path)
            crop_image_script = load_crop_image_script()

            crop_image_script.crop(input_path, 1, 1, tmpdir + os.sep)

            with Image.open(os.path.join(tmpdir, 'oriented_0_0.png')) as output_image:
                self.assertEqual(output_image.size, (3, 2))
                self.assertEqual(output_image.getpixel((0, 0)), (255, 0, 255))


if __name__ == '__main__':
    unittest.main()
