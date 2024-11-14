import unittest
from unittest import mock
from PIL import Image
from apps.image_service.services.image_handlers.image_process import (
    _resize_image,
    _convert_to_grayscale,
    _save_resized_image,
    _process_image,
)
from apps.image_service.models import ImageModel


class TestImageProcessingFunctions(unittest.TestCase):

    def setUp(self):
        self.test_image = Image.new('RGB', (200, 200), color='white')
        self.image_instance = mock.Mock(spec=ImageModel)
        self.image_instance.file_path.name = "test_image.jpg"
        self.image_instance.file_path.path = "test_image.jpg"

    @mock.patch("apps.image_service.services.image_handlers.image_process.extract_metadata")
    @mock.patch("apps.image_service.services.image_handlers.image_process.Image.open")
    @mock.patch("apps.image_service.services.image_handlers.image_process._save_resized_image")
    def test_process_image_success(self, mock_save, mock_open, mock_extract_metadata):
        """Тест успешной обработки изображения."""

        mock_open.return_value = self.test_image

        # metadata example
        mock_extract_metadata.return_value = {
            "width": 200,
            "height": 200,
            "size": 50,
            "resolution": "500x500",
            "format": "JPEG"
        }

        _process_image(self.image_instance, self.image_instance.file_path.path)

        self.assertTrue(mock_save.called)
        self.assertTrue(self.image_instance.save.called)

    @mock.patch("apps.image_service.services.image_handlers.image_process.Image.open",
                side_effect=FileNotFoundError)
    def test_process_image_file_not_found(self, mock_open):
        """Тест обработки отсутствующего файла изображения."""

        with self.assertRaises(FileNotFoundError):
            _process_image(self.image_instance,
                           self.image_instance.file_path.path)

    def test_resize_image_success(self):
        """Тест успешного изменения размера изображения."""

        resized_image = _resize_image(self.test_image, (100, 100))
        self.assertEqual(resized_image.size, (100, 100))

    def test_convert_to_grayscale_success(self):
        """Тест успешного преобразования изображения в оттенки серого."""

        grayscale_image = _convert_to_grayscale(self.test_image)
        self.assertEqual(grayscale_image.mode, 'L')


    @mock.patch("apps.image_service.services.image_handlers.image_process.os.makedirs",
                side_effect=OSError("Filesystem error"))
    def test_save_resized_image_os_error(self, mock_makedirs):
        """Тест ошибки файловой системы при сохранении изображения."""

        with self.assertRaises(OSError):
            _save_resized_image(self.test_image, (100, 100),
                                "test_image.jpg", "small")


if __name__ == '__main__':
    unittest.main()
