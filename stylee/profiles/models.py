from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save



from .utils import create_unique_username

GENDER_CHOICES = [
    # Top
    ('m' , 'Male'),
    ('f' , 'Female'),
    ('u', 'Undefined'),
]

LOCATION_CHOICES = [
    ('ud', 'Undefined'),
    ('us', 'United States'),
    ('ko', 'South Korea'),
    ('jp', 'Japan'),
    ('ch', 'China'),
]

def upload_location(instance, filename):
    new_id = instance.id
    ext = filename.split('.')[-1]
    return "profiles/%s/%s.%s" % (instance.user.id, new_id, ext)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    bio = models.TextField(max_length=255, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='u')
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES, default='ud')
    birth = models.DateField(default='1992-07-23', blank=True, null=True)
    profile_img = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True)
    def __str__(self):
        return str(self.user)

    def get_image_url(self):
        return self.profile_img.url
    #
    # def is_user_blocked_user(self, user):
    #
    #     return


# def pre_save_profile_receiver(sender, instance, *args, **kwargs):
#     #if not instance.username:
#     instance.username = create_unique_username(instance)
#
# pre_save.connect(pre_save_profile_receiver, sender=Profile)

class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follower')
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(
            self.follower.username,
            self.following.username
        )
def pre_save_user_receiver(sender, instance, *args, **kwargs):
    if instance.username:
        instance.username = create_unique_username(instance)

pre_save.connect(pre_save_user_receiver, sender=settings.AUTH_USER_MODEL)

def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if instance.username:
        instance.username = create_unique_username(instance)
        print(instance.username)
    if created:
        # There is no chance to 'get' without creation here.
        #      => because the instance(User) is unique.
        #           => we call get_or_create just for Creation
        profile, is_created = Profile.objects.get_or_create(user=instance)

post_save.connect(post_save_user_receiver, sender=settings.AUTH_USER_MODEL)
