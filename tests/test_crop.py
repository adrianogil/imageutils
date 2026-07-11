import os
import tempfile
import unittest

from PIL import Image

from dip.crop import clamp_bounding_box, crop_image


class CropTest(unittest.TestCase):
    def test_clamp_bounding_box_to_image_bounds(self):
        self.assertEqual(
            clamp_bounding_box([-5, -10, 12, 15], (10, 8)),
            (0, 0, 10, 8),
        )

    def test_clamp_bounding_box_preserves_inside_box(self):
        self.assertEqual(
            clamp_bounding_box([1, 2, 8, 7], (10, 8)),
            (1, 2, 8, 7),
        )

    def test_clamp_bounding_box_rejects_non_overlapping_box(self):
        with self.assertRaisesRegex(ValueError, 'does not overlap'):
            clamp_bounding_box([11, 1, 20, 5], (10, 8))

    def test_clamp_bounding_box_requires_four_values(self):
        with self.assertRaisesRegex(ValueError, 'exactly four values'):
            clamp_bounding_box([0, 1, 2], (10, 8))

    def test_crop_image_clamps_output_size(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, 'input.png')
            output_path = os.path.join(tmpdir, 'output.png')

            Image.new('RGB', (10, 8), 'red').save(input_path)

            crop_image(input_path, output_path, [-5, -2, 12, 6])

            with Image.open(output_path) as output_image:
                self.assertEqual(output_image.size, (10, 6))


if __name__ == '__main__':
    unittest.main()
