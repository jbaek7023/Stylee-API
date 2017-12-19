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
    CategoryListOnOutfitView,
    AddOutfitOnCategory,
    DeleteOutfitOnCategory,
    StyleFeedAPIView,
    PopularFeedAPIView,
    ProfileOutfitListNext,
)

urlpatterns = [
    url(r'^feed/(?P<page>\d+)/$', StyleFeedAPIView.as_view(), name="style_feed"),
    url(r'^popular/$', PopularFeedAPIView.as_view(), name="popular_feed"),

    url(r'^create/$', OutfitCreateAPIView.as_view(), name="create_outfit"),
    url(r'^addto/$', AddOutfitOnCategory.as_view(), name="add_outfit_to_category"),
    url(r'^deletefrom/$', DeleteOutfitOnCategory.as_view(), name="delete_outfit_from_category"),
    url(r'^list/$', OutfitListView.as_view(), name="user_outfits_list"),

    url(r'^catelist/(?P<pk>\d+)/$', CategoryListOnOutfitView.as_view(), name="outfit_categories"),

    # detail / edit is actually same thing, yeah but let's do it later
    url(r'^detail/(?P<pk>\d+)/$', OutfitDetailView.as_view(), name="outfit_detail"),
    url(r'^edit/(?P<pk>\d+)/$', OutfitEditView.as_view(), name="outfit_edit"),


    url(r'^comments/(?P<pk>\d+)/$', OutfitDetailCommentsView.as_view(), name="outfit_comments"),
    url(r'^likes/(?P<pk>\d+)/$', OutfitDetailLikesView.as_view(), name="outfit_likes"),
    url(r'^outlist/(?P<user_id>\d+)/$', OutfitListByIdView.as_view(), name="outfit_list_by_id"),
    url(r'^next/(?P<user_id>\d+)/(?P<page>\d+)/$', ProfileOutfitListNext.as_view(), name="outfit_list_next"),
    url(r'^outfeedlist/(?P<user_id>\d+)/$', OutfitFeedListView.as_view(), name="outfit_feedlist_by_id"),
]
