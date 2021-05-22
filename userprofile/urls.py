from django.urls import path
from .views import *

urlpatterns = [
    path("<slug>/",ProfileView.as_view(),name = 'profileview'),
    path("",UserProfileView.as_view(), name = 'userprofileview'),
]
