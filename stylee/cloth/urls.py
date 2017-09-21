from django.conf.urls import url, include
from django.contrib import admin

# import JWT
from .views import (
    ClothesListView,
    ClothDetailView,
    ClothDetailCommentsView,
    ClothDetailLikesView
)

urlpatterns = [
    url(r'^list/$', ClothesListView.as_view(), name="clo_wardrobe_list"),
    url(r'^detail/(?P<pk>\d+)/$', ClothDetailView.as_view(), name="clo_detail"),
    url(r'^comments/(?P<pk>\d+)/$', ClothDetailCommentsView.as_view(), name="clo_comments"),
    url(r'^likes/(?P<pk>\d+)/$', ClothDetailLikesView.as_view(), name="clo_likes"),
]
