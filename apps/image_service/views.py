from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from .models import ImageModel
from .serializers import ImageSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from apps.image_service.services.rabbitMQ_handlers.messaging import (
    _publish_message,

)
from apps.image_service.services.image_handlers.image_process import (
    _process_image
)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated, ]

    def perform_create(self, serializer):
        image_instance = serializer.save()
        _publish_message(
            'image_uploaded',
            image_instance.id,
            'Image created successfully'
        )

        if not image_instance.file_path:
            raise ValidationError(
                "File not found! Please upload file")

        original_image_path = image_instance.file_path.path
        _process_image(image_instance, original_image_path)

    def perform_update(self, serializer):
        image_instance = serializer.save()
        _publish_message(
            'image_updated',
            image_instance.id,
            'Image updated successfully'
        )

    def perform_destroy(self, instance):
        image_id = instance.id
        instance.delete()
        _publish_message(
            'image_deleted',
            image_id,
            'Image deleted successfully'
        )
