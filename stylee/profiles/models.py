from django.db import models
from django.db.models.signals import pre_save, post_save

from django.conf import settings

# create  unique username
import random
import string
from django.utils.text import slugify

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_unique_username(instance, username=None):
    # instance : Profile
    if not username:
        username = str(instance.user)

    # only allow lower case for the username
    username = username.lower()

    # User doesn't expect to
    exists = Profile.objects.filter(username=username).exists()
    if exists:
        new_username = "%s%s" % (username, random_string_generator(size=1))
        return create_unique_username(instance, username=new_username)
    return username

# Create your models here.
# Add Verified?
class Profile(models.Model):
    user            =   models.OneToOneField(settings.AUTH_USER_MODEL)
    username        =   models.SlugField(max_length=20)
    bio             =   models.TextField(max_length=255, blank=True)
    
    def __str__(self):
        return str(self.user)
    #
    # def is_user_blocked_user(self, user):
    #
    #     return

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

post_save.connect(post_save_user_receiver, sender=settings.AUTH_USER_MODEL)
