from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView

from .models import Star

from .serializers import create_star_serializer, ListStarSerializer

class StarCreateAPIView(generics.CreateAPIView):
    queryset = Star.objects.all()

    def get_serializer_class(self):
        model_type = self.request.GET.get("type")
        id = self.request.GET.get("id")
        return create_star_serializer(
            model_type=model_type,
            id=id,
            user=self.request.user
        )

class StarListAPIView(generics.ListAPIView):
    serializer_class = ListStarSerializer

    def get_queryset(self):
        qs = Star.objects.filter(user=self.request.user)
        return qs


    # Outfit.outfit_img
    # Outfit.id
    #
    # Cloth.cloth_img
