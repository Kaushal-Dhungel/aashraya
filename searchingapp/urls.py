from django.urls import path
from .views import *

urlpatterns = [
    path("<category>/",ItemsFilterView.as_view(),name = 'itemFilterView'),
    path("",ItemView.as_view(),name = 'itemView'),
    path("details/<slug>/",ItemDetailView.as_view(), name = 'itemDetails'),
    path("cartview",CartView.as_view(),name = 'cartview'),

]
