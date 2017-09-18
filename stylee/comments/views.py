from django.shortcuts import render

from rest_framework import generics

from .models import Comment

from .serializers import CommentSerializer, CommentDetailSerializer

# Create your views here.
class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        qs = Comment.objects.all()
        # if undefined user, return 404.(later)
        return qs

# Requires [{JWT or Bearer Token} AND outfit_id
# Returns Outfit fields
class CommentDetailView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    lookup_field = 'pk'

# Requires [{JWT or Bearer Token}]
# Returns Category. [{name:'Gym', main:'aws_img', count: '5'}]
# class OutfitCategoryListView(generics.ListAPIView):
#     serializer_class = OutfitListSerializer

# Requires [{JWT or Bearer Token} AND Category_id]
# Returns Outfits in the category
# class OutfitCategoryDetailView(generi
