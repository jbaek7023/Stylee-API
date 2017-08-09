from rest_framework import serializers

from .models import Profile

class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'bio')
