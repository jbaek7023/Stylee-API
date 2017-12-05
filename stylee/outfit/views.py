from django.shortcuts import render
from re import sub
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.authtoken.models import Token
from .models import Outfit
from category.models import Category
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import (
    OutfitListSerializer,
    OutfitDetailSerializer,
    OutfitDetailCommentSerializer,
    OutfitDetailLikeSerializer,
    OutfitCreateSerializer,
    OutfitDetailFeedSerializer,
    CategoryListOnOutfitSerializer,
)

from comments.serializers import CommentSerializer

class OutfitCreateAPIView(APIView):
    def post(self, request, format='multipart/form-data'):
        # Create Cloth
        image_base64 = self.request.data.get('image')
        cloth_image = ContentFile(base64.b64decode(image_base64), name='temp.jpg')

        logged_in_user = self.request.user
        content = self.request.data.get('name')
        big_cloth_type = self.request.data.get('bigType')
        cloth_type = self.request.data.get('clothType')
        in_wardrobe = self.request.data.get('inWardrobe')
        only_me = self.request.data.get('onlyMe')
        link = self.request.data.get('link')

        cloth_instance = Cloth(
            user=logged_in_user,
            content=content,
            big_cloth_type=big_cloth_type,
            cloth_type=cloth_type,
            cloth_image=cloth_image,
            in_wardrobe=in_wardrobe,
            only_me=only_me,
            link=link,
            )
        cloth_instance.save()

        # Add outfit
        styleIds = request.data.get('selectedStyleIds')
        for styleId in styleIds:
            try:
                outfit = Outfit.objects.get(id=styleId)
            except SomeModel.DoesNotExist:
                outfit = None
            if outfit is not None:
                outfit.tagged_clothes.add(cloth_instance)
                # don' need to do save()

        # Create Cloth Detail
        color = self.request.data.get('selectedColorIds') # multiple
        brand = self.request.data.get('brand')
        size = self.request.data.get('selectedSizeIds') # multiple
        sex = self.request.data.get('gender')
        seasons = self.request.data.get('selectedSeasonIds') # multiple
        location = self.request.data.get('location')
        description = self.request.data.get('description')

        detail_instance, created = ClothDetail.objects.get_or_create(cloth=cloth_instance)
        detail_instance.color = color
        detail_instance.brand = brand
        detail_instance.size = size
        detail_instance.sex = sex
        detail_instance.seasons = seasons
        detail_instance.location = location
        detail_instance.description = description
        detail_instance.save()

        json_output = {"success": True}
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
