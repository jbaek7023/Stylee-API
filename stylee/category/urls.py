from django.conf.urls import url, include
from django.contrib import admin

from .views import (
    OutfitCategoryAPIView
)

urlpatterns = [
    url(r'^category/(?P<pk>\d+)/$', OutfitCategoryAPIView.as_view(), name="outfits_category_list"),
]
