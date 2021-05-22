from django.urls import path
from .views import *

urlpatterns = [
    path('popular/',PopularView.as_view(), name = 'popular'),
    path('testimonial/',TestimonialView.as_view(), name = 'testimonial'),

]