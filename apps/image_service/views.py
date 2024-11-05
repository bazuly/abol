from rest_framework import viewsets, permissions
from .models import ImageModel
from .serializers import ImageSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from apps.image_service.services.image_handlers.image_extraction import (
    extract_metadata
)
from apps.image_service.services.image_handlers.image_process import (
    convert_to_grayscale, save_resized_image
)
from apps.image_service.services.rabbitMQ_handlers.messaging import (
    publish_message
)
from PIL import Image


class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated, ]

    def perform_create(self, serializer):
        image_instance = serializer.save()
        publish_message(
            'image_uploaded',
            image_instance.id,
            'Image created successfully'
        )
        original_image_path = image_instance.file_path.path

        with Image.open(original_image_path) as img:
            metadata = extract_metadata(img, original_image_path)
            image_instance.format = metadata['format']
            image_instance.size = metadata['size']
            image_instance.resolution = metadata['resolution']

            grayscale_img = convert_to_grayscale(img)

            image_instance.file_path_small = save_resized_image(
                grayscale_img, (100, 100),
                image_instance.file_path.name, 'small')
            image_instance.file_path_medium = save_resized_image(
                grayscale_img, (500, 500),
                image_instance.file_path.name, 'medium')

            image_instance.save()

    def perform_update(self, serializer):
        image_instance = serializer.save()
        publish_message(
            'image_updated',
            image_instance.id,
            'Image updated successfully'
        )

    def perform_destroy(self, instance):
        image_id = instance.id
        instance.delete()
        publish_message(
            'image_deleted',
            image_id,
            'Image deleted successfully'
        )
