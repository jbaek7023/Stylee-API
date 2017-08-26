from django.conf.urls import url, include
from django.contrib import admin

# import JWT

urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
]
