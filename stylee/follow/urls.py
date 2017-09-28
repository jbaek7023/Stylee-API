from django.conf.urls import url

# import JWT
from .views import (
    FollowCreateAPIView,
)

urlpatterns = [
    url(r'^follow/$', FollowCreateAPIView.as_view(), name="follow_user"),
]
