from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import Category
from outfit.models import Outfit

from .serializers import (
    CategoryDetailSerializer,
    CategoryListSerializer,
    CategorySimpleListSerializer
)

# Create your views here.
class OutfitCategoryAPIView(generics.RetrieveAPIView):
    # queryset = Outfit.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = Category.objects.all(owner=self.request.user)
        return qs

class CreateCategoryView(APIView):
    def post(self, request, format=None):
        outfit_id = self.request.data.get('outfit_id')
        print(outfit_id)
        if outfit_id == 0:
            print('passing as expected')
            name = self.request.data.get('name')
            only_me = self.request.data.get('only_me')
            category_instance, created = Category.objects.get_or_create(
                owner=self.request.user,
                name=name,
                only_me=only_me)
            if category_instance is not None:
                json_output = {"success": True, "name": category_instance.name, "id": category_instance.id }
                return Response(json_output, status.HTTP_201_CREATED)
            else:
                json_output = {"success": False}
                return Response(json_output, HTTP_409_CONFLICT)
        else:
            outfit_instance = Outfit.objects.filter(id=outfit_id).first()
            if outfit_instance is not None:
                name = self.request.data.get('name')
                only_me = self.request.data.get('only_me')
                category_instance, created = Category.objects.get_or_create(
                    owner=self.request.user,
                    name=name,
                    only_me=only_me)
                if category_instance is not None:
                    category_instance.outfits.add(outfit_instance)
                    print(category_instance.main_img)
                    print(outfit_instance.outfit_img)
                    if category_instance.main_img is None:
                        print('imhere')

                    category_instance.main_img = outfit_instance.outfit_img
                    json_output = {"success": True, "name": category_instance.name }
                    return Response(json_output, status.HTTP_201_CREATED)
                else:
                    json_output = {"success": False}
                    return Response(json_output, HTTP_409_CONFLICT)
            else:
                json_output = {"success": False}
                return Response(json_output, HTTP_409_CONFLICT)

class CreateSimpleCategoryView(APIView):
    def post(self, request, format=None):
        if outfit_instance is not None:
            name = self.request.data.get('name')
            only_me = self.request.data.get('only_me')
            category_instance, created = Category.objects.get_or_create(
                owner=self.request.user,
                name=name,
                only_me=only_me)
            if category_instance is not None:
                category_instance.outfits.add(outfit_instance)
                print(category_instance.main_img)
                print(outfit_instance.outfit_img)
                if category_instance.main_img is None:
                    print('imhere')

                category_instance.main_img = outfit_instance.outfit_img
                json_output = {"success": True, "name": category_instance.name }
                return Response(json_output, status.HTTP_201_CREATED)
            else:
                json_output = {"success": False}
                return Response(json_output, HTTP_409_CONFLICT)
        else:
            json_output = {"success": False}
            return Response(json_output, HTTP_409_CONFLICT)


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

class CategorySimpleListAPIView(generics.ListAPIView):
    serializer_class = CategorySimpleListSerializer

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
