from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from django.http import Http404

# Create your views here.

# class ProfileView(APIView):

#     def get(self,request,format= None):
#         # snippets = Items.objects.filter(category = category)
#         snippets = Profile.objects.all()
#         serializer = ProfileSerializer(snippets, many=True)
#         return Response(serializer.data)

class ProfileView(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get_object(self, slug):
        try:
            return Profile.objects.get(slug=slug)
        except Profile.DoesNotExist:
            raise Http404


    def get(self, request,slug, format=None):
        snippets = self.get_object(slug)
        
        serializer = ProfileSerializer(snippets)
        return Response(serializer.data)

class UserProfileView(APIView):
    def get(self,request,format = None):
        # print(request.user)
        profile = Profile.objects.get(user = request.user.id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)



    def post(self,request,*args, **kwargs):
        profile = Profile.objects.get(user = request.user.id)

        if request.data.get('action') == 'remove_pic':
            profile.avatar = 'avatar.png'
        
        else:
            profile.avatar = request.data.get('avatar')
        
        profile.save()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def patch(self,request,*args, **kwargs):
        # print(request.data)
        profile = Profile.objects.get(user = request.user.id)

        try:

            profile.first_name =  request.data.get('first_name') if request.data.get('first_name') is not '' else profile.first_name
            profile.last_name =  request.data.get('last_name') if request.data.get('last_name') is not '' else profile.last_name
            profile.email =  request.data.get('email') if request.data.get('email') is not '' else profile.email
            profile.phone =  request.data.get('phone') if request.data.get('phone') is not '' else profile.phone
            profile.avatar =  profile.avatar
            profile.facebook_link =  request.data.get('facebook_link') if request.data.get('facebook_link') is not '' else profile.facebook_link
            profile.twitter_link =  request.data.get('twitter_link') if request.data.get('twitter_link') is not '' else profile.twitter_link
            profile.instagram_link =  request.data.get('instagram_link') if request.data.get('instagram_link') is not '' else profile.instagram_link

            profile.save()
            return Response("Update is successful")
        
        except Exception as e:
            # print(e)   
            return Response("Update failed")
    