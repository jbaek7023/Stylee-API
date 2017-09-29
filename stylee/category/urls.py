from django.conf.urls import url, include
from django.contrib import admin

from .views import (
    OutfitCategoryAPIView,
    CategoryListAPIView,
    CategoryListForIdAPIView,
)

urlpatterns = [
    url(r'^detail/(?P<pk>\d+)/$', OutfitCategoryAPIView.as_view(), name="outfits_category_list"),
    url(r'^list/$', CategoryListAPIView.as_view(), name="category_list"),
    url(r'^catelist/(?P<user_id>\d+)/$', CategoryListForIdAPIView.as_view(), name="category_list_for_id"),
]
