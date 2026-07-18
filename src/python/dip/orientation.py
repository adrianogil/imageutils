from PIL import Image, ImageOps


def open_oriented_image(image_path):
    image = Image.open(image_path)
    oriented_image = ImageOps.exif_transpose(image)

    if oriented_image is not image:
        image.close()

    return oriented_image
