from PIL import Image
import os
import logging
from .image_extraction import extract_metadata
from tenacity import retry, stop_after_attempt, wait_fixed

# ----------------------------------------------------------------
# https://pillow.readthedocs.io/en/stable/reference/Image.html
# ----------------------------------------------------------------

logger = logging.getLogger(__name__)


def _resize_image(img, size):
    """
    Изменение размера изображения до заданных размеров.
    """
    try:
        return img.resize(size, Image.LANCZOS)
    except Exception as e:
        logger.exception(f"Resize image error: {e}")
        raise RuntimeError("Resize image error.")

# ----------------------------------------------------------------
# https://tenacity.readthedocs.io/en/latest/
# ----------------------------------------------------------------


@retry(
    wait=wait_fixed(5),
    stop=stop_after_attempt(5),
    reraise=True,
    retry=(lambda retry_state: isinstance(
        retry_state.outcome.exception(), RuntimeError)),
)
def _convert_to_grayscale(img):
    """
    Преобразует изображение в оттенки серого.
    """
    try:
        return img.convert('L')
    except Exception as e:
        logger.exception(
            f"Error while convert file to grayscale format: {e}")
        raise RuntimeError(
            "Grayscale convert error")


def _save_resized_image(img, size, base_path, size_name):
    """
    Сохраняет изображение с заданным размером и возвращает путь.
    """
    try:
        filename, ext = os.path.splitext(base_path)
        resized_path = f"images/{size_name}/{filename}_{size_name}{ext}"
        full_path = os.path.join('media_converted', resized_path)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        resized_img = _resize_image(img, size)
        resized_img.save(full_path)

        return resized_path
    except OSError as os_error:
        logger.exception(
            f"File system allow error {os_error}")
        raise OSError("File system allow error")
    except Exception as e:
        logger.exception(f"Unexpected save image error: {e}")
        raise RuntimeError("Unexpected save image error:")


def _process_image(image_instance, image_path):
    try:
        with Image.open(image_path) as img:
            metadata = extract_metadata(img, image_path)
            image_instance.format = metadata['format']
            image_instance.size = metadata['size']
            image_instance.resolution = metadata['resolution']

            grayscale_img = _convert_to_grayscale(img)

            image_instance.file_path_small = _save_resized_image(
                grayscale_img, (100,
                                100), image_instance.file_path.name, 'small'
            )
            image_instance.file_path_medium = _save_resized_image(
                grayscale_img, (500,
                                500), image_instance.file_path.name, 'medium'
            )

            image_instance.save()
    except FileNotFoundError:
        logger.error(f"File not found: {image_path}")
        raise FileNotFoundError(f"File '{image_path}' not found.")
    except Exception as e:
        logger.exception(f"Unexpected process image error: {e}")
        raise RuntimeError("Unexpected process image error. ")


def _extract_and_update_metadata(self, image_instance, img, image_path):
    try:
        metadata = extract_metadata(img, image_path)
        image_instance.format = metadata['format']
        image_instance.size = metadata['size']
        image_instance.resolution = metadata['resolution']
        return metadata
    except Exception as e:
        logger.exception(f"Extraction metadata error {e}.")
        raise RuntimeError("Extraction metadata error. ")
