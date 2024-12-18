# Generated by Django 5.1.2 on 2024-11-04 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('file_path', models.ImageField(upload_to='images/')),
                ('file_path_small', models.ImageField(blank=True, null=True, upload_to='images/small/')),
                ('file_path_medium', models.ImageField(blank=True, null=True, upload_to='images/medium/')),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('resolution', models.CharField(max_length=50)),
                ('size', models.PositiveIntegerField(blank=True, null=True)),
                ('format', models.CharField(blank=True, max_length=10)),
            ],
        ),
    ]
