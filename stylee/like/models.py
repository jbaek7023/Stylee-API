from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from stream_django.activity import Activity
from stream_django.feed_manager import feed_manager

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
class Like(models.Model, Activity):
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

    @property
    def activity_object_attr(self):
        return self

    @property
    def activity_author_feed(self):
        return 'Like'

    @property
    def activity_target_attr(self):
        print('tgarget')
        print('tgarget')
        print('tgarget')
        print('tgarget')
        SomeModel = self.content_type.model_class()
        object_id = self.object_id
        qs = SomeModel.objects.filter(id=self.object_id)
        if qs.exists():
            target_instance = SomeModel.objects.filter(id=self.object_id).first()
            if target_instance:
                print('yeah!')
                print(target_instance)
                return target_instance
        return None

    @property
    def activity_notify(self):
        # get liked object
        # content_type, object_id
        SomeModel = self.content_type.model_class()
        object_id = self.object_id
        qs = SomeModel.objects.filter(id=self.object_id)
        if qs.exists():
            target_instance = SomeModel.objects.filter(id=self.object_id).first()
            if target_instance:
                user_object = target_instance.user
                if user_object:
                    user_id = user_object.id
                    author_id = self.user.id
                    if user_id != author_id:
                        target_feed = feed_manager.get_notification_feed(user_id)
                        return [target_feed]
        return []
