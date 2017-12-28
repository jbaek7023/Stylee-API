from django.conf.urls import url, include
from django.contrib import admin

# import JWT
from .views import (
    ClothesListView,
    ClothDetailView,
    ClothDetailCommentsView,
    ClothDetailLikesView,
    ClothesListByIdView,
    ClothesArchieveList,
    ClothEditAPIView,
    ClothDetailDetailEditAPIView,
    ClothCreateAPIView,
    ClothUpdateAPIView,
)

urlpatterns = [
    url(r'^list/(?P<ctype>\d+)/$', ClothesListView.as_view(), name="clo_wardrobe_list"),
    url(r'^create/$', ClothCreateAPIView.as_view(), name="create_cloth"),
    url(r'^update/$', ClothUpdateAPIView.as_view(), name="update_cloth"),

    url(r'^detail/(?P<pk>\d+)/$', ClothDetailView.as_view(), name="clo_detail"),
    url(r'^edit/(?P<pk>\d+)/$', ClothEditAPIView.as_view(), name="clo_edit"),

    url(r'^comments/(?P<pk>\d+)/$', ClothDetailCommentsView.as_view(), name="clo_comments"),
    url(r'^likes/(?P<pk>\d+)/$', ClothDetailLikesView.as_view(), name="clo_likes"),
    url(r'^clothlist/(?P<user_id>\d+)/(?P<ctype>\d+)/$', ClothesListByIdView.as_view(), name="clo_list_id"),
    url(r'^archieve/$', ClothesArchieveList.as_view(), name="archieve_clo_list"),
    url(r'^detailedit/(?P<pk>\d+)/$', ClothDetailDetailEditAPIView.as_view(), name="clo_detail_edit"),
]
