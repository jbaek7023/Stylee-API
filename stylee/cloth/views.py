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
import base64
from PIL import Image
from io import BytesIO

class ClothCreateAPIView(APIView):
    def post(self, request, format='multipart/form-data'):
        # Create Cloth
        image_base64 = self.request.data.get('image')
        cloth_image = ContentFile(base64.b64decode(image_base64), name='temp.jpg')

        logged_in_user = self.request.user
        content = self.request.data.get('text')
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

        detail_instance, created = ClothDetail.objects.get_or_create(cloth=cloth_instance)
        detail_instance.color = color
        detail_instance.brand = brand
        detail_instance.size = size
        detail_instance.sex = sex
        detail_instance.seasons = seasons
        detail_instance.location = location
        detail_instance.save()

        json_output = {"success": True}
        return Response(json_output, status=status.HTTP_201_CREATED)

class ClothesListView(generics.ListAPIView):
    serializer_class = ClothesListSerializer

    def get_queryset(self):
        u = self.request.user
        qs = Cloth.objects.all(user=u)
        qs1 = qs.filter(user=u)
        return qs1

class ClothesArchieveList(generics.ListAPIView):
    serializer_class = ClothesListSerializer

    def get_queryset(self):
        u = self.request.user
        qs = Cloth.objects.filter(user=u, archieve=True)
        return qs


class ClothesListByIdView(generics.ListAPIView):
    serializer_class = ClothesListSerializer

    def get_queryset(self):
        uid = self.kwargs['user_id']
        User = get_user_model()
        cloth_owner = User.objects.filter(id=uid).first()
        qs = Cloth.objects.all(user=self.request.user)
        qs = qs.filter(user=cloth_owner)
        return qs

class ClothDetailView(generics.RetrieveAPIView):
    serializer_class = ClothDetailSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        # this is for privacy
        qs = Cloth.objects.all(user=self.request.user)
        return qs

class ClothEditAPIView(UpdateModelMixin, generics.RetrieveAPIView):
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
