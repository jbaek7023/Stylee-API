from django.shortcuts import render
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework import generics
from django.contrib.auth import get_user_model
from .models import Cloth, ClothDetail
from outfit.models import Outfit
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from base64 import b64decode
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    ClothesListSerializer,
    ClothDetailSerializer,
    ClothDetailCommentSerializer,
    ClothDetailLikeSerializer,
    ClothDetailDetailSerializer,
)

from .pagination import ClothPagination
import base64

class ClothCreateAPIView(APIView):
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

        json_output = {"success": True, "created": cloth_instance.created_at}
        return Response(json_output, status=status.HTTP_201_CREATED)

class ClothUpdateAPIView(APIView):
    def put(self, request, format='multipart/form-data'):
        # Create Cloth
        logged_in_user = self.request.user
        content = self.request.data.get('name')
        big_cloth_type = self.request.data.get('bigType')
        cloth_type = self.request.data.get('clothType')
        in_wardrobe = self.request.data.get('inWardrobe')
        only_me = self.request.data.get('onlyMe')
        link = self.request.data.get('link')
        cid = self.request.data.get('cid')
        qs = Cloth.objects.filter(id=cid)
        if not qs:
            return Response(json_output, status=status.HTTP_404_NOT_FOUND)
        cloth_instance = qs.first()
        if not cloth_instance:
            return Response(json_output, status=status.HTTP_404_NOT_FOUND)

        cloth_instance.content=content
        cloth_instance.big_cloth_type = big_cloth_type
        cloth_instance.cloth_type = cloth_type
        cloth_instance.in_wardrobe = in_wardrobe
        cloth_instance.only_me = only_me
        cloth_instance.link = link
        cloth_instance.save()

        # Add outfit
        styleIds = request.data.get('selectedStyleIds')
        cloth_instance.outfit_set = Outfit.objects.none()
        if styleIds:
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
        return Response(json_output, status=status.HTTP_200_OK)

class ClothesListView(generics.ListAPIView):
    serializer_class = ClothesListSerializer
    pagination_class = ClothPagination

    def get_queryset(self):
        cloth_type = self.kwargs['ctype']
        u = self.request.user
        big_cloth_type = 'Top'
        if cloth_type == str(2):
            big_cloth_type = 'Outerwear'
        elif cloth_type == str(3):
            big_cloth_type = 'Bottom'
        elif cloth_type == str(4):
            big_cloth_type = 'Shoes'
        elif cloth_type == str(5):
            big_cloth_type = 'ETC'
        qs = Cloth.objects.filter(user=u, big_cloth_type=big_cloth_type, archieve=False)
        return qs

class ClothesArchieveList(generics.ListAPIView):
    serializer_class = ClothesListSerializer
    pagination_class = ClothPagination

    def get_queryset(self):
        u = self.request.user
        qs = Cloth.objects.filter(user=u, archieve=True)
        return qs


class ClothesListByIdView(generics.ListAPIView):
    serializer_class = ClothesListSerializer
    pagination_class = ClothPagination

    def get_queryset(self):
        cloth_type = self.kwargs['ctype']
        uid = self.kwargs['user_id']
        User = get_user_model()
        cloth_owner = User.objects.filter(id=uid).first()

        big_cloth_type = 'Top'
        if cloth_type == str(2):
            big_cloth_type = 'Outerwear'
        elif cloth_type == str(3):
            big_cloth_type = 'Bottom'
        elif cloth_type == str(4):
            big_cloth_type = 'Shoes'
        elif cloth_type == str(5):
            big_cloth_type = 'ETC'

        if cloth_owner == self.request.user:
            qs = Cloth.objects.filter(user=cloth_owner, big_cloth_type=big_cloth_type, archieve=False)
        else:
            qs = Cloth.objects.filter(user=cloth_owner, big_cloth_type=big_cloth_type, only_me=False, archieve=False)
        return qs

class ClothDetailView(generics.RetrieveAPIView):
    serializer_class = ClothDetailSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        # this is for privacy
        qs = Cloth.objects.all(user=self.request.user)
        return qs

class ClothEditAPIView(DestroyModelMixin, UpdateModelMixin, generics.RetrieveAPIView):
    serializer_class = ClothDetailSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        # this is for privacy
        qs = Cloth.objects.all(user=self.request.user)
        return qs

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ClothDetailDetailEditAPIView(UpdateModelMixin, DestroyModelMixin, generics.RetrieveAPIView):
    serializer_class = ClothDetailDetailSerializer

    def get_queryset(self):
        # this is for privacy
        qs = Cloth.objects.all(user=self.request.user)
        return qs

    def get_object(self):
        pk = self.kwargs['pk']
        queryset = self.get_queryset().filter(id=pk)
        obj = get_object_or_404(queryset)
        return obj.c_detail

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ClothDetailCommentsView(generics.RetrieveAPIView):
    serializer_class = ClothDetailCommentSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = Cloth.objects.all(user=self.request.user)
        return qs


class ClothDetailLikesView(generics.RetrieveAPIView):
    serializer_class = ClothDetailLikeSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = Cloth.objects.all(user=self.request.user)
        return qs
