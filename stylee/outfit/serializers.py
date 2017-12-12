from rest_framework import serializers
from django.db.models import Q
from django.db.models import Case, When
from .models import Outfit
# from cloth.models import Cloth

from comments.models import Comment
from like.models import Like
from star.models import Star
from category.models import Category

class OutfitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outfit
        fields = (
            'id',
            # 'user',
            'outfit_img',
            # 'category',
            # 'tagged_clothes',
            # 'location',
            'only_me'
        )

class OutfitStarSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Outfit
        fields = ('image',)

    def get_image(self, obj):
        if obj.outfit_img:
            return str(obj.outfit_img.url)
        return None

class OutfitCreateSerializer(serializers.ModelSerializer):
    outfit_img = serializers.ImageField(
        max_length=None,
        required=False,
        allow_empty_file=True,
        use_url=True)

    class Meta:
        model = Outfit
        fields = (
            'outfit_img',
            'content',
            'gender',
            'tagged_clothes',
            'location',
            'link',
            'only_me')

from comments.serializers import CommentSerializer
from cloth.serializers import ClothesListSerializer
from like.serializers import LikeListSerializer
from category.serializers import CategorySerializer, CategorySimpleListSerializer
from profiles.serializers import UserRowSerializer
class OutfitDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    user = UserRowSerializer(read_only=True)
    tagged_clothes = serializers.SerializerMethodField()
    starred = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Outfit
        fields = (
            'id',
            'user',
            'content',
            'gender',
            'created_at',
            'outfit_img',
            # 'category',
            'tagged_clothes',
            'location',
            'comments',
            'comment_count',
            'like_count',
            'liked',
            'categories',
            'starred',
            'only_me',
            'is_owner',
            'is_following',
        )

    def get_tagged_clothes(self, obj):
        clothes = obj.tagged_clothes
        return ClothesListSerializer(clothes, many=True).data

    def get_categories(self, obj):
        user = self.context['request'].user
        categories = Category.objects.filter(owner=user)
        added = categories.extra(select={'added': '1'}).filter(outfits__pk=obj.pk)
        added = list(added.values('added', 'name', 'id'))
        added_f = categories.extra(select={'added': '0'}).exclude(outfits__pk=obj.pk)
        added_f = list(added_f.values('added', 'name', 'id'))
        categories = added + added_f
        return CategorySerializer(categories, many=True).data

    def get_starred(self, obj):
        content_type = obj.get_content_type
        object_id = obj.id
        user = self.context['request'].user
        my_star = Star.objects.filter_by_instance(obj).filter(user=user)
        if my_star.count() == 0:
            return False
        return True

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
        comments_count = comments_count
        return comments_count

    def get_is_owner(self, obj):
        if(obj.user):
            return obj.user == self.context['request'].user
        return False

    def get_is_following(self, obj):
        return obj.user.target.filter(user=self.context['request'].user).exists()

class CategoryListOnOutfitSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Outfit
        fields = (
            'id',
            'categories',
        )

    #Field name.. declare here too
    def get_categories(self, obj):
        user = self.context['request'].user
        categories = Category.objects.filter(owner=user)
        added = categories.extra(select={'added': '1'}).filter(outfits__pk=obj.pk)
        added = list(added.values('added', 'name', 'id', 'only_me'))
        added_f = categories.extra(select={'added': '0'}).exclude(outfits__pk=obj.pk)
        added_f = list(added_f.values('added', 'name', 'id', 'only_me'))
        categories = added + added_f
        return CategorySerializer(categories, many=True).data
        # return CategorySerializer(categories, many=True).data

class OutfitDetailFeedSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    user = UserRowSerializer(read_only=True)
    starred = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Outfit
        fields = (
            'id',
            'user',
            'content',
            'created_at',
            'outfit_img',
            'comments',
            'comment_count',
            'like_count',
            'liked',
            'starred',
            'only_me',
            'is_owner',

        )

    # def get_categories(self, obj):
    #     all_categories = Category.objects.filter(owner=self.context['request'].user)
    #     categories = obj.categories.filter(owner=self.context['request'].user)
    #     return CategorySerializer(categories, many=True).data

    def get_starred(self, obj):
        content_type = obj.get_content_type
        object_id = obj.id
        user = self.context['request'].user
        my_star = Star.objects.filter_by_instance(obj).filter(user=user)
        if my_star.count() == 0:
            return False
        return True

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
        comments_count = comments_count
        return comments_count

    def get_is_owner(self, obj):
        if(obj.user):
            return obj.user == self.context['request'].user
        return False

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

class OutfitDetailLikeSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Outfit
        fields = (
            'likes',
        )

    def get_likes(self, obj):
        content_type = obj.get_content_type
        object_id = obj.id
        likes = Like.objects.filter_by_instance(obj)
        return LikeListSerializer(likes, many=True).data
