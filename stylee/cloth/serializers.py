from rest_framework import serializers

from .models import Cloth

class ClothesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cloth
        fields = ('user', 'name', 'publish', 'updated', 'color', 'cloth_type', 'cloth_image', 'size', 'link')
