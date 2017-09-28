from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save



from .utils import create_unique_username

GENDER_CHOICES = [
    ('m' , 'Male'),
    ('f' , 'Female'),
    ('u', 'Not Specified'),
]

LOCATION_CHOICES = [
    ('ud', 'Not Specified'),
    ('us', 'United States'),
    ('ko', 'South Korea'),
    ('jp', 'Japan'),
    ('ch', 'China'),
]

def upload_location(instance, filename):
    ext = filename.split('.')[-1]
    random_number = uuid.uuid4()
    random_number = str(random_number).replace('-', '_')
    firstpart, secondpart = random_number[::2], random_number[1::2]
    return "profiles/%s%s%s.%s" % (firstpart, instance.user.id, secondpart, ext)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    title = models.TextField(max_length=155, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='u') # Recommend Factor
    location = models.CharField(max_length=40, choices=LOCATION_CHOICES, default='ud') # Recommend Factor
    birth = models.DateField(default='1992-07-23', blank=True, null=True) # Recommend Factor
    height = models.CharField(max_length=5, default='undefined')
    height_in_ft = models.BooleanField(default=True)
    profile_img = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True)

    def __str__(self):
        return str(self.user)

    def get_image_url(self):
        return self.profile_img.url

def pre_save_user_receiver(sender, instance, *args, **kwargs):
    if instance.username:
        instance.username = create_unique_username(instance)

pre_save.connect(pre_save_user_receiver, sender=settings.AUTH_USER_MODEL)

def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if instance.username:
        instance.username = create_unique_username(instance)
    if created:
        # There is no chance to 'get' without creation here.
        #      => because the instance(User) is unique.
        #           => we call get_or_create just for Creation
        profile, is_created = Profile.objects.get_or_create(user=instance)

post_save.connect(post_save_user_receiver, sender=settings.AUTH_USER_MODEL)
