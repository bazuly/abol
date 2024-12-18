import os
import logging
from PIL import Image
from typing import Any, Dict

logger = logging.getLogger(__name__)


def extract_metadata(img: Image.Image, file_path: str) -> dict[str, Any]:
    """
    Извлекает метаданные изображения: формат, разрешение, размер файла.
    """

    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found {file_path}")
            raise FileNotFoundError(f"File '{file_path}' not found")

        metadata: Dict[str, Any] = {
            'format': img.format,
            'resolution': f"{img.width}x{img.height}",
            'size': os.path.getsize(file_path),
        }
        return metadata

    except FileNotFoundError as fnf_error:
        logger.exception(f"Error: {fnf_error}")
        raise fnf_error

    except OSError as os_error:
        logger.exception("File system get metadata error")
        raise OSError(f"File now allowed '{file_path}': {os_error}")

    except Exception as e:
        logger.exception("Unexpected error.")
        raise RuntimeError(f"Unexpected error'{file_path}': {e}")
