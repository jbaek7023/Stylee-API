from django.db import models
from django.conf import settings

CLOTHES_CHOICES = (
    ts : 't-shirt',
    ct : 'coat',

)

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

# Create your models here.
class Cloth(models.Model):
    owner           = models.ForeignKey(settings.AUTH_USER_MODEL)
    image = models.ImageField(upload_to=upload_location,
                                null=True,
                                blank=True,
                                width_field=1080,
                                height_field=1080)
    name            = models.CharField(max_length=20)
    color           = models.CharField(max_length=10)
    cloth_type      = models.ForeignKey(Type)
    size            = models.CharField(max_length=3) #XXXS, XXS, XS, S, M, L, XL, XXL, XXXL
    # http://www.asos.com/men/t-shirts-and-polo-shirts-size-guide/?szgid=16&r=2
    create_date     = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_date    = models.DateTimeField(auto_now=True, auto_now_add=False)
    # worn_date       = models.DateTimeField(auto_now=True, auto_now_add=False)
    link            = models.CharField(require=False)

    def __str__(self):
        return str(self.user)

# This model will be very useful when we implement the Diary and statistics
class Wear(models.Model):
    who = models.ForeignKey()
    which = models.ForeignKey()
    date = models.DateTimeField(auto_now=True, auto_now_add=False)

# Wear.filter(user = user.getUser)

class Type(models.Model):
    name = models.CharField(max_length=9, choices=CLOTHES_CHOICES, default='1')

# user.clothes.filter('top')
# cloth.filter('button')
# cloth.filter('second')
