from rest_framework import serializers
from .models import *
from searchingapp.serializers import ItemSerializer

class ProfileSerializer(serializers.ModelSerializer):
    get_username = serializers.ReadOnlyField()
    get_email = serializers.ReadOnlyField()

    item_model = ItemSerializer(many=True, read_only=True)
    class Meta:
        model = Profile
        fields = "__all__"