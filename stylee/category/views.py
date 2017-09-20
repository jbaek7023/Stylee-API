from django.shortcuts import render

from rest_framework import generics
from .models import Category

from .serializers import OutfitListCategorySerializer

# Create your views here.
class OutfitCategoryAPIView(generics.RetrieveAPIView):
    # queryset = Outfit.objects.all()
    serializer_class = OutfitListCategorySerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = Category.objects.all()
        return qs
