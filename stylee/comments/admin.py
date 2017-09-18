from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'publish', 'content_type')
    class Meta:
        model = Comment
# Register your models here.
admin.site.register(Comment, CommentAdmin)
