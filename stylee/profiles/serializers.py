from rest_framework import serializers

from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileDetailSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('username', 'bio', 'user_id', 'gender', 'location', 'birth')

    def get_username(self, obj):
        return obj.user.username

class UserRowSerializer(serializers.ModelSerializer):
    # user = UserAccountSerializer(read_only=True)
    image = serializers.SerializerMethodField()
    # user_id = serializers.SerializerMethodField()
    # username = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('image', 'id', 'username')

    def get_image(self, obj):
        try:
            image = obj.profile.profile_img.url
        except:
            image = None
        return image


class UserEmailSerizlier(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

class ProfileRetrieveAndUpdateSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('username', 'bio', 'gender','location', 'birth')

    def get_username(self, obj):
        return obj.user.username
