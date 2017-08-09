from django.db import models
from django.db.models.signals import post_save

from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user    =   models.OneToOneField(User)
    bio     =   models.TextField(max_length=255, blank=True)

    def __str__(self):
        return str(self.user)

def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile, is_created = Profile.objects.get_or_create(user=instance)

post_save.connect(post_save_user_receiver, sender=User)
