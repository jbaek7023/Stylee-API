from rest_framework import serializers

from .models import Outfit


class OutfitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outfit
        fields = (
            'user',
            'content',
            'publish',
            'updated',
            'outfit_img',
            'category',
            'tagged_clothes',
            'location')
