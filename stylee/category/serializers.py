from rest_framework import serializers

from .models import Category
from outfit.serializers import OutfitListSerializer
from profiles.serializers import UserRowSerializer

class CategoryEditSerializer(serializers.ModelSerializer):
    owner = UserRowSerializer(read_only=True)

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'owner',
            'only_me',
        )

class CategoryDetailSerializer(serializers.ModelSerializer):
    outfits = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    owner = UserRowSerializer(read_only=True)
    outfit_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'owner',
            'is_owner',
            'outfits',
            'outfit_count',
            'only_me',
            'detail',
        )

    def get_outfits(self, obj):
        page = self.context['request'].query_params["page"]
        page_num_before = 0
        page_num = 18
        if page:
            page_num_before = (int(page)-1) * 18 # page 1 -> 0: 24
            page_num = int(page) * 18

        if obj.outfits is not None:
            outfits = obj.outfits
            if obj.owner != self.context['request'].user:
                outfits = outfits.filter(only_me=False)
            return OutfitListSerializer(outfits.all()[page_num_before:page_num], many=True, context=self.context).data
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
            if obj.outfits.first().outfit_img:
                request = self.context.get('request')
                return request.build_absolute_uri(obj.outfits.first().outfit_img.url)
            return None
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
