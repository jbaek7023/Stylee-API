from django.conf.urls import url, include
from django.contrib import admin

from .views import (
    LikeListView,
    LikeCreateAPIView,
)

urlpatterns = [
    url(r'^list/$', LikeListView.as_view(), name="likes_list"),
    url(r'^create/$', LikeCreateAPIView.as_view(), name="create_like"),

    # url(r'^category/$', OutfitCategoryListView.as_view(), name="user_outfits_category_list"),
]
