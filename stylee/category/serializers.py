from rest_framework import serializers

from .models import Category
from outfit.serializers import OutfitListSerializer

class CategorySerializer(serializers.ModelSerializer):
    # added = serializers.BooleanField(source='outfits__pk')
    added = serializers.BooleanField()
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'added'
        )

class OutfitListCategorySerializer(serializers.ModelSerializer):
    outfits = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'is_owner',
            'outfits',
        )

    def get_outfits(self, obj):
        if obj.outfits is not None:
            return OutfitListSerializer(obj.outfits, many=True).data
        return None

    def get_is_owner(self, obj):
        if(obj.owner):
            return obj.owner == self.context['request'].user
        return False

class CategoryListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'image',
            'only_me',
        )

    def get_image(self, obj):
        if obj.main_img:
            return obj.main_img.url
        return None
