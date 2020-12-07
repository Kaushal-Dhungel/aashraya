from django.urls import path
from .views import *

urlpatterns = [
    path("<slug>/",ProfileView.as_view()),
    path("",UserProfileView.as_view()),
]
