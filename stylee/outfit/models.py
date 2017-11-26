from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from .utils import GENDER_CHOICES

from cloth.models import Cloth
from comments.models import Comment
import uuid
def upload_location_outfit(instance, filename):
    ext = filename.split('.')[-1]
    random_number = uuid.uuid4()
    return "outfits/%s.%s" % (random_number, ext)

class OutfitManager(models.Manager):
    def all(self, user=None, request=None, *args, **kwargs):
        qs = super(OutfitManager, self).all()

        # owned by user
        if user: #user logged in
            qs = qs.exclude(Q(only_me=True) & ~Q(user=user))
        return qs

# Create your models here.
class Outfit(models.Model):
    # normal post info
    parent = models.ForeignKey("self", blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    content = models.CharField(max_length=30)
    publish = models.DateTimeField(auto_now=False, auto_now_add=True)
    outfit_img = models.ImageField(
                            upload_to=upload_location_outfit,
                            null=True,
                            blank=True)

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='u')

    # Tagged Clothes <-> outfit_set
    tagged_clothes = models.ManyToManyField(Cloth, blank=True)
    location = models.CharField(max_length=20, blank=True, null=True)
    link = models.CharField(max_length=20, blank=True, null=True)
    only_me = models.BooleanField(default=False)
    # other Related Class
    # Like, Comment, Share,
    objects = OutfitManager()

    def __str__(self):
        return str(self.user)

    def get_categories(self):
        # object lists
        # we want to return array of it.
        # it contains, ?
        return self.categories

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type
