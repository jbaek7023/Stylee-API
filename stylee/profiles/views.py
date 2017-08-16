from django.shortcuts import render

from rest_framework import generics

from .serializers import ProfileDetailSerializer
from django.contrib.auth import get_user_model

from .models import Profile

class ProfileDetailViewByUser(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    lookup_field = 'username'

class ProfileDetailView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer

    def get_queryset(self):
        qs = super(ProfileDetailView, self).get_queryset()
        logged_in_user_profile = qs.filter(user=self.request.user)
        return logged_in_user_profile
