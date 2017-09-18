from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class CommentManager(models.Manager):
    def all(self):
        # filter only parent
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        # content_type = ContentType.objects.get_for_model(Outfit)
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id)
        # comments = Comment.objects.filter(content_type=content_type, object_id=obj_id)
        return qs

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    parent = models.ForeignKey("self", null=True, blank=True)

    content = models.TextField(max_length=500, blank=True, null=True)
    publish = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = CommentManager()

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.content

    def children(self):
        return Comment.objects.filter(parent=self)

    def is_parent(self):
        if self.parent is not None:
            return False
        return True


# view,
# instance.comment_set.all ? nope!
# ContentType.objects.get_for_model(User)
# content_type = ContentType.objects.get_for_model(Outfit)
# obj_id = instance.id
# comments = Comment.objects.filter(content_type=content_type, object_id=obj_id)
# comment.content_object <-- parentObject ... object.post_name

# you can do this on view, but we recommend you to do it on ModelManager
# returns qs we want.
