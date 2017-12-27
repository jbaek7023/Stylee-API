from django.conf.urls import url

# import JWT
from .views import (
    FollowAPIView,
    UnFollowAPIView,
    FollowingUserView,
    FollowerUserView,
)

urlpatterns = [
    url(r'^follow/$', FollowAPIView.as_view(), name="follow_user"),
    url(r'^unfollow/$', UnFollowAPIView.as_view(), name="unfollow_user"),
    url(r'^following/(?P<user_id>\d+)/$', FollowingUserView.as_view(), name="unfollow_user"),
    url(r'^follower/(?P<user_id>\d+)/$', FollowerUserView.as_view(), name="unfollow_user"),
]
