from django.shortcuts import render
from re import sub
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.authtoken.models import Token
from .models import Outfit
from category.models import Category
from rest_framework.views import APIView

from .serializers import (
    OutfitListSerializer,
    OutfitDetailSerializer,
    OutfitDetailCommentSerializer,
    OutfitDetailLikeSerializer,
    OutfitCreateSerializer,
    OutfitDetailFeedSerializer,
)

from comments.serializers import CommentSerializer

class OutfitCreateAPIView(APIView):
    def post(self):
        # id = self.request.POST.get('user_id')

        # Outfit.Create

        # Img width and height, positionX, Y
        # Cloth.get_create()

        # ?조금더 하면됨. 굳.
        pass

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
