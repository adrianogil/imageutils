from PIL import Image
import sys


def convert_from_str(list_str):
    list_data = []

    values = list_str.split(',')
    for v in values:
        list_data.append(int(v))

    return list_data


def clamp_value(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def clamp_bounding_box(boundingbox, image_size):
    if len(boundingbox) != 4:
        raise ValueError('Bounding box must contain exactly four values: x0,y0,x1,y1')

    image_width, image_height = image_size
    left, top, right, bottom = boundingbox

    clamped_box = (
        clamp_value(left, 0, image_width),
        clamp_value(top, 0, image_height),
        clamp_value(right, 0, image_width),
        clamp_value(bottom, 0, image_height),
    )

    if clamped_box[0] >= clamped_box[2] or clamped_box[1] >= clamped_box[3]:
        raise ValueError('Bounding box does not overlap the image.')

    return clamped_box


def crop_image(target_image, output_image, boundingbox):
    with Image.open(target_image) as image:
        clamped_box = clamp_bounding_box(boundingbox, image.size)
        cropped_image = image.crop(clamped_box)
        cropped_image.save(output_image)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    if len(argv) < 3:
        raise SystemExit('Usage: crop.py <input> <output> <x0,y0,x1,y1>')

    target_image = argv[0]
    output_image = argv[1]
    boundingbox_str = argv[2]
    boundingbox = convert_from_str(boundingbox_str)

    crop_image(target_image, output_image, boundingbox)


if __name__ == '__main__':
    main()
