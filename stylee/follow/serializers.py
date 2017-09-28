from rest_framework import serializers

from .models import Follow

class FollowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ()
