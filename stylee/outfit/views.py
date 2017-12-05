from django.shortcuts import render
from re import sub
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.authtoken.models import Token
from .models import Outfit
from cloth.models import Cloth
from category.models import Category
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from base64 import b64decode
from django.core.files.base import ContentFile

from .serializers import (
    OutfitListSerializer,
    OutfitDetailSerializer,
    OutfitDetailCommentSerializer,
    OutfitDetailLikeSerializer,
    OutfitCreateSerializer,
    OutfitDetailFeedSerializer,
    CategoryListOnOutfitSerializer,
)
import base64

from comments.serializers import CommentSerializer

class OutfitCreateAPIView(APIView):
    def post(self, request, format='multipart/form-data'):
        # Create Outfits
        content = self.request.data.get('name')
        base_img_data = self.request.data.get('base64')
        outfit_img = ContentFile(base64.b64decode(base_img_data), name='temp.jpg')
        gender = self.request.data.get('gender')
        location = self.request.data.get('location')
        description = self.request.data.get('description')
        only_me = self.request.data.get('onlyMe')
        link=self.request.data.get('link')

        outfit_instance = Outfit(
            user=self.request.user,
            content=content,
            outfit_img=outfit_img,
            gender=gender,
            location=location,
            description=description,
            only_me=only_me,
            link=link
        )
        outfit_instance.save()

        tagged_categories = self.request.data.get('taggedCategories')
        for category_id in tagged_categories:
            category_instance = Category.objects.get(id=category_id, owner=self.request.user)
            if category_instance is not None:
                category_instance.outfits.add(outfit_instance)
        cloth_ids = self.request.data.get('selectedClothesIds')

        for cloth_id in cloth_ids:
            cloth_instance = Cloth.objects.get(id=cloth_id, user=self.request.user)
            if cloth_instance is not None:
                outfit_instance.tagged_clothes.add(cloth_instance)

        tagged_clothes = self.request.data.get('taggedClothes')

        for tagged_cloth in tagged_clothes:
            image_base = tagged_cloth.get('base64')
            cloth_image = ContentFile(base64.b64decode(image_base), name='temp.jpg')
            print(cloth_image)
            new_cloth_instance = Cloth(
                user=self.request.user,
                cloth_image=cloth_image
            )
            new_cloth_instance.save()

            cloth_content = tagged_cloth.get('name')
            if cloth_content is not None:
                new_cloth_instance.content = cloth_content

            cloth_type = tagged_cloth.get('clothType')
            if cloth_type is not None:
                new_cloth_instance.cloth_type = cloth_type

            in_wardrobe = tagged_cloth.get('inWardrobe')
            if in_wardrobe is not None:
                new_cloth_instance.in_wardrobe = in_wardrobe

            only_me = tagged_cloth.get('onlyMe')
            if only_me is not None:
                new_cloth_instance.only_me = only_me

            gender = tagged_cloth.get('gender')
            if gender is not None:
                new_cloth_instance.gender = gender

            seasons = tagged_cloth.get('selectedSeasonIds')
            if seasons is not None:
                new_cloth_instance.seasons = seasons

            size = tagged_cloth.get('selectedSizeIds')
            if size is not None:
                new_cloth_instance.size = size

            color = tagged_cloth.get('selectedColorIds')
            if color is not None:
                new_cloth_instance.color = color
            outfit_instance.tagged_clothes.add(new_cloth_instance)

        # Tag Clothes to the Outfits
        json_output = {"success": True, "created": outfit_instance.publish }
        return Response(json_output, status=status.HTTP_201_CREATED)


class AddOutfitOnCategory(APIView):
    def post(self, request, format=None):
        outfit_id = self.request.data.get('outfit_id')
        outfit_instance = Outfit.objects.filter(id=outfit_id).first()
        if outfit_instance is not None:
            category_id = self.request.data.get('category_id')
            category_instance = Category.objects.filter(
                id=category_id,
                owner=self.request.user).first()
            if category_instance is not None:
                category_instance.outfits.add(outfit_instance)
                # if category_instance.main_img is None:
                #     category_instance.main_img = outfit_instance.outfit_img
                json_output = {"success": True, "added": category_instance.name }
                return Response(json_output, status.HTTP_201_CREATED)
            else:
                json_output = {"success": False}
                return Response(json_output, status.HTTP_409_CONFLICT)
        else:
            json_output = {"success": False}
            return Response(json_output, status.HTTP_409_CONFLICT)

class DeleteOutfitOnCategory(APIView):
    def post(self, request, format=None):
        outfit_id = self.request.data.get('outfit_id')
        outfit_instance = Outfit.objects.filter(id=outfit_id).first()
        if outfit_instance is not None:
            category_id = self.request.data.get('category_id')
            category_instance = Category.objects.filter(
                id=category_id,
                owner=self.request.user).first()

            print(category_instance)
            if category_instance is not None:
                category_name = category_instance.name
                category_instance.outfits.remove(outfit_instance)
                # if category_instance.main_img is None:
                #     category_instance.main_img = outfit_instance.outfit_img
                json_output = {"success": True, "removed": category_name }
                return Response(json_output, status.HTTP_200_OK)
            else:
                json_output = {"success": False}
                return Response(json_output, status.HTTP_409_CONFLICT)

        else:
            json_output = {"success": False}
            return Response(json_output, status.HTTP_409_CONFLICT)

# Create your views here.
class OutfitListView(generics.ListAPIView):
    serializer_class = OutfitListSerializer

    def get_queryset(self):
        qs = Outfit.objects.all(user=self.request.user)
        logged_in_user_profile = qs.filter(user=self.request.user)
        # if undefined user, return 404.(later)
        return logged_in_user_profile

class OutfitListByIdView(generics.ListAPIView):
    serializer_class = OutfitListSerializer

    def get_queryset(self):
        uid = self.kwargs['user_id']
        User = get_user_model()
        outfit_owner = User.objects.filter(id=uid).first()
        # this is wrong.
        qs = Outfit.objects.all(user=self.request.user)
        # This is not quite.
        qs = qs.filter(user=outfit_owner)
        return qs

# Requires [{JWT or Bearer Token} AND outfit_id
# Returns Outfit fields
class OutfitDetailView(generics.RetrieveAPIView):
    serializer_class = OutfitDetailSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = Outfit.objects.all(user=self.request.user)
        return qs

class CategoryListOnOutfitView(generics.RetrieveAPIView):
    serializer_class = CategoryListOnOutfitSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = Outfit.objects.all(user=self.request.user)
        return qs

# Requires [{JWT or Bearer Token} AND outfit_id
# Returns Outfit fields
# By Id
class OutfitFeedListView(generics.ListAPIView):
    serializer_class = OutfitDetailFeedSerializer

    def get_queryset(self):
        uid = self.kwargs['user_id']
        User = get_user_model()
        outfit_owner = User.objects.filter(id=uid).first()
        # this is wrong.
        qs = Outfit.objects.all(user=self.request.user)
        # This is not quite.
        qs = qs.filter(user=outfit_owner)
        return qs

class OutfitEditView(DestroyModelMixin, UpdateModelMixin, generics.RetrieveAPIView):
    serializer_class = OutfitDetailSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = Outfit.objects.all(user=self.request.user)
        return qs

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class OutfitDetailCommentsView(generics.RetrieveAPIView):
    serializer_class = OutfitDetailCommentSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = Outfit.objects.all(user=self.request.user)
        return qs

class OutfitDetailLikesView(generics.RetrieveAPIView):
    serializer_class = OutfitDetailLikeSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = Outfit.objects.all(user=self.request.user)
        return qs
