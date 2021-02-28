from rest_framework import serializers
from .models import *

class PopularSerializer(serializers.ModelSerializer):
    class Meta:
        model = Popular
        fields = "__all__"   

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = "__all__"   