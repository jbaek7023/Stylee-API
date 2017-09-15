from django.db import models
from cloth.models import Cloth
from django.conf import settings

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
    return "%s/%s" % (new_id, filename)
    # return outfits/owner_id/new_id.png
    # return ""%s/%s" % (new_id, filename)"

# Create your models here.
class Outfit(models.Model):
    # normal post info
    parent = models.ForeignKey("self", blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    content = models.CharField(max_length=30)
    publish = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    outfit_img = models.ImageField(
                            upload_to=upload_location,
                            null=True,
                            blank=True,
                            width_field=1080,
                            height_field=1080)


    # This can be MANY categories. ManyToManyField
    category = models.CharField(max_length=20)

    # Tagged Clothes <-> outfit_set
    tagged_clothes = models.ManyToManyField(Cloth, blank=True)
    location = models.CharField(max_length=20)
    # other Related Class
    # Like, Comment, Share,

    def __str__(self):
        return str(self.user)

    # is it owner?

    #
    # def is_user_blocked_user(self, user):
    #
    #     return
#
# class LikeOutfit(models.Model):
#     who = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="liked_outfits")
#     which = models.ForeignKey(Outfit)
