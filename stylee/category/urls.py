from django.conf.urls import url, include
from django.contrib import admin

from .views import (
    OutfitCategoryAPIView,
    CategoryListAPIView
)

urlpatterns = [
    url(r'^category/(?P<pk>\d+)/$', OutfitCategoryAPIView.as_view(), name="outfits_category_list"),
    url(r'^list/$', CategoryListAPIView.as_view(), name="category_list"),
]
