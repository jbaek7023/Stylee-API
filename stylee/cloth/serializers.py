from rest_framework import serializers

from .models import Cloth
from profiles.serializers import UserRowSerializer


class ClothesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cloth
        fields = ('cloth_image', 'id')

# In Progress..!!
class ClothDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cloth
        fields = ('cloth_image', 'id')
