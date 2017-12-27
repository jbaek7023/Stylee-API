from django.shortcuts import render
from re import sub
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.authtoken.models import Token
from .models import Outfit
from cloth.models import Cloth
from category.models import Category
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from base64 import b64decode
from django.core.files.base import ContentFile
from stream_django.enrich import Enrich
from stream_django.feed_manager import feed_manager
from django.db.models import Count
import base64
import datetime
from .serializers import (
    OutfitListSerializer,
    OutfitDetailSerializer,
    OutfitDetailCommentSerializer,
    OutfitDetailLikeSerializer,
    OutfitCreateSerializer,
    OutfitDetailFeedSerializer,
    CategoryListOnOutfitSerializer,
)

from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)
from .pagination import OutfitPagination, CategoryPagination, OutfitByCategoryPagination


from comments.serializers import CommentSerializer
enricher = Enrich()

class StyleFeedAPIView(APIView):
    def get(self, request, page=0, format=None):
        page = self.kwargs['page']
        if not page:
            page_num = 0
        else:
            page_num = int(page)* 24
        feeds = feed_manager.get_news_feeds(request.user.id)
        activities = feeds.get('timeline').get(limit=24, offset=page_num)['results']
        activities = enricher.enrich_activities(activities)
        feed = []
        for activity in activities:
            outfit_instance = activity.__dict__.get('activity_data').get('object')
            if outfit_instance:
                data = OutfitDetailFeedSerializer(
                    outfit_instance,
                    context={'request': request}).data
                feed.append(data)
        json_output = feed
        return Response(json_output, status=status.HTTP_200_OK)

class OutfitListByCategoryId(generics.ListAPIView):
    serializer_class = OutfitListSerializer
    pagination_class = OutfitByCategoryPagination

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        category_qs = Category.objects.filter(id=category_id)
        if category_qs:
            category_instance = category_qs.first()
            if category_instance:
                qs = Outfit.objects.filter(categories=category_instance)
                return qs
        return Outfit.objects.none()

class PopularFeedAPIView(generics.ListAPIView):
    serializer_class = OutfitDetailFeedSerializer
    pagination_class = OutfitPagination

    # User Profile 에 나오는 거 Page 따라하기.
    def get_queryset(self):
        today = datetime.date.today()
        # qs = Outfit.objects.filter(created_at__gte=today)
        qs = Outfit.objects.filter(only_me=False).annotate(like_count=Count('likes')).order_by('-like_count')
        # order_by created_at '-created_at'
        return qs

class OutfitCreateAPIView(APIView):
    def post(self, request, format='multipart/form-data'):
        # Create Outfits
        content = self.request.data.get('name')
        base_img_data = self.request.data.get('base64')
        outfit_img = ContentFile(base64.b64decode(base_img_data), name='temp.jpg')
        gender = self.request.data.get('gender')
        location = self.request.data.get('location')
        description = self.request.data.get('description')
        only_me = self.request.data.get('onlyMe')
        link=self.request.data.get('link')

        outfit_instance = Outfit(
            user=self.request.user,
            content=content,
            outfit_img=outfit_img,
            gender=gender,
            location=location,
            description=description,
            only_me=only_me,
            link=link
        )
        outfit_instance.save()

        tagged_categories = self.request.data.get('taggedCategories')
        for category_id in tagged_categories:
            category_instance = Category.objects.get(id=category_id, owner=self.request.user)
            if category_instance is not None:
                category_instance.outfits.add(outfit_instance)
        cloth_ids = self.request.data.get('selectedClothesIds')

        for cloth_id in cloth_ids:
            cloth_instance = Cloth.objects.get(id=cloth_id, user=self.request.user)
            if cloth_instance is not None:
                outfit_instance.tagged_clothes.add(cloth_instance)

        tagged_clothes = self.request.data.get('taggedClothes')

        for tagged_cloth in tagged_clothes:
            image_base = tagged_cloth.get('base64')
            cloth_image = ContentFile(base64.b64decode(image_base), name='temp.jpg')
            print(cloth_image)
            new_cloth_instance = Cloth(
                user=self.request.user,
                cloth_image=cloth_image
            )
            new_cloth_instance.save()

            cloth_content = tagged_cloth.get('name')
            if cloth_content is not None:
                new_cloth_instance.content = cloth_content

            cloth_type = tagged_cloth.get('clothType')
            if cloth_type is not None:
                new_cloth_instance.cloth_type = cloth_type

            in_wardrobe = tagged_cloth.get('inWardrobe')
            if in_wardrobe is not None:
                new_cloth_instance.in_wardrobe = in_wardrobe

            only_me = tagged_cloth.get('onlyMe')
            if only_me is not None:
                new_cloth_instance.only_me = only_me

            gender = tagged_cloth.get('gender')
            if gender is not None:
                new_cloth_instance.gender = gender

            seasons = tagged_cloth.get('selectedSeasonIds')
            if seasons is not None:
                new_cloth_instance.seasons = seasons

            size = tagged_cloth.get('selectedSizeIds')
            if size is not None:
                new_cloth_instance.size = size

            color = tagged_cloth.get('selectedColorIds')
            if color is not None:
                new_cloth_instance.color = color
            outfit_instance.tagged_clothes.add(new_cloth_instance)

        # Tag Clothes to the Outfits
        json_output = {"success": True, "created": outfit_instance.created_at }
        return Response(json_output, status=status.HTTP_201_CREATED)

