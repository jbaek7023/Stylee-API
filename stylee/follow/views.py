from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from .models import Follow

class FollowAPIView(APIView):
    def post(self, request, format=None):
        User = get_user_model()
        following_user = User.objects.filter(id=self.request.data.get('user_id')).first()
        if following_user is not None:
            follow_obj = Follow.objects.filter(follower=self.request.user, following=following_user).first()
            if follow_obj is not None:
                # follow_obj.delete()
                json_output = {"success": False}
                # 404 later
                return Response(json_output)
            else:
                instance = Follow(follower=self.request.user, following=following_user)
                instance.save()
                json_output = {"success": True}
                return Response(json_output)
        return Response({})

class UnFollowAPIView(APIView):
    def post(self, request, format=None):
        User = get_user_model()
        following_user = User.objects.filter(id=self.request.data.get('user_id')).first()
        if following_user is not None:
            follow_obj = Follow.objects.filter(follower=self.request.user, following=following_user).first()
            if follow_obj is not None:
                follow_obj.delete()
                json_output = {"success": True}
                return Response(json_output)
            else:
                # instance = Follow(follower=self.request.user, following=following_user)
                # instance.save()
                json_output = {"followed": False}
                # 404 Later
                return Response(json_output)
        return Response({})
