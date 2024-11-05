from rest_framework import serializers
from .models import ImageModel


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = [
            'id',
            'name',
            'file_path',
            'file_path_small',
            'file_path_medium',
            'upload_date',
            'resolution',
            'size',
            'format'
        ]
