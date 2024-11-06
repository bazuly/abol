from PIL import Image
import os
from .image_extraction import extract_metadata

# ----------------------------------------------------------------
# https://pillow.readthedocs.io/en/stable/reference/Image.html
# ----------------------------------------------------------------


def resize_image(img, size):
    """
    Меняет размер изображения до заданных размеров.
    """
    return img.resize(size, Image.LANCZOS)


def convert_to_grayscale(img):
    """
    Преобразует изображение в оттенки серого.
    """
    return img.convert('L')


def save_resized_image(img, size, base_path, size_name):
    """
    Сохраняет изображение с заданным размером и возвращает путь.
    """
    filename, ext = os.path.splitext(base_path)
    resized_path = f"images/{size_name}/{filename}_{size_name}{ext}"
    full_path = os.path.join('media_converted', resized_path)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    resized_img = resize_image(img, size)
    resized_img.save(full_path)

    return resized_path


def _process_image(image_instance, image_path):
    original_image_path = image_instance.file_path.path
    with Image.open(original_image_path) as img:
        metadata = extract_metadata(img, original_image_path)
        image_instance.format = metadata['format']
        image_instance.size = metadata['size']
        image_instance.resolution = metadata['resolution']

        grayscale_img = convert_to_grayscale(img)

        image_instance.file_path_small = save_resized_image(
            grayscale_img, (100, 100),
            image_instance.file_path.name,
            'small'
        )
        image_instance.file_path_medium = save_resized_image(
            grayscale_img,
            (500, 500), image_instance.file_path.name,
            'medium'
        )

        image_instance.save()


def _extract_and_update_metadata(self, image_instance, img, image_path):
    metadata = extract_metadata(img, image_path)
    image_instance.format = metadata['format']
    image_instance.size = metadata['size']
    image_instance.resolution = metadata['resolution']
    return metadata
