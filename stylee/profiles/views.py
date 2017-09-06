from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import render
from django.utils.text import slugify

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

import random
import string

from .serializers import ProfileDetailSerializer, UserEmailSerizlier
from .models import Profile

User = get_user_model()

class ProfileDetailViewByUser(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    lookup_field = 'username'

# /profile/detail/
class ProfileDetailView(generics.ListAPIView):
    serializer_class = ProfileDetailSerializer

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

# class UserCheckEmail(generics.)
