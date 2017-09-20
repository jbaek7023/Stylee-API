from rest_framework import serializers
from django.db.models import Q

from .models import Outfit

from comments.serializers import CommentSerializer
from comments.models import Comment
from like.models import Like
from profiles.serializers import UserRowSerializer


class OutfitListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Outfit
        fields = (
            'id',
            # 'user',
            'image',
            # 'category',
            # 'tagged_clothes',
            # 'location'
        )

    def get_image(self, obj):
        if obj.outfit_img is not None:
            return obj.outfit_img.url
        return None

from category.serializers import CategorySerializer
from category.models import Category
class OutfitDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    user = UserRowSerializer(read_only=True)

    class Meta:
        model = Outfit
        fields = (
            'id',
            'user',
            'content',
            'publish',
            'updated',
            'outfit_img',
            # 'category',
            'tagged_clothes',
            'location',
            'comments',
            'comment_count',
            'like_count',
            'liked',
            'categories'
        )

    # def get_categories(self, obj):
    #     all_categories = Category.objects.filter(owner=self.context['request'].user)
    #     categories = obj.categories.filter(owner=self.context['request'].user)
    #     return CategorySerializer(categories, many=True).data

    def get_categories(self, obj):
        user = self.context['request'].user
        categories = Category.objects.filter(owner=user)
        add_f = Q(owner=user, outfits__pk__isnull=True)
        add_t = Q(owner=user, outfits__pk=obj.pk)

        pf = add_f | add_t
        categories = categories.filter(pf).values('outfits__pk', 'name', 'id')
        return CategorySerializer(categories, many=True).data

    def get_like_count(self, obj):
        content_type = obj.get_content_type
        object_id = obj.id
        like_count = Like.objects.filter_by_instance(obj).count()
        return like_count

    def get_liked(self, obj):
        content_type = obj.get_content_type
        object_id = obj.id
        # Each serializer object has a context dictionary, which holds the request object by default when initialised.
        # You can pass literally anything from view into serializer context like,
        # YourSerializer(data=data, context={'name':'name'}) and name can be accessed from the serializer object.
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

    # user = user_serializer
    # user = category_serializer
    # tagged_clothes = clothes_serializer

class OutfitDetailCommentSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Outfit
        fields = (
            'comments',
        )

    def get_comments(self, obj):
        content_type = obj.get_content_type
        object_id = obj.id
        comments = Comment.objects.filter_by_instance(obj)
        return CommentSerializer(comments, many=True).data
