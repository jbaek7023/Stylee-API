from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType


from cloth.models import Cloth
from comments.models import Comment

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
    return "outfits/%s/%s.%s" % (instance.user.id, new_id, ext)

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
                            blank=True)
    # This can be MANY categories. ManyToManyField <-..!

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
        return self.category

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

class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    name = models.CharField(max_length=20)
    outfits = models.ManyToManyField(Outfit, related_name="categories")

    def __str__(self):
        return str(self.name)

#
# class LikeOutfit(models.Model):
#     who = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="liked_outfits")
#     which = models.ForeignKey(Outfit)
