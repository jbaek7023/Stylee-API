from django.shortcuts import render

from rest_framework import generics

from .models import Comment
from outfit.models import Outfit
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin

from .serializers import (
    CommentSerializer,
    CommentDetailSerializer,
    create_comment_serializer,
    CommentEditSerializer,
)

class CommentsOnOutfit(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        content_type = 26
        oid = self.kwargs['oid']
        comments = Comment.objects.filter(content_type=content_type, object_id=oid)
        return comments

class CommentsOnCloth(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        content_type = 15
        cid = self.kwargs['cid']
        comments = Comment.objects.filter(content_type=content_type, object_id=cid)
        return comments

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
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentDetailSerializer
    lookup_field = 'pk'

# Edit or Delete Comment
class CommentEditAPIView(DestroyModelMixin, UpdateModelMixin, generics.RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=0) # all comment
    serializer_class = CommentEditSerializer
    lookup_field = 'pk'

    #define mixin method
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Comment on outfit
class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        model_type = self.request.GET.get("type")
        id = self.request.GET.get("id")
        parent_id = self.request.GET.get("parent_id", None)
        return create_comment_serializer(
            model_type=model_type,
            id=id,
            user=self.request.user,
            parent_id=parent_id
        )

class CreateReplyAPIView(APIView):
    def post(self, request, format=None):
        # get parent comment
        parent_comment_id = self.request.data.get('pid')
        parent_comment_qs = Comment.objects.filter(id=parent_comment_id)

        if parent_comment_qs:
            parent_instance = parent_comment_qs.first()
            content = self.request.data.get('message')

            # create Comment on Parent (Reply)
            reply = Comment(
                parent=parent_instance,
                content=content,
                content_type=parent_instance.content_type,
                object_id=parent_instance.object_id
                )
            reply.save()
            json_output = {"success": True}
            return Response(json_output, status=status.HTTP_200_OK)

        json_output = {"success": False}
        return Response(json_output, status=status.HTTP_404_NOT_FOUND)
