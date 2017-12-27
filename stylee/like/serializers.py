from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from profiles.serializers import UserRowSerializer

from .models import Like

# def create_like_serializer(model_type='outfit', id=None, user=None):
#     class LikeCreateSerializer(serializers.ModelSerializer):
#         class Meta:
#             model=Like
#             fields = [
#                 'user',
#                 'created_at',
#             ]
#         def __init__(self, *args, **kwargs):
#             self.model_type = model_type
#             self.id = id
#
#             # Maybe we can delete rather than create here?
#             return super(LikeCreateSerializer, self).__init__(*args, **kwargs)
#
#         def validate(self, data):
#             model_type = self.model_type # coming from __init__
#             model_qs = ContentType.objects.filter(model=model_type)
#             if not model_qs.exists() or model_qs.count() != 1:
#                 raise serializers.ValidationError("This is not a valid content type")
#             SomeModel = model_qs.first().model_class()
#
#             obj_qs = SomeModel.objects.filter(id=self.id)
#             # obj_qs = Post.objects.filter(pk=self.pk)
#             if not obj_qs.exists() or obj_qs.count() !=1:
#                 raise serializers.ValidationError("This is not a id for this content type")
#             return data
#
#         def create(self, validated_data):
#             if user:
#                 main_user = user
#             else:
#                 # admin
#                 main_user = User.objects.all().first()
#             model_type = self.model_type
#             id = self.id
#
#             like = Like.objects.create_by_model_type(
#                 model_type=model_type,
#                 id=id,
#                 user=main_user, # main_user itseslf?
#             )
#             return like
#
#     return LikeCreateSerializer
#
# def delete_like_serializer(model_type='outfit', id=None, user=None):
#     class LikeDestroySerializer(serializers.ModelSerializer):
#         class Meta:
#             model=Like
#             fields = [
#                 'user',
#                 'created_at',
#             ]
#         def __init__(self, *args, **kwargs):
#             self.model_type = model_type
#             self.id = id
#
#             # Maybe we can delete rather than create here?
#             return super(LikeDestroySerializer, self).__init__(*args, **kwargs)
#
#         def validate(self, data):
#             model_type = self.model_type # coming from __init__
#             model_qs = ContentType.objects.filter(model=model_type)
#             if not model_qs.exists() or model_qs.count() != 1:
#                 raise serializers.ValidationError("This is not a valid content type")
#             SomeModel = model_qs.first().model_class()
#
#             obj_qs = SomeModel.objects.filter(id=self.id)
#             # obj_qs = Post.objects.filter(pk=self.pk)
#             if not obj_qs.exists() or obj_qs.count() !=1:
#                 raise serializers.ValidationError("This is not a id for this content type")
#             return data
#
#         def destroy(self, validated_data):
#             if user:
#                 main_user = user
#             else:
#                 # admin
#                 main_user = User.objects.all().first()
#             model_type = self.model_type
#             id = self.id
#
#             like = Like.objects.delete_by_model_type(
#                 model_type=model_type,
#                 id=id,
#                 user=main_user, # main_user itseslf?
#             )
#             return like
#     return LikeCreateSerializer

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            'id',
            'user',
            'created_at'
        )

class LikedUserSerializer(serializers.ModelSerializer):
    user = UserRowSerializer(read_only=True)
    class Meta:
        model = Like
        fields = (
            'id',
            'user',
        )

class LikeListSerializer(serializers.ModelSerializer):
    user = UserRowSerializer(read_only=True)
    class Meta:
        model = Like
        fields = (
            'user',
        )
