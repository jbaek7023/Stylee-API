from rest_framework import serializers

from .models import Outfit

from comments.serializers import CommentSerializer
from comments.models import Comment

class OutfitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outfit
        fields = (
            'pk',
            'id',
            'user',
            'content',
            'publish',
            'updated',
            'outfit_img',
            'category',
            'tagged_clothes',
            'location')

class OutfitDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Outfit
        fields = (
            'user',
            'content',
            'publish',
            'updated',
            'outfit_img',
            'category',
            'tagged_clothes',
            'location',
            'comments',
        )


    def get_comments(self, obj):
        content_type = obj.get_content_type
        object_id = obj.id
        comments = Comment.objects.filter_by_instance(obj)
        return CommentSerializer(comments, many=True).data

    # user = user_serializer
    # user = category_serializer
    # tagged_clothes = clothes_serializer
