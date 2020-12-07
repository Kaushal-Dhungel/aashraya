from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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


        if password1 != password2:
            return Response({"Your password1 and password2 didn't match"},status=status.HTTP_400_BAD_REQUEST)

        else:
            if len(password1) < 8:
                return Response({"Your password must be atleast 8 characters long"},status=status.HTTP_400_BAD_REQUEST)
            
            try:
                user = User.objects.create_user(username, email, password1)
                uri = 'http://localhost:8000/auth/token'
                http_method='POST'
                body = {
                    'client_id' : '7GaNfuodxtkhUeVKHqE4ZAapgPwD4SwE0BQ5F9T0',
                    'client_secret' : '2Zt7tpt6R6osAgVlC5iRxgo7rUVT31PgOkcxfGENl1BJ29x4KGs0PvWmvPbd6edHB0JFlb2BaFhXcuYT6kEJav1bBHWQJwcFYhURpgoghpMuPlffveCsARTN9vhGtaKi',
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