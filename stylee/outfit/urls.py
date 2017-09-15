from django.conf.urls import url, include
from django.contrib import admin

from .views import OutfitListView

urlpatterns = [
    url(r'^list/$', OutfitListView.as_view(), name="user_outfits_list"),
]
