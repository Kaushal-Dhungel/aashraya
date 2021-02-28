from rest_framework import serializers
from .models import *
# from userprofile.serializers import ProfileSerializer

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"   

class ItemSerializer(serializers.ModelSerializer):
    profile_slug = serializers.ReadOnlyField()
    images = ImageSerializer(many=True, read_only=True)
    class Meta:
        model = Item
        fields = "__all__"

    # def to_representation(self, instance):
    #     response=super().to_representation(instance)
    #     print("instance is")
    #     print(instance)
    #     response['profile']=ProfileSerializer(instance.profile).data
    #     return response

class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only = True)
    class Meta:
        model = CartItem
        fields = "__all__"  