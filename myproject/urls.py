"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.views.static import serve
from django.conf.urls import url
from core.views import homeView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    # path('rest-auth/', include('rest_auth.urls')),
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),
    # path('rest-auth/twitter/', TwitterLogin.as_view(), name='twitter_login'),
    # path('accounts/', include('allauth.urls')),

	path('',homeView, name = "homeview"),
    path('core/', include('core.urls')),
    path('profile/', include('userprofile.urls')),
    path('items/', include('searchingapp.urls')),
    path('mates/', include('roommate.urls')),

    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),

]

if settings.DEBUG:
    # these serve the static and media files in development
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,{'document_root':settings.MEDIA_ROOT}), 
        url(r'^static/(?P<path>.*)$', serve,{'document_root':settings.STATIC_ROOT}), 
    ]