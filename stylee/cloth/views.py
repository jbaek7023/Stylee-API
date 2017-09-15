from django.shortcuts import render

from rest_framework import generics

from .models import Cloth

from .serializers import ClothesListSerializer

# Create your views here.
class ClothesListView(generics.ListAPIView):
    serializer_class = ClothesListSerializer

    def get_queryset(self):
        qs = Cloth.objects.all()
        logged_in_user_profile = qs.filter(user=self.request.user)
        return logged_in_user_profile
