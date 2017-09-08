"""stylee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

# import JWT
from .views import FacebookLogin

urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    # url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^profile/', include('profiles.urls', namespace="auth")),
    url(r'^stylebook/', include('outfit.urls', namespace="outfit")),
    url(r'^wardrobe/', include('cloth.urls', namespace="wardrobe")),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
]
