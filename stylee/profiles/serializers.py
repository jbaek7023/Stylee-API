from rest_framework import serializers

from .models import Profile
from django.contrib.auth import get_user_model


User = get_user_model()


class UserRowSerializer(serializers.ModelSerializer):
    # user = UserAccountSerializer(read_only=True)
    image = serializers.SerializerMethodField()
    # user_id = serializers.SerializerMethodField()
    # username = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('image', 'id', 'username', 'name')

    def get_image(self, obj):
        try:
            image = obj.profile.profile_img.url
        except:
            image = None
        return image

    def get_name(self, obj):
        try:
            name = obj.profile.name
        except:
            name = None
        return name

class UserMenuSerializer(serializers.ModelSerializer):
    user = UserRowSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('user',)

class UserEmailSerizlier(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

class UserUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

# User Account Edit Retrieve
class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',)

# User Profile Edit
class ProfileRetrieveAndUpdateSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'title',
            'gender',
            # 'birth',
            # 'height',
            # 'height_in_ft',
            'profile_img',
            'username',
        )

    def get_username(self, obj):
        return obj.user.username

# Image Update
class ProfileUpdateProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('profile_img',)

class ProfileEditSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'title',
            'gender',
            # 'birth',
            # 'height',
            # 'height_in_ft',
            'profile_img',
            'username',
        )

    def get_username(self, obj):
        return obj.user.username

from outfit.serializers import OutfitDetailFeedSerializer
from outfit.serializers import OutfitListSerializer
class ProfilePageSerializer(serializers.ModelSerializer):
    outfit_count = serializers.SerializerMethodField()
    followed_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    category_count = serializers.SerializerMethodField()
    clothes_count = serializers.SerializerMethodField()
    outfits = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'image',
            'outfit_count',
            'followed_count',
            'following_count',
            'title',
            'category_count',
            'clothes_count',
            'outfits',
            'is_owner',
            'is_following',
        )

    def get_image(self, obj):
        if(obj.profile.profile_img):
            return obj.profile.profile_img.url
        return None

    def get_title(self, obj):
        if(obj.profile):
            return obj.profile.title
        return ""

    def get_outfit_count(self, obj):
        if(obj.outfit_set):
            return obj.outfit_set.count()
        return 0

    def get_followed_count(self, obj):
        if(obj.follower):
            return obj.follower.count()
        return 0

    def get_following_count(self, obj):
        if(obj.following):
            return obj.following.count()
        return 0

    def get_category_count(self, obj):
        if(obj.category_set):
            return obj.category_set.count()
        return 0

    def get_clothes_count(self, obj):
        if(obj.cloth_set):
            return obj.cloth_set.count()
        return 0

    def get_outfits(self, obj):
        if(obj.outfit_set):
            outfits = obj.outfit_set.all()
            if obj != self.context['request'].user:
                outfits = outfits.filter(only_me=False)
            return OutfitDetailFeedSerializer(outfits.all()[:12], many=True, context={'request': self.context['request']}).data
        return {}

    def get_is_owner(self, obj):
        return obj == self.context['request'].user

    def get_is_following(self, obj):
        return obj.following.filter(user=self.context['request'].user).exists()
