from rest_framework import serializers

from .models import Cloth, ClothDetail
from comments.models import Comment
from like.models import Like

from comments.serializers import CommentSerializer
from profiles.serializers import UserRowSerializer
from like.serializers import LikeListSerializer

class ClothesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cloth
        fields = ('cloth_image', 'id')

class ClothDetailDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothDetail
        fields = (
            'publish',
            'updated',
            'color',
            'brand',
            'size',
            'sex',
            'seasons',
            'delivery_loc',
            'link',
            'detail')

# In Progress..!!
class ClothDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()

    user = UserRowSerializer(read_only=True)

    detail = serializers.SerializerMethodField()
    class Meta:
        model = Cloth
        fields = (
            'id',
            'user',
            'content',
            'cloth_type',
            'cloth_image',
            'in_wardrobe',
            'detail',
            'comments',
            'comment_count',
            'like_count',
            'liked')

    def get_like_count(self, obj):
        content_type = obj.get_content_type
        object_id = obj.id
        like_count = Like.objects.filter_by_instance(obj).count()
        return like_count

    def get_liked(self, obj):
        content_type = obj.get_content_type
        object_id = obj.id
        user = self.context['request'].user
        my_like = Like.objects.filter_by_instance(obj).filter(user=user)
        if my_like.count() == 0:
            return False
        return True

    def get_comments(self, obj):
        content_type = obj.get_content_type
        object_id = obj.id
        comments = Comment.objects.filter_by_instance(obj)[:2]
        return CommentSerializer(comments, many=True).data

    def get_comment_count(self, obj):
        content_type = obj.get_content_type
        object_id = obj.id
        comments_count = Comment.objects.filter_by_instance(obj).count()
        comments_count = comments_count - 2
        return comments_count

    def get_detail(self, obj):
        cloth_detail = obj.c_detail
        return ClothDetailDetailSerializer(cloth_detail).data

class ClothDetailCommentSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Cloth
        fields = (
            'comments',
        )

    def get_comments(self, obj):
        content_type = obj.get_content_type
        object_id = obj.id
        comments = Comment.objects.filter_by_instance(obj)
        return CommentSerializer(comments, many=True).data

class ClothDetailLikeSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Cloth
        fields = (
            'likes',
        )

    def get_likes(self, obj):
        content_type = obj.get_content_type
        object_id = obj.id
        likes = Like.objects.filter_by_instance(obj)
        return LikeListSerializer(likes, many=True).data
