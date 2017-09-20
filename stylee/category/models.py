from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType


from outfit.models import Outfit

def upload_location_category(instance, filename):
    PostModel = instance.__class__
    new_id = PostModel.objects.order_by("id").last().id + 1
    ext = filename.split('.')[-1]
    return "category/%s/%s.%s" % (instance.user.id, new_id, ext)

class Category(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    outfits = models.ManyToManyField(Outfit, related_name="categories", blank=True)
    main_img = models.ImageField(
                            upload_to=upload_location_category,
                            null=True,
                            blank=True)
    detail = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        if(self.owner):
            uname = self.owner.username
        else:
            uname = None
        return '{} : {}'.format(uname, self.name)
