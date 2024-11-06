import unittest
from unittest import mock
from PIL import Image, UnidentifiedImageError
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
        self.image_instance.file_path.path = "/path/to/test_image.jpg"

    @mock.patch("apps.image_service.services.image_handlers.image_process.Image.open")
    def test_process_image_success(self, mock_open):
        """Тест успешной обработки изображения."""

        mock_open.return_value = self.test_image
        with mock.patch("apps.image_service.services.image_handlers.image_process.save_resized_image") as mock_save:
            _process_image(self.image_instance,
                           self.image_instance.file_path.path)
            self.assertTrue(mock_save.called)
            self.assertTrue(self.image_instance.save.called)

    @mock.patch("apps.image_service.services.image_handlers.image_process.Image.open",
                side_effect=FileNotFoundError)
    def test_process_image_file_not_found(self, mock_open):
        """Тест обработки отсутствующего файла изображения."""

        with self.assertRaises(FileNotFoundError):
            _process_image(self.image_instance,
                           self.image_instance.file_path.path)

    @mock.patch("apps.image_service.services.image_handlers.image_process.Image.open",
                side_effect=UnidentifiedImageError)
    def test_process_image_invalid_image(self, mock_open):
        """Тест обработки некорректного файла изображения."""

        with self.assertRaises(ValueError):
            _process_image(self.image_instance,
                           self.image_instance.file_path.path)

    def test_resize_image_success(self):
        """Тест успешного изменения размера изображения."""

        resized_image = _resize_image(self.test_image, (100, 100))
        self.assertEqual(resized_image.size, (100, 100))

    @mock.patch("apps.image_service.services.image_handlers.image_process.Image.resize",
                side_effect=Exception("Resize error"))
    def test_resize_image_error(self, mock_resize):
        """Тест ошибки при изменении размера изображения."""

        with self.assertRaises(RuntimeError):
            _resize_image(self.test_image, (100, 100))

    def test_convert_to_grayscale_success(self):
        """Тест успешного преобразования изображения в оттенки серого."""

        grayscale_image = _convert_to_grayscale(self.test_image)
        self.assertEqual(grayscale_image.mode, 'L')

    @mock.patch("apps.image_service.services.image_handlers.image_process.Image.convert",
                side_effect=Exception("Convert error"))
    def test_convert_to_grayscale_error(self, mock_convert):
        """Тест ошибки при преобразовании изображения в оттенки серого."""

        with self.assertRaises(RuntimeError):
            _convert_to_grayscale(self.test_image)

    @mock.patch("apps.image_service.services.image_handlers.image_process.os.makedirs")
    @mock.patch("apps.image_service.services.image_handlers.image_process.Image.save")
    def test_save_resized_image_success(self, mock_save, mock_makedirs):
        """Тест успешного сохранения изменённого изображения."""

        resized_path = _save_resized_image(
            self.test_image, (100, 100), "test_image.jpg", "small")
        self.assertTrue(mock_makedirs.called)
        self.assertTrue(mock_save.called)
        self.assertIn("images/small/test_image_small.jpg", resized_path)

    @mock.patch("apps.image_service.services.image_handlers.image_process.os.makedirs",
                side_effect=OSError("Filesystem error"))
    def test_save_resized_image_os_error(self, mock_makedirs):
        """Тест ошибки файловой системы при сохранении изображения."""

        with self.assertRaises(OSError):
            _save_resized_image(self.test_image, (100, 100),
                                "test_image.jpg", "small")

    @mock.patch("apps.image_service.services.image_handlers.image_process.Image.save",
                side_effect=Exception("Save error"))
    def test_save_resized_image_save_error(self, mock_save):
        """Тест ошибки при сохранении изображения."""

        with self.assertRaises(RuntimeError):
            _save_resized_image(self.test_image, (100, 100),
                                "test_image.jpg", "small")


if __name__ == '__main__':
    unittest.main()
