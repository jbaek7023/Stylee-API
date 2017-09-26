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
        u = self.request.user
        cloth_type = self.request.GET.get("c")
        qs = Cloth.objects.all()
        qs1 = qs.filter(user=u).filter(big_cloth_type=cloth_type)
        return qs1

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
