from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from profiles.serializers import UserRowSerializer

from .models import Comment

User = get_user_model()

# content, user
def create_comment_serializer(model_type='outfit', id=None, parent_id=None, user=None):
    class CommentCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model=Comment
            fields = [
                'id',
                # 'user',
                # 'content_type',
                # 'object_id',
                'content',
                'publish',
                'updated',
                'parent',
            ]
        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.id = id
            self.parent_obj = None

            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() ==1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type # coming from __init__
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise serializers.ValidationError("This is not a valid content type")
            SomeModel = model_qs.first().model_class()

            obj_qs = SomeModel.objects.filter(id=self.id)
            # obj_qs = Post.objects.filter(pk=self.pk)
            if not obj_qs.exists() or obj_qs.count() !=1:
                raise serializers.ValidationError("This is not a id for this content type")
            return data

        def create(self, validated_data):
            content = validated_data.get("content")
            if user:
                main_user = user
            else:
                main_user = User.objects.all().first()
            model_type = self.model_type
            id = self.id
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(
                model_type=model_type,
                id=id,
                user=main_user, # main_user itseslf?
                content=content,
                parent_obj=parent_obj,
            )
            return comment

    return CommentCreateSerializer

class CommentSerializer(serializers.ModelSerializer):
    reply_count = serializers.SerializerMethodField()
    user = UserRowSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            # 'content_type',
            # 'object_id',
            'content',
            'publish',
            'updated',
            # 'parent',
            'reply_count',
        )

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

class CommentsOnPostSerializer(serializers.ModelSerializer):
    reply_count = serializers.SerializerMethodField()
    user = UserRowSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'content',
            'publish',
            'updated',
            'reply_count',
        )

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentChildSerializer(serializers.ModelSerializer):
    user = UserRowSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'content',
            'publish',
            'updated',
        )

class CommentDetailSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user = UserRowSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'content',
            'publish',
            'updated',
            'replies',
        )
        read_only_fields = (
        )

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

class CommentEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id',
            'content',
            'publish',
            'updated',
        )