class OutfitCreateAPIView(APIView):
    def post(self, request, format='multipart/form-data'):
        # Create Outfits
        content = self.request.data.get('name')
        base_img_data = self.request.data.get('base64')
        outfit_img = ContentFile(base64.b64decode(base_img_data), name='temp.jpg')
        gender = self.request.data.get('gender')
        location = self.request.data.get('location')
        description = self.request.data.get('description')
        only_me = self.request.data.get('onlyMe')
        link=self.request.data.get('link')

        outfit_instance = Outfit(
            user=self.request.user,
            content=content,
            outfit_img=outfit_img,
            gender=gender,
            location=location,
            description=description,
            only_me=only_me,
            link=link
        )
        outfit_instance.save()

        tagged_categories = self.request.data.get('taggedCategories')
        for category_id in tagged_categories:
            category_instance = Category.objects.get(id=category_id, owner=self.request.user)
            if category_instance is not None:
                category_instance.outfits.add(outfit_instance)
        cloth_ids = self.request.data.get('selectedClothesIds')

        for cloth_id in cloth_ids:
            cloth_instance = Cloth.objects.get(id=cloth_id, user=self.request.user)
            if cloth_instance is not None:
                outfit_instance.tagged_clothes.add(cloth_instance)

        tagged_clothes = self.request.data.get('taggedClothes')

        for tagged_cloth in tagged_clothes:
            image_base = tagged_cloth.get('base64')
            cloth_image = ContentFile(base64.b64decode(image_base), name='temp.jpg')
            print(cloth_image)
            new_cloth_instance = Cloth(
                user=self.request.user,
                cloth_image=cloth_image
            )
            new_cloth_instance.save()

            cloth_content = tagged_cloth.get('name')
            if cloth_content is not None:
                new_cloth_instance.content = cloth_content

            cloth_type = tagged_cloth.get('clothType')
            if cloth_type is not None:
                new_cloth_instance.cloth_type = cloth_type

            in_wardrobe = tagged_cloth.get('inWardrobe')
            if in_wardrobe is not None:
                new_cloth_instance.in_wardrobe = in_wardrobe

            only_me = tagged_cloth.get('onlyMe')
            if only_me is not None:
                new_cloth_instance.only_me = only_me

            gender = tagged_cloth.get('gender')
            if gender is not None:
                new_cloth_instance.gender = gender

            seasons = tagged_cloth.get('selectedSeasonIds')
            if seasons is not None:
                new_cloth_instance.seasons = seasons

            size = tagged_cloth.get('selectedSizeIds')
            if size is not None:
                new_cloth_instance.size = size

            color = tagged_cloth.get('selectedColorIds')
            if color is not None:
                new_cloth_instance.color = color
            outfit_instance.tagged_clothes.add(new_cloth_instance)

        # Tag Clothes to the Outfits
        json_output = {"success": True, "created": outfit_instance.created_at }
        return Response(json_output, status=status.HTTP_201_CREATED)

