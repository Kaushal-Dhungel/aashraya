from django.urls import path
from .views import *

urlpatterns = [
    path("<category>/",RoomieView.as_view(), name = 'roomieView'),
    path("details/<slug>/",RoomieDetailView.as_view(), name = 'roomieDetails'),
    # path("image/img/",ImageView.as_view()),
    path("",ViewRoomie.as_view(), name = 'viewRoomie'),
    path("roomie/<slug>/",RoomiePostView.as_view(), name = 'roomiePost'),
    path("roomiecart",RoomieCartView.as_view(), name = 'roomieCartView'),


]
