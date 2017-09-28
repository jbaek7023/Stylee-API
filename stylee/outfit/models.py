from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from .utils import GENDER_CHOICES

from cloth.models import Cloth
from comments.models import Comment

def upload_location_outfit(instance, filename):
    ext = filename.split('.')[-1]
    random_number = uuid.uuid4()
    random_number = str(random_number).replace('-', '_')
    firstpart, secondpart = random_number[::2], random_number[1::2]
    return "outfits/%s%s%s.%s" % (firstpart, instance.user.id, secondpart, ext)

# Create your models here.
class Outfit(models.Model):
    # normal post info
    parent = models.ForeignKey("self", blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    content = models.CharField(max_length=30)
    publish = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    outfit_img = models.ImageField(
                            upload_to=upload_location_outfit,
                            null=True,
                            blank=True)

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='u')

    # Tagged Clothes <-> outfit_set
    tagged_clothes = models.ManyToManyField(Cloth, blank=True)
    location = models.CharField(max_length=20, blank=True, null=True)
    # other Related Class
    # Like, Comment, Share,

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


    # is it owner?

    #
    # def is_user_blocked_user(self, user):
    #
    #     return