class OutfitEditAPIView(APIView):
    def put(self, request, format='multipart/form-data'):
        # Create Outfits
        oid = self.request.data.get('oid')
        qs = Outfit.objects.filter(id=oid)
        if not qs:
            json_output = {"success": False }
            return Response(json_output, status=status.HTTP_404_NOT_FOUND)
        outfit_instance = qs.first()
        if outfit_instance:
            content = self.request.data.get('name')
            gender = self.request.data.get('gender')
            location = self.request.data.get('location')
            description = self.request.data.get('description')
            only_me = self.request.data.get('onlyMe')
            link=self.request.data.get('link')

            outfit_instance.content = content
            outfit_instance.gender = gender
            outfit_instance.location = location
            outfit_instance.description = description
            outfit_instance.only_me = only_me
            outfit_instance.link = link
            outfit_instance.save()

            cloth_ids = self.request.data.get('selectedClothesIds')
            for cloth_id in cloth_ids:
                cloth_qs = Cloth.objects.filter(id=cloth_id)
                cloth_instance = None
                if cloth_qs:
                    cloth_instance = cloth_qs.first()
                if cloth_instance is not None:
                    outfit_instance.tagged_clothes.add(cloth_instance)

            tagged_clothes = self.request.data.get('taggedClothes')
            for tagged_cloth in tagged_clothes:
                image_base = tagged_cloth.get('base64')
                cloth_image = ContentFile(base64.b64decode(image_base), name='temp.jpg')
                new_cloth_instance = Cloth(
                    user=self.request.user,
                    cloth_image=cloth_image
                )
                new_cloth_instance.save()

                cloth_content = tagged_cloth.get('name')
                if cloth_content is not None:
                    new_cloth_instance.content = cloth_content

                cloth_type = tagged_cloth.get('clothType')
                if cloth_type is not None:
                    new_cloth_instance.cloth_type = cloth_type

                in_wardrobe = tagged_cloth.get('inWardrobe')
                if in_wardrobe is not None:
                    new_cloth_instance.in_wardrobe = in_wardrobe

                only_me = tagged_cloth.get('onlyMe')
                if only_me is not None:
                    new_cloth_instance.only_me = only_me

                gender = tagged_cloth.get('gender')
                if gender is not None:
                    new_cloth_instance.gender = gender

                seasons = tagged_cloth.get('selectedSeasonIds')
                if seasons is not None:
                    new_cloth_instance.seasons = seasons

                size = tagged_cloth.get('selectedSizeIds')
                if size is not None:
                    new_cloth_instance.size = size

                color = tagged_cloth.get('selectedColorIds')
                if color is not None:
                    new_cloth_instance.color = color
                outfit_instance.tagged_clothes.add(new_cloth_instance)
            json_output = {"success": True, "updated": outfit_instance.created_at }
            return Response(json_output, status=status.HTTP_200_OK)
        else:
            json_output = {"success": False }
            return Response(json_output, status=status.HTTP_404_NOT_FOUND)
        # Tag Clothes to the Outfits




class AddOutfitOnCategory(APIView):
    def post(self, request, format=None):
        outfit_id = self.request.data.get('outfit_id')
        outfit_instance = Outfit.objects.filter(id=outfit_id).first()
        if outfit_instance is not None:
            category_id = self.request.data.get('category_id')
            category_instance = Category.objects.filter(
                id=category_id,
                owner=self.request.user).first()
            if category_instance is not None:
                category_instance.outfits.add(outfit_instance)
                # if category_instance.main_img is None:
                #     category_instance.main_img = outfit_instance.outfit_img
                json_output = {"success": True, "added": category_instance.name }
                return Response(json_output, status.HTTP_201_CREATED)
            else:
                json_output = {"success": False}
                return Response(json_output, status.HTTP_409_CONFLICT)
        else:
            json_output = {"success": False}
            return Response(json_output, status.HTTP_409_CONFLICT)

