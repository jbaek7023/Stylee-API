from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class LikeManager(models.Manager):
    def filter_by_instance(self, instance):
        # content_type = ContentType.objects.get_for_model(Outfit)
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(LikeManager, self).filter(content_type=content_type, object_id=obj_id)
        # comments = Comment.objects.filter(content_type=content_type, object_id=obj_id)
        return qs

    # def create_by_model_type(self, model_type, id, user, parent_obj=None):
    #     model_qs = ContentType.objects.filter(model=model_type)
    #     if model_qs.exists():
    #         SomeModel = model_qs.first().model_class()
    #         obj_qs = SomeModel.objects.filter(id=id)
    #
    #         if obj_qs.exists() and obj_qs.count() ==1:
    #             instance, created = Like.objects.get_or_create(
    #                 user=user,
    #                 content_type=model_qs.first(),
    #                 object_id=obj_qs.first().id
    #                 )
    #             if created:
    #                 return instance
    #             else:
    #                 # instance.delete()
    #                 empty_instance = self.model()
    #                 return empty_instance
    #     return None
    #
    # def delete_by_model_type(self, model_type, id, user, parent_obj=None):
    #     model_qs = ContentType.objects.filter(model=model_type)
    #     if model_qs.exists():
    #         SomeModel = model_qs.first().model_class()
    #         obj_qs = SomeModel.objects.filter(id=id)
    #
    #         if obj_qs.exists() and obj_qs.count() == 1:
    #             like_obj = Like.objects.filter(user=user, content_type=model_qs.first(), object_id=obj_qs.first().id).first()
    #             if like_obj is not None:
    #                 like_obj.delete()
    #                 empty_instance = self.model()
    #                 return empty_instance
    #             else:
    #                 return empty_instance
    #     return None


# Create your models here.
# Create your models here.
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = LikeManager()

    def __str__(self):
        if self.user.username==None:
            return 'None'
        return self.user.username

# Who liked this posts
# [{user_obj}, {user}, {user}, ]
# user_obj = user_id, user_profile_img
