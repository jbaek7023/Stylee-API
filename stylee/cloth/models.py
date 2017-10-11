from django.db import models
from django.db.models import Q
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.contrib.contenttypes.models import ContentType

import uuid

from .utils import CLOTHES_CHOICES, CLOTHES_SIZE_CHOICES, BIG_CLOTHES_CATEGORIES

def upload_location(instance, filename):
    ext = filename.split('.')[-1]
    random_number = uuid.uuid4()
    random_number = str(random_number).replace('-', '_')
    firstpart, secondpart = random_number[::2], random_number[1::2]
    return "clothes/%s%s%s.%s" % (firstpart, instance.user.id, secondpart, ext)

class ClothManager(models.Manager):
    def all(self, user=None, request=None, *args, **kwargs):
        qs = super(ClothManager, self).all()

        # owned by user
        if user: #user logged in
            qs = qs.exclude(Q(only_me=True) & ~Q(user=user) | Q(archieve=True))
            print(qs)
        return qs

# Create your models here.
class Cloth(models.Model):
    # normal post info
    parent = models.ForeignKey("self", blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    content = models.CharField(max_length=20)

    big_cloth_type = models.CharField(max_length=11, choices=BIG_CLOTHES_CATEGORIES, default='t')
    # Cloth Type and image
    cloth_type = models.CharField(max_length=9, choices=CLOTHES_CHOICES, default='1')
    # img up to width of 1080px.
    # if shared a photo at a lower resolution, we enlarge it to a width of 320 pixels
    # photo at a higher resolution, we size it DOWN to 1080 pixels
    cloth_image = models.ImageField(upload_to=upload_location,
                                null=True,
                                blank=True)
    in_wardrobe = models.BooleanField(default=True)
    only_me = models.BooleanField(default=False)
    archieve = models.BooleanField(default=False)
    publish = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = ClothManager()

    def __str__(self):
        uname = 'None'
        content = 'None'
        if self.user is not None:
            uname = self.user.username
        if self.content is not None:
            content = self.content
        return '{} : {}'.format(uname, content)

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    def save(self, *args, **kwargs):
        # Set the big_cloth_type Here! (Top, Outwear, Pants, Others - (shoes, cabs, earings) )
        cloth_type = self.cloth_type
        if cloth_type in ['ts', 'ct', 'sh']:
            self.big_cloth_type = 't'
        elif cloth_type in ['ja']:
            self.big_cloth_type = 'o'
        elif cloth_type in ['j', 'p']:
            self.big_cloth_type = 'b'
        elif cloth_type in ['s']:
            self.big_cloth_type = 's'
        else:
            self.big_cloth_type = 'e'
        super(Cloth, self).save(*args, **kwargs)

def post_save_cloth_receiver(sender, instance, created, *args, **kwargs):
    if created:
        # There is no chance to 'get' without creation here.
        #      => because the instance(User) is unique.
        #           => we call get_or_create just for Creation
        cloth_detail, is_created = ClothDetail.objects.get_or_create(cloth=instance)

post_save.connect(post_save_cloth_receiver, sender=Cloth)

class ClothDetail(models.Model):
    # Cloth Detail
    cloth = models.OneToOneField(Cloth, null=True, on_delete=models.CASCADE, related_name='c_detail')

    color = models.CharField(max_length=6, blank=True, null=True)
    brand = models.CharField(max_length=30, blank=True, null=True)
    size = models.CharField(max_length=12, choices=CLOTHES_SIZE_CHOICES, blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    seasons = models.CharField(max_length=1, blank=True, null=True)
    delivery_loc = models.CharField(max_length=20, blank=True, null=True)
    link = models.CharField(max_length=20, blank=True, null=True)
    detail = models.TextField(max_length=300, blank=True, null=True)

    def __str__(self):
        if self.cloth is not None:
            return self.cloth.content
        return 'No Content'
