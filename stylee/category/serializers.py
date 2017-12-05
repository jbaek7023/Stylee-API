from rest_framework import serializers

from .models import Category
from outfit.serializers import OutfitListSerializer
from profiles.serializers import UserRowSerializer



class CategoryDetailSerializer(serializers.ModelSerializer):
    outfits = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    owner = UserRowSerializer(read_only=True)
    outfit_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'name',
            'owner',
            'is_owner',
            'outfits',
            'outfit_count',
            'only_me',
            'detail',
        )

    def get_outfits(self, obj):
        if obj.outfits is not None:
            return OutfitListSerializer(obj.outfits, many=True).data
        return None

    def get_outfit_count(self, obj):
        if obj.outfits is not None:
            return obj.outfits.count()

    def get_is_owner(self, obj):
        if(obj.owner):
            return obj.owner == self.context['request'].user
        return False

class CategoryListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    length = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'image',
            'only_me',
            'length',
        )

    def get_image(self, obj):
        if obj.outfits.first() is not None:
            return obj.outfits.first().outfit_img.url
        else:
            return None

    def get_length(self, obj):
        return obj.outfits.count()

class CategorySimpleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'only_me',
        )

class CategorySerializer(serializers.ModelSerializer):
    # added = serializers.BooleanField(source='outfits__pk')
    added = serializers.BooleanField()
    class Meta:
        model = Category
        fields = (
            'only_me',
            'id',
            'name',
            'added',
        )
