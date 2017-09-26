from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType


from outfit.models import Outfit

def upload_location_category(instance, filename):
    print(instance);
    print(instance.id);
    # instance.id is bad!
    ext = filename.split('.')[-1]
    return "category/%s/%s.%s" % (instance.owner.id, instance.id, ext)

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
