from django.urls import path
from .views import *

urlpatterns = [
    path("<category>/",RoomieView.as_view()),
    path("details/<slug>/",RoomieDetailView.as_view()),
    # path("image/img/",ImageView.as_view()),
    path("",ViewRoomie.as_view()),
    path("roomie/<slug>/",RoomiePostView.as_view()),
    path("roomiecart",RoomieCartView.as_view()),


]
