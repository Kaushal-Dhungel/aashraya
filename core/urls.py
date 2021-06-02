from django.urls import path
from .views import *

urlpatterns = [
    path('registeruser/', RegisterUser.as_view(),name = 'register'),
    path('checkuser/', CheckUser.as_view(), name = 'checkuser'),
    path('popular/',PopularView.as_view(), name = 'popular'),
    path('testimonial/',TestimonialView.as_view(), name = 'testimonial'),
]