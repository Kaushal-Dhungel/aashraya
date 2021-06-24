from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from django.http import Http404
from userprofile.models import Profile
from rest_framework import status


class RoomieFilterView(APIView):
    """
    For filtering the roomie using City and Price Range 
    """
    def get(self,request,category,format= None):
        city = request.query_params.get('city')
        price_range = request.query_params.get('priceRange')
        
        if price_range == "0":
            snippets = Roomie.objects.filter(location_customised__iexact = city,category = category)
        
        else :
            snippets = Roomie.objects.filter(location_customised__iexact = city,category = category,price_range = price_range)

        serializer = RoomieSerializer(snippets, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class RoomieView(APIView):

    # this get is for fetching the roomies for userprofile component
    def get(self,request,*args, **kwargs):
        profile = Profile.objects.get(user= request.user)
        snippets = Roomie.objects.filter(profile = profile )
        serializer = RoomieSerializer(snippets, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    # this is for creating/listing a roomie 
    def post(self,request,format = None):
        profile = Profile.objects.get(user = request.user.id)

        newdict = {
            'profile': profile.id,
            'category': request.data['category'],
            'headline': request.data['headline'],
            'location': request.data['location'],
            'location_customised' : 'random',
            'latitude': request.data['latitude'],
            'longitude': request.data['longitude'],
            'price_range': request.data['price_range'],
            'sex_pref': request.data['sex_pref'],
            'age_pref': request.data['age_pref'],
            'details': request.data['details'],
            'slug': 'abc',            
        }

        try:
            serializer = RoomieSerializer(data = newdict)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            for img in request.data.getlist('photos'):   
                imgdict = {
                    'roomie' : serializer.data['id'],
                    'image': img,
                }

                img_serializer = RoomieImageSerializer(data =imgdict)
                img_serializer.is_valid(raise_exception=True)
                img_serializer.save()

            responses = {
                "slug" : serializer.data['slug'],
                "text" : "Addtion successful"
            }
            return Response(responses,status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response("Thats bad mate",status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RoomieDetailView(APIView):
    def get_object(self, slug):
        try:
            return Roomie.objects.get(slug=slug)
        except Roomie.DoesNotExist:
            raise Http404

    def get(self, request,slug, format=None):
        snippets = self.get_object(slug)
        serializer = RoomieSerializer(snippets)
        return Response(serializer.data,status=status.HTTP_200_OK)

    # this is for adding/removing the images of roomie
    def post(self,request, *args, **kwargs):
        item_id = request.data.get('item_id')
        roomie = Roomie.objects.get(id = item_id)

        if request.data.get('action') == 'remove_img':
            img_id = request.data.get('img_id')
            img = RoomieImage.objects.get(id = img_id)
            img.delete()
        
        else:
            try:
                for img in request.data.getlist('photos'):
                    RoomieImage.objects.create(roomie = roomie,image = img)
            except Exception as e:
                return Response({'sorry'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = RoomieSerializer(roomie)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def delete(self,request,slug,*args, **kwargs):
        try:
            roomie = Roomie.objects.get(slug = slug)
            roomie.delete()
            return Response({'deleted'}, status=status.HTTP_200_OK)

        except Exception as e:
            print (e)
            return Response({'sorry'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # slug is changing everytime 
    def put(self,request,slug,*args, **kwargs):
        item = Roomie.objects.get(slug = slug)
        profile = Profile.objects.get(user = request.user.id)

        newdict = {
            'profile': profile.id,
            'category': request.data['category'],
            'headline': request.data['headline'],
            'location': request.data['location'],
            'location_customised' : item.location_customised,
            'latitude': request.data['latitude'],
            'longitude': request.data['longitude'],
            'price_range': request.data['price_range'],
            'sex_pref': request.data['sex_pref'],
            'age_pref': request.data['age_pref'],
            'details': request.data['details'],
            'slug': item.slug,            
        }
        serializer = RoomieSerializer(item,data= newdict)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoomiePostView(APIView):
    """
    This is for fetching roomie in profile(not for userprofile) component using slug, 
    because items(rooms,flats etc) are fetched by default when the profile component is rendered.
    """
    def get(self,request,slug,format= None):
        try:
            profile = Profile.objects.get(slug = slug)
            snippets = Roomie.objects.filter(profile = profile)
            serializer = RoomieSerializer(snippets,many = True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response([],status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RoomieCartView(APIView):
    def get(self,request,format = None):
        profile = Profile.objects.get(user = request.user.id)
        snippets = RoomieCartItem.objects.filter(profile = profile)
        serializer = RoomieCartItemSerializer(snippets, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args, **kwargs):
        item_id = request.data.get('id')
        action = request.data.get("action")
        item = Roomie.objects.get(id = item_id)
        profile = Profile.objects.get(user = request.user.id)
        
        if action == "add":
            cart_item, is_created = RoomieCartItem.objects.get_or_create(item = item, profile = profile)
            
            if is_created:
                serializer = RoomieCartItemSerializer(cart_item)
                return Response(serializer.data,status=status.HTTP_201_CREATED)

            else:
                return Response({"Already exists"},status=status.HTTP_201_CREATED)

        else:
            cart_item = RoomieCartItem.objects.get(item = item)
            cart_item.delete()
            return Response({"Removal Successful"},status=status.HTTP_200_OK)
