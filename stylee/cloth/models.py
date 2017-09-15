from django.db import models
from django.conf import settings

from .utils import CLOTHES_CHOICES

def upload_location(instance, filename):
    #filebase, extension = filename.split(".")
    #return "%s/%s.%s" %(instance.id, instance.id, extension)
    PostModel = instance.__class__
    new_id = PostModel.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object,
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    ext = filename.split('.')[-1]
    # user id, cloth id, extension
    return "clothes/%s/%s.%s" % (instance.user.id, new_id, ext)

# Create your models here.
class Cloth(models.Model):
    # normal post info
    parent = models.ForeignKey("self", blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    name = models.CharField(max_length=20)
    publish = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    color = models.CharField(max_length=10)
    cloth_type = models.CharField(max_length=9, choices=CLOTHES_CHOICES, default='1')

    # img up to width of 1080px.
    # if shared a photo at a lower resolution, we enlarge it to a width of 320 pixels
    # photo at a higher resolution, we size it DOWN to 1080 pixels
    cloth_image = models.ImageField(upload_to=upload_location,
                                null=True,
                                blank=True)
    size = models.CharField(max_length=3) #XXXS, XXS, XS, S, M, L, XL, XXL, XXXL
    # http://www.asos.com/men/t-shirts-and-polo-shirts-size-guide/?szgid=16&r=2
    # worn_date       = models.DateTimeField(auto_now=True, auto_now_add=False)
    link = models.CharField(max_length=20)


    def __str__(self):
        return str(self.user)

# This model will be very useful when we implement the Diary and statistics
class Wear(models.Model):
    who = models.ForeignKey(settings.AUTH_USER_MODEL)
    which = models.ForeignKey(Cloth)
    date = models.DateTimeField(auto_now=True, auto_now_add=False)
