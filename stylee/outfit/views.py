from django.shortcuts import render

from rest_framework import generics

from .models import Outfit
from category.models import Category

from .serializers import (
    OutfitListSerializer,
    OutfitDetailSerializer,
    OutfitDetailCommentSerializer,
    OutfitDetailLikeSerializer
)

from comments.serializers import CommentSerializer

# Create your views here.
class OutfitListView(generics.ListAPIView):
    serializer_class = OutfitListSerializer

    def get_queryset(self):
        qs = Outfit.objects.all()
        logged_in_user_profile = qs.filter(user=self.request.user)
        # if undefined user, return 404.(later)
        return logged_in_user_profile

# Requires [{JWT or Bearer Token} AND outfit_id
# Returns Outfit fields
class OutfitDetailView(generics.RetrieveAPIView):
    queryset = Outfit.objects.all()
    serializer_class = OutfitDetailSerializer
    lookup_field = 'pk'
#
# class OutfitCategoryView(generics.RetrieveUpdateAPIView):
#     queryset = Outfit.objects.all()
#     serializer_class = CategoryListUpdateSerializer
#     lookup_field = 'pk'

class OutfitDetailCommentsView(generics.RetrieveAPIView):
    queryset = Outfit.objects.all()
    serializer_class = OutfitDetailCommentSerializer
    lookup_field = 'pk'

class OutfitDetailLikesView(generics.RetrieveAPIView):
    queryset = Outfit.objects.all()
    serializer_class = OutfitDetailLikeSerializer
    lookup_field = 'pk'



# Requires [{JWT or Bearer Token}]
# Returns Category. [{name:'Gym', main:'aws_img', count: '5'}]
# class OutfitCategoryListView(generics.ListAPIView):
#     serializer_class = OutfitListSerializer

# Requires [{JWT or Bearer Token} AND Category_id]
# Returns Outfits in the category
