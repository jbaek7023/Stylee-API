from django.db import models
from django.conf import settings
from stream_django.activity import Activity
from stream_django.feed_manager import feed_manager
from django.db.models.signals import post_save, post_delete

# Create your models here.
class Follow(models.Model, Activity):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follower')
    target = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(
            self.user.username,
            self.target.username
        )

    @classmethod
    def activity_related_models(cls):
        return ['user', 'target']

    @property
    def activity_object_attr(self):
        return self

    @property
    def activity_author_feed(self):
        return 'Follow'

    @property
    def activity_notify(self):
        # get liked object
        # content_type, object_id
        following_instance = self.target
        if following_instance:
            # Notify to following user
            target_feed = feed_manager.get_notification_feed(following_instance.id)
        return [target_feed]

def follow_listner(sender, instance, created, **kwargs):
    if created:
        feed_manager.follow_user(instance.user.id, instance.target.id)

def unfollow_listener(sender, instance, **kwargs):
    feed_manager.unfollow_user(instance.user.id, instance.target.id)

post_save.connect(follow_listner, sender=Follow)
post_delete.connect(unfollow_listener, sender=Follow)
