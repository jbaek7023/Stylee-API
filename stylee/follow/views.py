from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import generics
from .serializers import FollowerUserSerializer, FollowingUserSerializer
from .models import Follow
from .pagination import FollowPagination

class FollowAPIView(APIView):
    def post(self, request, format=None):
        User = get_user_model()
        following_user = User.objects.filter(id=self.request.data.get('user_id')).first()
        if following_user is not None:
            follow_obj = Follow.objects.filter(user=self.request.user, target=following_user).first()
            if follow_obj is not None:
                # follow_obj.delete()
                json_output = {"success": False}
                # 404 later
                return Response(json_output)
            else:
                instance = Follow(user=self.request.user, target=following_user)
                instance.save()
                json_output = {"success": True}
                return Response(json_output)
        return Response({})

class UnFollowAPIView(APIView):
    def post(self, request, format=None):
        User = get_user_model()
        following_user = User.objects.filter(id=self.request.data.get('user_id')).first()
        if following_user is not None:
            follow_obj = Follow.objects.filter(user=self.request.user, target=following_user).first()
            if follow_obj is not None:
                follow_obj.delete()
                json_output = {"success": True}
                return Response(json_output)
            else:
                json_output = {"followed": False}
                # 404 Later
                return Response(json_output)
        return Response({})

class FollowingUserView(generics.ListAPIView):
    serializer_class = FollowingUserSerializer
    pagination_class = FollowPagination

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        User = get_user_model()
        page_owner = User.objects.filter(id=user_id).first()
        if page_owner is not None:
            qs = Follow.objects.filter(target=page_owner)
            return qs
        return Follow.objects.none()

class FollowerUserView(generics.ListAPIView):
    serializer_class = FollowerUserSerializer
    pagination_class = FollowPagination

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        User = get_user_model()
        page_owner = User.objects.filter(id=user_id).first()
        if page_owner is not None:
            qs = Follow.objects.filter(user=page_owner)
            return qs
        return Follow.objects.none()
