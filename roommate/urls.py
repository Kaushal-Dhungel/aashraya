from django.urls import path
from .views import *

urlpatterns = [
    path("<category>/",RoomieFilterView.as_view(), name = 'roomieFilterView'),
    path("details/<slug>/",RoomieDetailView.as_view(), name = 'roomieDetails'),
    path("",RoomieView.as_view(), name = 'roomieView'),
    path("roomie/<slug>/",RoomiePostView.as_view(), name = 'roomiePost'),
    path("roomiecart",RoomieCartView.as_view(), name = 'roomieCartView'),


]
