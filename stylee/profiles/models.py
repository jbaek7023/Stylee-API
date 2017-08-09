from django.db import models
from django.db.models.signals import pre_save, post_save

from django.contrib.auth.models import User
from .utils import random_string_generator, create_unique_username

# Create your models here.
class Profile(models.Model):
    user        =   models.OneToOneField(User)
    username    =   models.SlugField(max_length=20)
    bio         =   models.TextField(max_length=255, blank=True)

    def __str__(self):
        return str(self.user)

def pre_save_profile_receiver(sender, instance, *args, **kwargs):
    #if not instance.username:
    instance.username = create_unique_username(instance)

pre_save.connect(pre_save_profile_receiver, sender=Profile)

def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        # There is no chance to 'get' without creation here.
        #      => because the instance(User) is unique.
        #           => we call get_or_create just for Creation
        profile, is_created = Profile.objects.get_or_create(user=instance)

post_save.connect(post_save_user_receiver, sender=User)