class DeleteOutfitOnCategory(APIView):
    def post(self, request, format=None):
        outfit_id = self.request.data.get('outfit_id')
        outfit_instance = Outfit.objects.filter(id=outfit_id).first()
        if outfit_instance is not None:
            category_id = self.request.data.get('category_id')
            category_instance = Category.objects.filter(
                id=category_id,
                owner=self.request.user).first()

            print(category_instance)
            if category_instance is not None:
                category_name = category_instance.name
                category_instance.outfits.remove(outfit_instance)
                # if category_instance.main_img is None:
                #     category_instance.main_img = outfit_instance.outfit_img
                json_output = {"success": True, "removed": category_name }
                return Response(json_output, status.HTTP_200_OK)
            else:
                json_output = {"success": False}
                return Response(json_output, status.HTTP_409_CONFLICT)

        else:
            json_output = {"success": False}
            return Response(json_output, status.HTTP_409_CONFLICT)

# Create your views here.
class OutfitListView(generics.ListAPIView):
    serializer_class = OutfitListSerializer
    pagination_class = OutfitPagination

    def get_queryset(self):
        qs = Outfit.objects.all(user=self.request.user)
        logged_in_user_profile = qs.filter(user=self.request.user)
        # if undefined user, return 404.(later)
        return logged_in_user_profile

class OutfitListByIdView(generics.ListAPIView):
    serializer_class = OutfitListSerializer
    pagination_class = OutfitPagination

    def get_queryset(self):
        uid = self.kwargs['user_id']
        User = get_user_model()
        outfit_owner = User.objects.filter(id=uid).first()

        # this is wrong.
        qs = Outfit.objects.all(user=self.request.user)
        # This is not quite.
        qs = qs.filter(user=outfit_owner)
        return qs

class ProfileOutfitListNext(generics.ListAPIView):
    serializer_class = OutfitDetailFeedSerializer
    pagination_class = CategoryPagination

    def get_queryset(self):
        uid = self.kwargs['user_id']
        User = get_user_model()
        outfit_owner = User.objects.filter(id=uid).first()

        # this is wrong.
        qs = Outfit.objects.filter(user=outfit_owner)
        if outfit_owner != self.request.user:
            qs = qs.filter(only_me=False)
        return qs

# Requires [{JWT or Bearer Token} AND outfit_id
# Returns Outfit fields
class OutfitDetailView(generics.RetrieveAPIView):
    serializer_class = OutfitDetailSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = Outfit.objects.all(user=self.request.user)
        return qs

class CategoryListOnOutfitView(generics.RetrieveAPIView):
    serializer_class = CategoryListOnOutfitSerializer
    lookup_field = 'pk'
    pagination_class = CategoryPagination

    def get_queryset(self):
        qs = Outfit.objects.all(user=self.request.user)
        return qs

# Requires [{JWT or Bearer Token} AND outfit_id
# Returns Outfit fields
# By Id
class OutfitFeedListView(generics.ListAPIView):
    serializer_class = OutfitDetailFeedSerializer

    def get_queryset(self):
        uid = self.kwargs['user_id']
        User = get_user_model()
        outfit_owner = User.objects.filter(id=uid).first()
        # this is wrong.
        qs = Outfit.objects.all(user=self.request.user)
        # This is not quite.
        qs = qs.filter(user=outfit_owner)
        return qs

class OutfitEditView(DestroyModelMixin, UpdateModelMixin, generics.RetrieveAPIView):
    serializer_class = OutfitDetailSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = Outfit.objects.all(user=self.request.user)
        return qs

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class OutfitDetailCommentsView(generics.RetrieveAPIView):
    serializer_class = OutfitDetailCommentSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = Outfit.objects.all(user=self.request.user)
        return qs

class OutfitDetailLikesView(generics.RetrieveAPIView):
    serializer_class = OutfitDetailLikeSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = Outfit.objects.all(user=self.request.user)
        return qs
