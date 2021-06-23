from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from django.contrib.auth.models import User
import os

# to view the profile of the user who listed the item, if the user is not you
class ProfileView(APIView):
    def get_object(self, slug):
        try:
            return Profile.objects.get(slug=slug)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request,slug, format=None):
        snippets = self.get_object(slug)
        serializer = ProfileSerializer(snippets)
        return Response(serializer.data,status=status.HTTP_200_OK)

# for your profile
class UserProfileView(APIView):
    def get(self,request,format = None):
        profile = Profile.objects.get(user = request.user.id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    #  this is not to create the profile but for adding/removing the display pic, profile gets created automatically
    def post(self,request,*args, **kwargs):
        profile = Profile.objects.get(user = request.user.id)

        if request.data.get('action') == 'remove_pic':
            profile.avatar = 'avatar.png'
        
        else:
            profile.avatar = request.data.get('avatar')
        
        profile.save()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self,request,*args, **kwargs):
        profile = Profile.objects.get(user = request.user.id)
        try:
            profile.first_name =  request.data.get('first_name',profile.first_name) 
            profile.last_name =  request.data.get('last_name',profile.last_name) 
            profile.email =  profile.email if request.data.get('get_email') == "" else request.data.get('get_email')
            profile.phone =  request.data.get('phone',profile.phone) 
            profile.avatar =  profile.avatar
            profile.facebook_link =  request.data.get('facebook_link',profile.facebook_link) 
            profile.twitter_link =  request.data.get('twitter_link',profile.twitter_link)
            profile.instagram_link =  request.data.get('instagram_link',profile.instagram_link) 

            profile.save()
            return Response({"Update successful"},status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"Update failed"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user = request.user.id)
            user = User.objects.get(profile__id = profile.id)
            user.delete()
            return Response({"Deleted"},status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"Deletion failed"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)