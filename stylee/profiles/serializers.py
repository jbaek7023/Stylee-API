from rest_framework import serializers

from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('username', 'bio')

class UserEmailSerizlier(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)
