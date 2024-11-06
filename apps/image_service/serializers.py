from rest_framework import serializers
from .models import ImageModel


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = [
            'id',
            'name',
            'file_path',
            'upload_date',
            'resolution',
        ]
