from django.conf.urls import url, include
from django.contrib import admin

from .views import CommentListView, CommentDetailView

urlpatterns = [
    url(r'^list/$', CommentListView.as_view(), name="comments_list"),
    url(r'^detail/(?P<pk>\d+)/$', CommentDetailView.as_view(), name="outfit_detail"),
    # url(r'^category/$', OutfitCategoryListView.as_view(), name="user_outfits_category_list"),
]
