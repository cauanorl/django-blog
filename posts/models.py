from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from PIL import Image
from django.conf import settings
import os.path

from categories.models import Category

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    excerpt = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    image = models.ImageField(upload_to='media/%Y/%m/%d/', blank=True, null=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image(self.image.name, 800)
    
    @staticmethod
    def resize_image(image_name, new_width):
        image_path = settings.MEDIA_ROOT / image_name
        image = Image.open(image_path)  # from PIL import Image
        width, height = image.size
        new_height = round((new_width * height) / width)
        
        if int(width) <= new_width:
            image.close()
            return

        new_image = image.resize((new_width, new_height), Image.ANTIALIAS)
        new_image.save(
            image_path,
            optimize=True,
            quality=60,
        )
        image.close()
        new_image.close()
