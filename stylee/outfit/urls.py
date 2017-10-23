from django.conf.urls import url, include
from django.contrib import admin

from .views import (
    OutfitListView,
    OutfitDetailView,
    OutfitDetailCommentsView,
    OutfitDetailLikesView,
    OutfitListByIdView,
    OutfitEditView,
    OutfitCreateAPIView,
    OutfitFeedListView,
)

urlpatterns = [
    url(r'^create/$', OutfitCreateAPIView.as_view(), name="create_outfit"),
    url(r'^list/$', OutfitListView.as_view(), name="user_outfits_list"),
    url(r'^detail/(?P<pk>\d+)/$', OutfitDetailView.as_view(), name="outfit_detail"),
    url(r'^edit/(?P<pk>\d+)/$', OutfitEditView.as_view(), name="outfit_edit"),
    url(r'^comments/(?P<pk>\d+)/$', OutfitDetailCommentsView.as_view(), name="outfit_comments"),
    url(r'^likes/(?P<pk>\d+)/$', OutfitDetailLikesView.as_view(), name="outfit_likes"),
    url(r'^outlist/(?P<user_id>\d+)/$', OutfitListByIdView.as_view(), name="outfit_list_by_id"),
    url(r'^outfeedlist/(?P<user_id>\d+)/$', OutfitFeedListView.as_view(), name="outfit_feedlist_by_id"),
]
