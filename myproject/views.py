from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

# from oauthlib.common import Request
from django.db import IntegrityError
import json
import requests

from django.shortcuts import render

def homeView (request,*args, **kwargs):
	return render(request, 'index.html')

class RegisterUser(APIView):

    def post(self,request,*args, **kwargs):
        # print(request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        client_id = request.data.get('client_id')
        client_secret = request.data.get('client_secret')

        if password1 != password2:
            return Response({"Your password1 and password2 didn't match"},status=status.HTTP_400_BAD_REQUEST)

        else:
            if len(password1) < 8:
                return Response({"Your password must be atleast 8 characters long"},status=status.HTTP_400_BAD_REQUEST)
            
            try:
                user = User.objects.create_user(username, email, password1)
                uri = 'https://aashraya.herokuapp.com/auth/token'

                if settings.DEBUG:
                    uri = 'http://localhost:8000/auth/token'

                http_method='POST'
                body = {
                    'client_id' : client_id,
                    'client_secret' : client_secret,
                    'grant_type' : 'password',
                    'username': username,
                    'password': password1,
                }
                # newrequest = Request(uri=uri,http_method=http_method,body=body)
                user.save()
                newreq = requests.post(uri,body)
                # print(newreq.json())
                return Response(newreq.json(),status= status.HTTP_201_CREATED)
            
            except IntegrityError:
                return Response({'Username Already Exists. Please Try New Username'},status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                # print(e)
                # print(e.__class__.__name__)
                return Response({"Unknown Error Occured. Please Try Later"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CheckUser(APIView):
    def get(self,request,*args,**kwargs):

        username = request.query_params.get('username')
        email = request.query_params.get('email')
        if email == '':
            try:
                User.objects.get(username = username)
                return Response({'True'},status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response({"False"},status = status.HTTP_200_OK)

            except Exception as e:
                print (e)
                return Response({'Some error occured'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            try:
                User.objects.get(email = email)
                return Response({'True'},status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response({"False"},status = status.HTTP_200_OK)

            except Exception as e:
                print (e)
                return Response({'Some error occured'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)