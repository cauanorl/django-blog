from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'categorie'

    def __str__(self):
        return self.category_name
