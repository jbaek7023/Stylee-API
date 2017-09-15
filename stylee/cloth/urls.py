from django.conf.urls import url, include
from django.contrib import admin

# import JWT
from .views import ClothesListView

urlpatterns = [
    url(r'^list/$', ClothesListView.as_view(), name="clo_wardrobe_list"),
]
