from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from outfit.models import Outfit

def upload_location_category(instance, filename):
    ext = filename.split('.')[-1]
    random_number = uuid.uuid4()
    return "category/%s.%s" % (random_number, ext)

class CategoryManager(models.Manager):
    def all(self, user=None, request=None, *args, **kwargs):
        qs = super(CategoryManager, self).all()
        # owned by user
        if user: #user logged in
            qs = qs.exclude(Q(only_me=True) & ~Q(owner=user))
            # qs = qs.exclude(~Q(owner=user))
        return qs

class Category(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    outfits = models.ManyToManyField(Outfit, related_name="categories", blank=True)
    main_img = models.ImageField(
                            upload_to=upload_location_category,
                            null=True,
                            blank=True)
    detail = models.CharField(max_length=50, blank=True, null=True)
    only_me = models.BooleanField(default=False)

    objects = CategoryManager()

    def __str__(self):
        if(self.owner):
            uname = self.owner.username
        else:
            uname = None
        return '{} : {}'.format(uname, self.name)
