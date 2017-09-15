from django.shortcuts import render

from rest_framework import generics

from .models import Outfit

from .serializers import OutfitListSerializer

# Create your views here.
class OutfitListView(generics.ListAPIView):
    serializer_class = OutfitListSerializer

    def get_queryset(self):
        qs = Outfit.objects.all()
        logged_in_user_profile = qs.filter(user=self.request.user)
        # if undefined user, return 404.(later)
        return logged_in_user_profile
