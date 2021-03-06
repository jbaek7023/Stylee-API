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
    ProfileImageChangeView,
    SearchProfileListView,
    NotificationAPIView,
)

urlpatterns = [
    url(r'^detail/$', UserDetailView.as_view(), name="user_profile"),
    url(r'^search/$', SearchProfileListView.as_view(), name="search_user"),
    url(r'^notifications/(?P<page>\d+)/$', NotificationAPIView.as_view(), name="user_notification"),
    url(r'^edit/$', ProfileEditAPIView.as_view(), name="edit_profile"),
    url(r'^emailedit/$', EmailEditAPIView.as_view(), name="edit_email"),
    url(r'^page/$', ProfilePageView.as_view(), name="profile_page"),
    url(r'^pageid/(?P<user_id>\d+)/$', ProfilePageByIdView.as_view(), name="profile_page_id"),
    url(r'^echeck/$', UserCheckEmail.as_view(), name="user_email_check"),
    url(r'^update/$', ProfileRetrieveAndUpdateProfile.as_view(), name="profile_retrieve_update"),
    url(r'^updateimg/$', ProfileImageChangeView.as_view(), name="profile_change_img"),
    url(r'^unamecheck/$', UserCheckUsername.as_view(), name="user_username_check"),
]
