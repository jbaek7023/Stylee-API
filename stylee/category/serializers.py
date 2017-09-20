from rest_framework import serializers

from .models import Category
from outfit.serializers import OutfitListSerializer

class CategorySerializer(serializers.ModelSerializer):
    added = serializers.BooleanField(source='outfits__pk')

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'added'
        )

class OutfitListCategorySerializer(serializers.ModelSerializer):
    outfits = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'outfits'
            # 'image',
        )

    def get_outfits(self, obj):
        if obj.outfits is not None:
            return OutfitListSerializer(obj.outfits, many=True).data
        return None
