from django.conf.urls import url, include
from django.contrib import admin

from .views import OutfitListView, OutfitDetailView

urlpatterns = [
    url(r'^list/$', OutfitListView.as_view(), name="user_outfits_list"),
    url(r'^detail/(?P<pk>\d+)/$', OutfitDetailView.as_view(), name="outfit_detail"),    
    # url(r'^category/$', OutfitCategoryListView.as_view(), name="user_outfits_category_list"),
]
