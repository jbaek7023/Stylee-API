from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from .models import Like

from .serializers import LikeSerializer
# , create_like_serializer, delete_like_serializer

# class LikeCreateAPIView(generics.CreateAPIView):
#     queryset = Like.objects.all()
#
#     def get_serializer_class(self):
#         model_type = self.request.GET.get("type")
#         id = self.request.GET.get("id")
#         return create_like_serializer(
#             model_type=model_type,
#             id=id,
#             user=self.request.user
#         )

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
                    return Response(json_output)
                else:
                    json_output = {"success": False}
                    return Response(json_output)

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
                    return Response(json_output)
                else:
                    json_output = {"success": False}
                    return Response(json_output)

# class LikeDestroyAPIView(generics.DestroyAPIView):
#     queryset = Like.objects.all()
#
#     def get_serializer_class(self):
#         model_type = self.request.GET.get("type")
#         id = self.request.GET.get("id")
#
#
#
#         return delete_like_serializer(
#             model_type=model_type,
#             id=id,
#             user=self.request.user
#         )

class LikeListView(generics.ListAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        qs = Like.objects.all()
        # if undefined user, return 404.(later)
        return qs
