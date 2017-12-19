from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from rest_framework import status

from .models import Star

from .serializers import ListStarSerializer
from .pagination import StarPagination
# class StarCreateAPIView(generics.CreateAPIView):
#     queryset = Star.objects.all()
#
#     def get_serializer_class(self):
#         model_type = self.request.GET.get("type")
#         id = self.request.GET.get("id")
#         return create_star_serializer(
#             model_type=model_type,
#             id=id,
#             user=self.request.user
#         )

class StarCreateView(APIView):
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
                instance, created = Star.objects.get_or_create(
                    user=self.request.user,
                    content_type=model_qs.first(),
                    object_id=obj_qs.first().id
                    )
                    # there is like object
                if created:
                    json_output = {"success": True}
                    # 404 later
                    return Response(json_output, status.HTTP_201_CREATED)
                else:
                    json_output = {"success": False}
                    return Response(json_output, status.HTTP_200_OK)

class StarDestroyView(APIView):
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
                star_instance = Star.objects.filter(
                    user=self.request.user,
                    content_type=model_qs.first(),
                    object_id=obj_qs.first().id
                ).first()
                    # there is something to delete
                if star_instance is not None:
                    star_instance.delete()
                    json_output = {"success": True}
                    return Response(json_output, status.HTTP_200_OK)
                else:
                    json_output = {"success": False}
                    return Response(json_output, status.HTTP_200_OK)


class StarListAPIView(generics.ListAPIView):
    serializer_class = ListStarSerializer
    pagination_class = StarPagination

    def get_queryset(self):
        qs = Star.objects.filter(user=self.request.user)
        return qs


    # Outfit.outfit_img
    # Outfit.id
    #
    # Cloth.cloth_img
