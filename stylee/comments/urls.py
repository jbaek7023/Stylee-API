from django.conf.urls import url, include
from django.contrib import admin

from .views import (
    CommentListView,
    CommentDetailView,
    CommentCreateAPIView,
    CommentEditAPIView,
    CommentsOnOutfit,
    CommentsOnCloth,
    CreateReplyAPIView,
)

urlpatterns = [
    url(r'^list/$', CommentListView.as_view(), name="comments_list"),
    url(r'^olist/(?P<oid>\d+)/$', CommentsOnOutfit.as_view(), name="comments_on_outfit"),
    url(r'^clist/(?P<cid>\d+)/$', CommentsOnCloth.as_view(), name="comments_on_cloth"),
    # comment and its detail
    url(r'^detail/(?P<pk>\d+)/$', CommentDetailView.as_view(), name="comment_detail"),
    url(r'^edit/(?P<pk>\d+)/$', CommentEditAPIView.as_view(), name="comment_edit"),
    url(r'^create/$', CommentCreateAPIView.as_view(), name="create_comment"),
    url(r'^reply/$', CreateReplyAPIView.as_view(), name="reply_on_comment"),

    # url(r'^category/$', OutfitCategoryListView.as_view(), name="user_outfits_category_list"),
]
