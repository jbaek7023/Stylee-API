from rest_framework import serializers

from .models import Follow
from profiles.serializers import UserRowSerializer

class FollowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ()

class FollowingUserSerializer(serializers.ModelSerializer):
    user = UserRowSerializer(read_only=True)
    class Meta:
        model = Follow
        fields = (
            'id',
            'user',
        )

class FollowerUserSerializer(serializers.ModelSerializer):
    target = UserRowSerializer(read_only=True)
    class Meta:
        model = Follow
        fields = (
            'id',
            'target',
        )
