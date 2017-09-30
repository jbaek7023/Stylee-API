from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin

from rest_framework import generics
from .models import Category

from .serializers import CategoryDetailSerializer, CategoryListSerializer





# Create your views here.
class OutfitCategoryAPIView(generics.RetrieveAPIView):
    # queryset = Outfit.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = Category.objects.all(owner=self.request.user)
        return qs

class CategoryEditAPIView(DestroyModelMixin, UpdateModelMixin, generics.RetrieveAPIView):
    serializer_class = CategoryDetailSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = Category.objects.all(owner=self.request.user)
        return qs

    def put(self, request, *args, **kwargs):
        # Raise 404 if user has self.request.user != Category(obj_.id).owner
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

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
