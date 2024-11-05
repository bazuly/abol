import os


def extract_metadata(img, file_path):
    """
    Извлекает метаданные изображения: формат, разрешение, размер файла.
    """
    metadata = {
        'format': img.format,
        'resolution': f"{img.width}x{img.height}",
        'size': os.path.getsize(file_path),
    }
    return metadata
