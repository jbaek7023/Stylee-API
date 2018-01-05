from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from .models import Like
from rest_framework import status

from .serializers import LikeSerializer, LikedUserSerializer
from .pagination import LikePagination

class LikeCreateView(APIView):
    def post(self, request, format=None):
        model_type = self.request.GET.get("type")
        id = self.request.GET.get("id")
        model_qs = ContentType.objects.filter(model=model_type)
        # Model Exists
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(id=id)
            # The instance exists and it is 1.(?)
            if obj_qs.exists():
                instance, created = Like.objects.get_or_create(
                    user=self.request.user,
                    content_type=model_qs.first(),
                    object_id=obj_qs.first().id
                    )
                    # there is like object
                if created:
                    json_output = {"success": True}
                    # 404 later
                    return Response(json_output, status=status.HTTP_200_OK)
                else:
                    json_output = {"success": False}
                    return Response(json_output, status=status.HTTP_400_BAD_REQUEST)

class LikeDestroyView(APIView):
    def post(self, request, format=None):
        model_type = self.request.GET.get("type")
        id = self.request.GET.get("id")
        model_qs = ContentType.objects.filter(model=model_type)
        # Model Exists
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(id=id)
            # The instance exists ()?)
            if obj_qs.exists():
                like_instance = Like.objects.filter(
                    user=self.request.user,
                    content_type=model_qs.first(),
                    object_id=obj_qs.first().id
                ).first()
                    # there is something to delete
                if like_instance is not None:
                    like_instance.delete()
                    json_output = {"success": True}
                    return Response(json_output, status=status.HTTP_200_OK)
                else:
                    json_output = {"success": False}
                    return Response(json_output, status=status.HTTP_400_BAD_REQUEST)

class LikeListView(generics.ListAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        qs = Like.objects.all()
        # if undefined user, return 404.(later)
        return qs

class LikeListByClothId(generics.ListAPIView):
    serializer_class = LikedUserSerializer
    pagination_class = LikePagination

    def get_queryset(self):
        cloth_id = self.kwargs['cid']
        qs = Like.objects.filter(content_type=15, object_id=cloth_id)
        return qs

class LikeListByOutfitId(generics.ListAPIView):
    serializer_class = LikedUserSerializer
    pagination_class = LikePagination

    def get_queryset(self):
        outfit_id = self.kwargs['oid']
        qs = Like.objects.filter(content_type=26, object_id=outfit_id)
        return qs
