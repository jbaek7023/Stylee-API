from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import generics
from .models import Category

from .serializers import OutfitListCategorySerializer, CategoryListSerializer





# Create your views here.
class OutfitCategoryAPIView(generics.RetrieveAPIView):
    # queryset = Outfit.objects.all()
    serializer_class = OutfitListCategorySerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = Category.objects.all(owner=self.request.user)
        return qs

class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategoryListSerializer

    def get_queryset(self):
        qs = Category.objects.all(user=self.request.user)
        qs = qs.filter(owner=self.request.user)
        return qs

class CategoryListForIdAPIView(generics.ListAPIView):
    serializer_class = CategoryListSerializer
    # permission

    def get_queryset(self):
        uid = self.kwargs['user_id']
        User = get_user_model()
        category_owner = User.objects.filter(id=uid).first()
        qs = Category.objects.all(user=self.request.user)
        qs = qs.filter(owner=category_owner)
        return qs
