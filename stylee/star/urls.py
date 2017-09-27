from django.conf.urls import url, include
from django.contrib import admin

from .views import (
    StarCreateAPIView,
    StarListAPIView
)

urlpatterns = [
    url(r'^create/$', StarCreateAPIView.as_view(), name="create_star"),
    url(r'^list/$', StarListAPIView.as_view(), name="list_star"),
]
