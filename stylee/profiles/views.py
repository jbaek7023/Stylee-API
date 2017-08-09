from django.shortcuts import render

from rest_framework import generics

from .serializers import ProfileDetailSerializer
from django.contrib.auth import get_user_model

from .models import Profile

# Create your views here.
class ProfileDetailView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    lookup_field = 'username'
