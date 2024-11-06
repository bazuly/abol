from django.db import models


class ImageModel(models.Model):
    name = models.CharField(max_length=255)
    file_path = models.ImageField(
        upload_to='images/', help_text='Upload file')
    file_path_small = models.ImageField(
        upload_to='images/small/', blank=True, null=True)
    file_path_medium = models.ImageField(
        upload_to='images/medium/', blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    resolution = models.CharField(
        max_length=50, help_text='500x500 example format')
    size = models.PositiveIntegerField(blank=True, null=True)
    format = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name
