from django.conf.urls import url

# import JWT
from .views import (
    # ProfileDetailViewByUser,
    UserDetailView,
    ProfileRetrieveAndUpdateProfile,
    UserCheckEmail,
    UserCheckUsername,
    ProfilePageView,
)

urlpatterns = [
    url(r'^detail/$', UserDetailView.as_view(), name="user_profile"),
    url(r'^page/$', ProfilePageView.as_view(), name="profile_page"),
    url(r'^echeck/$', UserCheckEmail.as_view(), name="user_email_check"),
    url(r'^update/$', ProfileRetrieveAndUpdateProfile.as_view(), name="profile_retrieve_update"),
    url(r'^unamecheck/$', UserCheckUsername.as_view(), name="user_username_check"),
]
