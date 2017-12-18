from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework import status
from base64 import b64decode
from django.core.files.base import ContentFile
import base64

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

import random
import string

from .serializers import (
    UserMenuSerializer,
    UserEmailSerizlier,
    ProfileRetrieveAndUpdateSerializer,
    ProfilePageSerializer,
    ProfileEditSerializer,
    UserAccountSerializer,
    # ProfilePageByIdSerializer
    UserRowSerializer,
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from .models import Profile
from stream_django.feed_manager import feed_manager

User = get_user_model()
import datetime
from stream_django.enrich import Enrich
enricher = Enrich()

class NotificationAPIView(APIView):
    def get(self, request, format=None):
        feeds = feed_manager.get_notification_feed(request.user.id)
        notifications = feeds.get(limit=25, mark_seen='all')['results']
        enriched_activities = enricher.enrich_aggregated_activities(notifications)
        feed = []
        # for activity in enriched_activities:
        #     activity_dict = activity.__dict__
        #     activity_type = activity_dict.get('verb')
        #     activity_time = activity_dict.get('updated_at')
        #     feed_object = None
            # if activity_type is 'comment':
            #     # user(last).image, updated_at,
            #     # ( username, user_id ), (username, user_id) commented on 'style_title', 'outfit_id'. (or cloth_title, cloth_id
            #     # target(object).content
            #     for small_activity in activity_dict.activities:
            #         small_activity_dict = activity.__dict__
            #         actor = small_activity_dict.get('actor')
            #         # content type & id
            #         obj = small_activity_dict.get('object')
            #         # obj_instnace = # obj.content_type & object_id
            #     # feed_object = small_activity_dict.get('object').
            #
            #     # {users: [{id: 5, username: 'michaelvozm_d'}, {id: 1, username: 'jbaek72'}], image: 'https:', updated_at:timeline,
            #     # title, id, content}
            # elif activity_type is 'like':
            #     # user(last).image, updated_at,
            #     # ( username, user_id ), (username, user_id) liked on 'style_title', 'outfit_id'. (or cloth_title, cloth_id)
            #     # target(object).content
            #     for small_activity in activity_dict.activities:
            #         small_activity_dict = activity.__dict__
            #         actor = small_activity_dict.get('actor')
            #         # content type & id
            #         obj = small_activity_dict.get('object')
            #         # obj_instnace = # obj.content_type & object_id
            # elif activity_type is 'follow':
            #     # user(last).image, updated_at,
            #     # ( username, user_id ), (username, user_id) started to following you
            #     for small_activity in activity_dict.activities:
            #         small_activity_dict = activity.__dict__
            #         actor = small_activity_dict.get('actor')
            #         # content type & id
            #         obj = small_activity_dict.get('object')
            #         # obj_instnace = # obj.content_type & object_id
            #
            # feed.append(feed_object)

        print(enriched_activities)
        json_output = { "feed" : 'feed' }
        return Response(json_output, status=status.HTTP_200_OK)

# allow only logged in user
class SearchProfileListView(generics.ListAPIView):
    serializer_class = UserRowSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username']
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset_list = User.objects.all()
        return queryset_list

class ProfileImageChangeView(APIView):
    def post(self, request, format=None):
        base_img_data = self.request.data.get('base64')
        profile_img = ContentFile(base64.b64decode(base_img_data), name='temp.jpg')

        qs = Profile.objects.all()
        logged_in_user_profile = qs.filter(user=self.request.user)
        profile_instance = logged_in_user_profile.first()
        if profile_instance is not None:
            profile_instance.profile_img = profile_img
            profile_instance.save()
            print(str(datetime.datetime.now()))
            json_output = {"changed": str(datetime.datetime.now())}
            return Response(json_output, status=status.HTTP_200_OK)
        else:
            email = create_unique_username(email)
            json_output = {"username": email}
            return Response(json_output, status=status.HTTP_200_OK)

# /profile/detail/
class UserDetailView(generics.ListAPIView):
    serializer_class = UserMenuSerializer

    def get_queryset(self):
        qs = Profile.objects.all()
        logged_in_user_profile = qs.filter(user=self.request.user)
        return logged_in_user_profile

class ProfilePageView(generics.RetrieveAPIView):
    serializer_class = ProfilePageSerializer

    def get_queryset(self):
        logged_in_user = User.objects.filter(username=self.request.user.username)
        return logged_in_user

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj


class EmailEditAPIView(UpdateModelMixin, generics.RetrieveAPIView):
    serializer_class = UserEmailSerizlier

    def get_queryset(self):
        logged_in_user = User.objects.filter(id=self.request.user.id)
        return logged_in_user

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class ProfilePageByIdView(generics.RetrieveAPIView):
    serializer_class = ProfilePageSerializer

    def get_queryset(self):
        uid = self.kwargs['user_id']
        User = get_user_model()
        profile_user = User.objects.filter(id=uid)
        # logged_in_user = User.objects.filter(username=self.request.user.username)
        return profile_user

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj


# EDIT
class ProfileEditAPIView(UpdateModelMixin, generics.RetrieveAPIView):
    serializer_class = ProfileEditSerializer

    def get_queryset(self):
        logged_in_user = User.objects.filter(id=self.request.user.id)
        return logged_in_user

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj.profile

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

# profile/update/<user_id> # only allow to logged in user (SECURE)
class ProfileRetrieveAndUpdateProfile(generics.RetrieveUpdateAPIView):
    """
    PUT : Edit
    GET : Retrieve Profile
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileRetrieveAndUpdateSerializer

    def get_queryset(self):
        qs = Profile.objects.all()
        logged_in_user_profile = qs.filter(user=self.request.user)
        return logged_in_user_profile

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_unique_username(username):
    #split @
    if '@' in username:
        part = username.split('@')
        username = part[0]
    # We only allow lower case for the username but just in case
    username = username.lower()

    ## Delete the username on Profile! (later Task)
    exists = User.objects.filter(username=username).exists()
    if exists:
        new_username = "%s%s" % (username, random_string_generator(size=1))
        return create_unique_username(username=new_username)
    return username

class UserCheckEmail(APIView):
    # CHECK username or email is valid
    # 200; obtained -> the email is already obtained
    # 200; username -> jbaek70233 is valid username

    def get(self, request, format=None):
        qs = User.objects.all()
        email = self.request.GET.get("em")
        if email:
            qs = qs.filter(
                Q(email__exact=email)
            ).distinct()

        if(len(qs)==1):
            json_output = {"obtained": 0}
            return Response(json_output, status=status.HTTP_200_OK)
        else:
            email = create_unique_username(email)
            json_output = {"username": email}
            return Response(json_output, status=status.HTTP_200_OK)

class UserCheckUsername(APIView):
    def get(self, request, format=None):
        qs = User.objects.all()
        username = self.request.GET.get("un")
        if username:
            qs = qs.filter(
                Q(username__exact=username)
            ).distinct()
        if(len(qs)==1):
            json_output = {"obtained": True}
            return Response(json_output)
        else:
            json_output = {"obtained": False}
            return Response(json_output)
