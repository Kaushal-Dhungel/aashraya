from django.urls import path
from .views import *

urlpatterns = [
    path("<category>/",ItemView.as_view()),
    path("details/<slug>/",ItemDetailView.as_view()),
    # path("image/img/",ImageView.as_view()),
    path("cartview",CartView.as_view()),
    path("",ViewItem.as_view()),

]
