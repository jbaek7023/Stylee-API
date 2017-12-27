from django.conf.urls import url, include
from django.contrib import admin

from .views import (
    OutfitCategoryAPIView,
    CategoryEditAPIView,
    CategoryListAPIView,
    CategoryListForIdAPIView,
    CategorySimpleListAPIView,
    CreateCategoryView,
)

urlpatterns = [
    # edit 으로가세욧!
    url(r'^detail/(?P<pk>\d+)/$', OutfitCategoryAPIView.as_view(), name="outfits_category_list"),
    url(r'^edit/(?P<pk>\d+)/$', CategoryEditAPIView.as_view(), name="category_edit"),
    url(r'^create/$', CreateCategoryView.as_view(), name="create_category"),
    url(r'^simplelist/$', CategorySimpleListAPIView.as_view(), name="category_simple_list"),
    url(r'^list/$', CategoryListAPIView.as_view(), name="category_list"),
    url(r'^catelist/(?P<user_id>\d+)/$', CategoryListForIdAPIView.as_view(), name="category_list_for_id"),

    # url(r'^likelist/(?P<user_id>\d+)/$', CategoryListForIdAPIView.as_view(), name="category_list_for_id"),


]
