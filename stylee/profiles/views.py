from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import render
from django.utils.text import slugify

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

import random
import string

from .serializers import (
    UserMenuSerializer,
    UserEmailSerizlier,
    ProfileRetrieveAndUpdateSerializer,
    FollowCreateSerializer
)

from .models import Profile, Follow

User = get_user_model()

# class ProfileDetailViewByUser(generics.RetrieveAPIView):
#     # we don't take use this function now
#     queryset = Profile.objects.all()
#     serializer_class = ProfileDetailSerializer
#     lookup_field = 'username'

# /profile/detail/
class UserDetailView(generics.ListAPIView):
    serializer_class = UserMenuSerializer

    def get_queryset(self):
        qs = Profile.objects.all()
        logged_in_user_profile = qs.filter(user=self.request.user)
        return logged_in_user_profile

class FollowCreateAPIView(APIView):
    def post(self, request, format=None):
        following_user = User.objects.filter(id=self.request.POST.get('user_id')).first()
        if following_user is not None:
            follow_obj = Follow.objects.filter(follower=self.request.user, following=following_user).first()
            if follow_obj is not None:
                follow_obj.delete()
                json_output = {"followed": False}
                return Response(json_output)
            else:
                instance = Follow(follower=self.request.user, following=following_user)
                instance.save()
                json_output = {"followed": True}
                return Response(json_output)
        return Response({})

# profile/update/<user_id> # only allow to logged in user (SECURE)
class ProfileRetrieveAndUpdateProfile(generics.RetrieveUpdateAPIView):
    """
    PUT : Edit
    GET : Retrieve Profile
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileRetrieveAndUpdateSerializer
    lookup_field = 'user_id'

    def get_queryset(self):
        qs = Profile.objects.all()
        logged_in_user_profile = qs.filter(user=self.request.user)
        return logged_in_user_profile

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_unique_username(username):
    #split @
    if '@' in username:
        part = username.split('@')
        username = part[0]
    # We only allow lower case for the username but just in case
    username = username.lower()

    ## Delete the username on Profile! (later Task)
    exists = User.objects.filter(username=username).exists()
    if exists:
        new_username = "%s%s" % (username, random_string_generator(size=1))
        return create_unique_username(username=new_username)
    return username

class UserCheckEmail(APIView):
    # CHECK username or email is valid
    # 200; obtained -> the email is already obtained
    # 200; username -> jbaek70233 is valid username

    def get(self, request, format=None):
        qs = User.objects.all()
        email = self.request.GET.get("em")
        if email:
            qs = qs.filter(
                Q(email__exact=email)
            ).distinct()

        if(len(qs)==1):
            json_output = {"obtained": 0}
            return Response(json_output)
        else:
            email = create_unique_username(email)
            json_output = {"username": email}
            return Response(json_output)

class UserCheckUsername(APIView):
    def get(self, request, format=None):
        qs = User.objects.all()
        username = self.request.GET.get("un")
        if username:
            qs = qs.filter(
                Q(username__exact=username)
            ).distinct()
        print(len(qs))
        if(len(qs)==1):
            json_output = {"obtained": True}
            return Response(json_output)
        else:
            json_output = {"obtained": False}
            return Response(json_output)
