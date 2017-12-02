from django.conf.urls import url, include
from django.contrib import admin

from .views import (
    LikeListView,
    # LikeCreateAPIView,
    # LikeDestroyAPIView,
    LikeCreateView,
    LikeDestroyView,
)

urlpatterns = [
    url(r'^list/$', LikeListView.as_view(), name="likes_list"),
    # url(r'^create/$', LikeCreateAPIView.as_view(), name="create_like"),
    url(r'^create/$', LikeCreateView.as_view(), name="createo_like"),
    # url(r'^delete/$', LikeDestroyAPIView.as_view(), name="delete_like"),
    url(r'^delete/$', LikeDestroyView.as_view(), name="deleteo_like"),
    # url(r'^category/$', OutfitCategoryListView.as_view(), name="user_outfits_category_list"),
]
