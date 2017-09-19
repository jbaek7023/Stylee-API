from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView

from like.models import Like

from .serializers import LikeSerializer, create_like_serializer

class LikeCreateAPIView(generics.CreateAPIView):
    queryset = Like.objects.all()

    def get_serializer_class(self):
        model_type = self.request.GET.get("type")
        id = self.request.GET.get("id")
        return create_like_serializer(
            model_type=model_type,
            id=id,
            user=self.request.user
        )

class LikeListView(generics.ListAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        qs = Like.objects.all()
        # if undefined user, return 404.(later)
        return qs
