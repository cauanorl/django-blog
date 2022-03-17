from django.db import models
from posts.models import Post
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Comment(models.Model):
    name_comment = models.CharField(max_length=150, verbose_name='Name')
    email_comment = models.EmailField(verbose_name='Email')
    comment = models.TextField()
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_comment = models.DateTimeField(default=timezone.now, verbose_name='Date')
    published_comment = models.BooleanField(default=True, verbose_name='Published')

    def __str__(self):
        return self.name_comment
