from django.shortcuts import render

from rest_framework import generics

from .models import Comment

from .serializers import CommentSerializer, CommentDetailSerializer, create_comment_serializer

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

# Comment on outfit
class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        model_type = self.request.GET.get("type")
        id = self.request.GET.get("id")
        print(id)
        parent_id = self.request.GET.get("parent_id", None)
        return create_comment_serializer(
            model_type='outfit',
            id=id,
            user=self.request.user,
            parent_id=parent_id
        )

# Requires [{JWT or Bearer Token}]
# Returns Category. [{name:'Gym', main:'aws_img', count: '5'}]
# class OutfitCategoryListView(generics.ListAPIView):
#     serializer_class = OutfitListSerializer

# Requires [{JWT or Bearer Token} AND Category_id]
# Returns Outfits in the category
# class OutfitCategoryDetailView(generi
