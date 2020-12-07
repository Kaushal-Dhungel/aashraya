from rest_framework import serializers
from .models import *

class RoomieImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomieImage
        fields = "__all__"   

class RoomieSerializer(serializers.ModelSerializer):
    profile_slug = serializers.ReadOnlyField()
    images = RoomieImageSerializer(many=True, read_only=True)
    class Meta:
        model = Roomie
        fields = "__all__"
