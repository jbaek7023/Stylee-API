from django.db import models
from django.conf import settings


# Create your models here.
class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follower')
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(
            self.follower.username,
            self.following.username
        )
