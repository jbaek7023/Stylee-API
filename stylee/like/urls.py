from django.conf.urls import url, include
from django.contrib import admin

from .views import (
    LikeListView,
    # LikeCreateAPIView,
    # LikeDestroyAPIView,
    LikeCreateView,
    LikeDestroyView,
    LikeListByClothId,
    LikeListByOutfitId,
)

urlpatterns = [
    url(r'^list/$', LikeListView.as_view(), name="likes_list"),

    url(r'^cloth/(?P<cid>\d+)/$', LikeListByClothId.as_view(), name="cloth_likes"),
    url(r'^outfit/(?P<oid>\d+)/$', LikeListByOutfitId.as_view(), name="outfit_likes"),
    # url(r'^create/$', LikeCreateAPIView.as_view(), name="create_like"),
    url(r'^create/$', LikeCreateView.as_view(), name="createo_like"),
    # url(r'^delete/$', LikeDestroyAPIView.as_view(), name="delete_like"),
    url(r'^delete/$', LikeDestroyView.as_view(), name="deleteo_like"),
    # url(r'^category/$', OutfitCategoryListView.as_view(), name="user_outfits_category_list"),
]
