from django.apps import AppConfig
from django.conf import settings
import os

class ImageViewerConfig(AppConfig):
    name = 'image_viewer'

    def ready(self):
        from .models import Image  # Import here to avoid circular import
        self.add_images_to_database()

    def add_images_to_database(self):
        from .models import Image  # Import here to avoid circular import
        media_images_path = os.path.join(settings.MEDIA_ROOT, 'images')
        for filename in os.listdir(media_images_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_path = os.path.join('images', filename)
                # Check if image is already in the database
                if not Image.objects.filter(image=image_path).exists():
                    Image.objects.create(name=filename, image=image_path)
