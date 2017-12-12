from django.db import models
from django.db.models import Q
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.contrib.contenttypes.models import ContentType
from django.core.validators import validate_comma_separated_integer_list
import uuid
from stream_django.activity import Activity

from .utils import (
    CLOTHES_SIZE_CHOICES,
    BIG_CLOTHES_CATEGORIES,
    TOP_TYPES,
    OUTWEAR_TYPES,
    SHOE_TYPES,
    BOTTOM_TYPES,
    ETC_TYPES
)

def upload_location(instance, filename):
    # This is 100% valid.
    ext = filename.split('.')[-1]
    random_number = uuid.uuid4()
    return "clothes/%s.%s" % (random_number, ext)

class ClothManager(models.Manager):
    def all(self, user=None, request=None, *args, **kwargs):
        qs = super(ClothManager, self).all()

        # owned by user
        if user: #user logged in
            qs = qs.exclude(Q(only_me=True) & ~Q(user=user) | Q(archieve=True))
            print(qs)
        return qs

# Outfit Detail과 비슷한 구조로가기.
class Cloth(models.Model):
    # normal post info
    parent = models.ForeignKey("self", blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    content = models.CharField(max_length=20, null=True, blank=True)

    big_cloth_type = models.CharField(max_length=11, choices=BIG_CLOTHES_CATEGORIES, default='t', null=True, blank=True)
    # Cloth Type and image
    cloth_type = models.CharField(max_length=15, default='1', null=True, blank=True)
    # img up to width of 1080px.
    # if shared a photo at a lower resolution, we enlarge it to a width of 320 pixels
    # photo at a higher resolution, we size it DOWN to 1080 pixels
    cloth_image = models.ImageField(upload_to=upload_location,
                                null=True,
                                blank=True)
    in_wardrobe = models.BooleanField(default=True)
    only_me = models.BooleanField(default=False)
    link = models.CharField(max_length=20, blank=True, null=True)

    archieve = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
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
        if cloth_type in TOP_TYPES:
            self.big_cloth_type = 'Top'
        elif cloth_type in OUTWEAR_TYPES:
            self.big_cloth_type = 'Outerwear'
        elif cloth_type in BOTTOM_TYPES:
            self.big_cloth_type = 'Bottom'
        elif cloth_type in SHOE_TYPES:
            self.big_cloth_type = 'Shoes'
        else:
            self.big_cloth_type = 'ETC'
        super(Cloth, self).save(*args, **kwargs)


def post_save_cloth_receiver(sender, instance, created, *args, **kwargs):
    if created:
        # There is no chance to 'get' without creation here.
        #      => because the instance(User) is unique.
        #           => we call get_or_create just for Creation
        cloth_detail, is_created = ClothDetail.objects.get_or_create(cloth=instance)

post_save.connect(post_save_cloth_receiver, sender=Cloth)

class ClothDetail(models.Model):
    # Cloth Detail => this is for search only.
    cloth = models.OneToOneField(Cloth, null=True, on_delete=models.CASCADE, related_name='c_detail')
    color = models.CharField(validators=[validate_comma_separated_integer_list], max_length=30, blank=True, null=True)
    brand = models.CharField(max_length=30, blank=True, null=True)
    size = models.CharField(validators=[validate_comma_separated_integer_list], max_length=30, blank=True, null=True)
    sex = models.CharField(max_length=5, blank=True, null=True)
    seasons = models.CharField(validators=[validate_comma_separated_integer_list], max_length=30, blank=True, null=True)
    location = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=299, blank=True, null=True)

    def __str__(self):
        if self.cloth is not None:
            if self.cloth.content is "" or self.cloth.content is None:
                return 'No Content'
            return self.cloth.content
        return 'No Content'
