from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'content_type',
            'object_id',
            'content',
            'publish',
            'updated',
            'parent',
            'reply_count',
        )

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'content_type',
            'object_id',
            'content',
            'publish',
            'updated',
        )

class CommentDetailSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'content_type',
            'object_id',
            'content',
            'publish',
            'updated',
            'replies',
        )

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None
