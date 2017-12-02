from django.conf.urls import url, include
from django.contrib import admin

from .views import (
    StarCreateView,
    StarDestroyView,
    StarListAPIView
)

urlpatterns = [
    url(r'^create/$', StarCreateView.as_view(), name="create_star"),
    url(r'^delete/$', StarDestroyView.as_view(), name="delete_star"),
    url(r'^list/$', StarListAPIView.as_view(), name="list_star"),
]
