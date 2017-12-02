from django.conf.urls import url

# import JWT
from .views import (
    FollowAPIView,
    UnFollowAPIView,
)

urlpatterns = [
    url(r'^follow/$', FollowAPIView.as_view(), name="follow_user"),
    url(r'^unfollow/$', UnFollowAPIView.as_view(), name="unfollow_user"),
]
