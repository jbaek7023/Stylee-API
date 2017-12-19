from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from cloth.serializers import ClothStarSerializer
from outfit.serializers import OutfitStarSerializer

from .models import Star

# def create_star_serializer(model_type='outfit', id=None, user=None):
#     class StarCreateSerializer(serializers.ModelSerializer):
#         class Meta:
#             model=Star
#             fields = [
#                 'user',
#             ]
#         def __init__(self, *args, **kwargs):
#             self.model_type = model_type
#             self.id = id
#
#             # Maybe we can delete rather than create here?
#             return super(StarCreateSerializer, self).__init__(*args, **kwargs)
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
#             star = Star.objects.create_by_model_type(
#                 model_type=model_type,
#                 id=id,
#                 user=main_user, # main_user itseslf?
#             )
#             return star
#     return StarCreateSerializer

class ListStarSerializer(serializers.ModelSerializer):
    mobject = serializers.SerializerMethodField()

    class Meta:
        model = Star
        fields = ('user', 'mobject', 'content_type', 'object_id')

    def get_mobject(self, obj):
        if obj.content_type_id == 26:
            serializer = OutfitStarSerializer(obj.target)
        elif obj.content_type_id == 15:
            serializer = ClothStarSerializer(obj.target)
        else:
            return {}

        return serializer.data
