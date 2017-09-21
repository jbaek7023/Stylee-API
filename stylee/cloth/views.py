from django.shortcuts import render

from rest_framework import generics

from .models import Cloth

from .serializers import (
    ClothesListSerializer,
    ClothDetailSerializer,
    ClothDetailCommentSerializer,
    ClothDetailLikeSerializer
)

# Create your views here.
class ClothesListView(generics.ListAPIView):
    serializer_class = ClothesListSerializer

    def get_queryset(self):
        qs = Cloth.objects.all()
        logged_in_user_profile = qs.filter(user=self.request.user)
        return logged_in_user_profile

class ClothDetailView(generics.RetrieveAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothDetailSerializer
    lookup_field = 'pk'

class ClothDetailCommentsView(generics.RetrieveAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothDetailCommentSerializer
    lookup_field = 'pk'

class ClothDetailLikesView(generics.RetrieveAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothDetailLikeSerializer
    lookup_field = 'pk'
