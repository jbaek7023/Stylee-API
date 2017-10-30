from django.conf.urls import url

from .views import (
    # ProfileDetailViewByUser,
    UserDetailView,
    ProfileRetrieveAndUpdateProfile,
    UserCheckEmail,
    UserCheckUsername,
    ProfilePageView,
    ProfilePageByIdView,
    ProfileEditAPIView,
    EmailEditAPIView,
)

urlpatterns = [
    url(r'^detail/$', UserDetailView.as_view(), name="user_profile"),
    url(r'^edit/$', ProfileEditAPIView.as_view(), name="edit_profile"),
    url(r'^emailedit/$', EmailEditAPIView.as_view(), name="edit_email"),
    url(r'^page/$', ProfilePageView.as_view(), name="profile_page"),
    url(r'^pageid/(?P<user_id>\d+)/$', ProfilePageByIdView.as_view(), name="profile_page_id"),
    url(r'^echeck/$', UserCheckEmail.as_view(), name="user_email_check"),
    url(r'^update/$', ProfileRetrieveAndUpdateProfile.as_view(), name="profile_retrieve_update"),
    url(r'^unamecheck/$', UserCheckUsername.as_view(), name="user_username_check"),
]
