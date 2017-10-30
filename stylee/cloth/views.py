from django.shortcuts import render
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework import generics
from django.contrib.auth import get_user_model
from .models import Cloth, ClothDetail
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from .serializers import (
    ClothesListSerializer,
    ClothDetailSerializer,
    ClothDetailCommentSerializer,
    ClothDetailLikeSerializer,
    ClothDetailDetailSerializer,
)

class ClothCreateAPIView(APIView):
    def post(self):
        # # Get input from the request
        # id=self.request.POST.get('user_id')
        # outfit_id_list=self.request.POST.get('user_id')
        # id=self.request.POST.get('user_id')
        #
        # cloth_instance = Cloth(
        #     follower=self.request.user,
        #     following=following_user
        #     )
        # cloth_instance.save()
        # # Delete the post_save on Cloth and Create ClothDetail connect to Cloth
        # # get or create
        # detail_instance = ClothDetail.objects.get_or_create(
        #     cloth=cloth_instance,
        #     detail...
        #     )
        #
        # detail_instance.save()
        pass

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
