from django.urls import path
from .views import *

urlpatterns = [
    path("<category>/",ItemView.as_view(),name = 'itemView'),
    path("details/<slug>/",ItemDetailView.as_view(), name = 'itemDetails'),
    # path("image/img/",ImageView.as_view()),
    path("cartview",CartView.as_view(),name = 'cartview'),
    path("",ViewItem.as_view(),name = 'viewItem'),

]
