from django.contrib import admin
from .models import Post
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(SummernoteModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'date', 'published')
    list_display_links = ('id', 'title', 'author')
    list_editable = ('published',)
    summernote_fields = ('content',)


# Register your models here.
admin.site.register(Post, PostAdmin)
