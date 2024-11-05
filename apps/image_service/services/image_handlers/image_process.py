from PIL import Image
import os

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
