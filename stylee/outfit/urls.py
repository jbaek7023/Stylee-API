from django.conf.urls import url, include
from django.contrib import admin

from .views import (
    OutfitListView,
    OutfitDetailView,
    OutfitDetailCommentsView
)

urlpatterns = [
    url(r'^list/$', OutfitListView.as_view(), name="user_outfits_list"),
    url(r'^detail/(?P<pk>\d+)/$', OutfitDetailView.as_view(), name="outfit_detail"),
    url(r'^comments/(?P<pk>\d+)/$', OutfitDetailCommentsView.as_view(), name="outfit_comments"),
]
