from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from django.contrib.auth.models import User


import os
from dotenv import load_dotenv
load_dotenv()

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
        return Response(serializer.data,status=status.HTTP_200_OK)

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
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self,request,*args, **kwargs):
        # print(request.data)
        profile = Profile.objects.get(user = request.user.id)

        try:

            profile.first_name =  request.data.get('first_name') if request.data.get('first_name') != '' else profile.first_name
            profile.last_name =  request.data.get('last_name') if request.data.get('last_name') != '' else profile.last_name
            profile.email =  request.data.get('email') if request.data.get('email') != '' else profile.email
            profile.phone =  request.data.get('phone') if request.data.get('phone') != '' else profile.phone
            profile.avatar =  profile.avatar
            profile.facebook_link =  request.data.get('facebook_link') if request.data.get('facebook_link') != '' else profile.facebook_link
            profile.twitter_link =  request.data.get('twitter_link') if request.data.get('twitter_link') != '' else profile.twitter_link
            profile.instagram_link =  request.data.get('instagram_link') if request.data.get('instagram_link') != '' else profile.instagram_link

            profile.save()
            return Response({"Update successful"},status=status.HTTP_200_OK)
        
        except Exception as e:
            # print(e)   
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
        

# class FbDataDeletionView(APIView):
#     def post(self, request, *args, **kwargs):
#         try:
#             signed_request = request.POST['signed_request']
#             encoded_sig, payload = signed_request.split('.')
#         except (ValueError, KeyError):
#             return Response(status=400, content='Invalid request')
 
#         try:
#             decoded_payload = base64.urlsafe_b64decode(payload + "==").decode('utf-8')
#             decoded_payload = json.loads(decoded_payload)
 
#             if type(decoded_payload) is not dict or 'user_id' not in decoded_payload.keys():
#                 return Response(status=400, content='Invalid payload data')
 
#         except (ValueError, json.JSONDecodeError):
#             return Response(status=400, content='Could not decode payload')
 
#         try:
#             secret = str(os.getenv('SOCIAL_AUTH_FACEBOOK_SECRET'))
 
#             sig = base64.urlsafe_b64decode(encoded_sig + "==")
#             expected_sig = hmac.new(bytes(secret, 'utf-8'), bytes(payload, 'utf-8'), hashlib.sha256)
#         except:
#             return Response(status=400, content='Could not decode signature')
 
#         if not hmac.compare_digest(expected_sig.digest(), sig):
#             return Response(status=400, content='Invalid request')
 
#         user_id = decoded_payload['user_id']
 
#         try:
#             # now you get facebook user id. you can delete its details from your database like below.
#             user_account = FacebookUserModel.objects.filter(fb_userid=user_id).delete()
#         except FacebookLoginDetails.DoesNotExist:
#             return Response(status=200)
 
        # Own custom logic here
 
        # return Response(status=200)