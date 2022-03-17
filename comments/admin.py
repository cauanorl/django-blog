from django.contrib import admin
from .models import Comment


class CommentsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user_comment', 'email_comment', 'post_comment',
        'date_comment', 'published_comment')
    list_display_links = ('id', 'user_comment', 'email_comment')
    list_editable = ('published_comment',)


# Register your models here.
admin.site.register(Comment, CommentsAdmin)
