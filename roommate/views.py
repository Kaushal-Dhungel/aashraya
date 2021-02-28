from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from django.http import Http404
from userprofile.models import Profile
from rest_framework import status
# Create your views here.

class RoomieView(APIView):

    def get(self,request,category,format= None):
        # snippets = Roomie.objects.all()
        city = request.query_params.get('city')
        priceRange = request.query_params.get('priceRange')
        print(city,priceRange)
        if priceRange == "0":
            snippets = Roomie.objects.filter(location_customised__iexact = city,category = category)
        
        else :
            snippets = Roomie.objects.filter(location_customised__iexact = city,category = category,price_range = priceRange)

        serializer = RoomieSerializer(snippets, many=True)
        return Response(serializer.data)

class ViewRoomie(APIView):
    def get(self,request,*args, **kwargs):
        profile = Profile.objects.get(user= request.user)
        snippets = Roomie.objects.filter(profile = profile )
        serializer = RoomieSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self,request,format = None):
        # print(request.data)
        # print(request.data.getlist('photos'))
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
            return Response(responses)

        except Exception as e:
            # print(e)
            return Response("Thats bad mate")



class RoomieDetailView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get_object(self, slug):
        try:
            return Roomie.objects.get(slug=slug)
        except Roomie.DoesNotExist:
            raise Http404


    def get(self, request,slug, format=None):
        snippets = self.get_object(slug)
        
        serializer = RoomieSerializer(snippets)
        
        return Response(serializer.data)

    
    def post(self,request, *args, **kwargs):
        
        item_id = request.data.get('item_id')
        roomie = Roomie.objects.get(id = item_id)

        if request.data.get('action') == 'remove_img':
            # print(request.data)
            img_id = request.data.get('img_id')
            # print(img_id,item_id)

            img = RoomieImage.objects.get(id = img_id)
            img.delete()

        
        else:
            # print(request.data)
            try:
                for img in request.data.getlist('photos'):
                    RoomieImage.objects.create(roomie = roomie,image = img)
            except Exception as e:
                # print(e)
                return Response({'sorry'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        serializer = RoomieSerializer(roomie)

        return Response(serializer.data)
      

# slug is changing everytime 
    def put(self,request,slug,*args, **kwargs):
        # print(slug)
        # print(request.data)
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
        # return Response()

class RoomiePostView(APIView):

    def get(self,request,slug,format= None):
        try:
            profile = Profile.objects.get(slug = slug)
            snippets = Roomie.objects.filter(profile = profile)
            serializer = RoomieSerializer(snippets,many = True)
            return Response(serializer.data)
        except Exception as e:
            # print(e)
            return Response([])

class RoomieCartView(APIView):

    def get(self,request,format = None):
        profile = Profile.objects.get(user = request.user.id)
        print(profile)
        snippets = RoomieCartItem.objects.filter(profile = profile)
        serializer = RoomieCartItemSerializer(snippets, many=True)
        return Response(serializer.data)

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

            else :
                return Response({"Already exists"})

        else:
            cart_item = RoomieCartItem.objects.get(item = item)
            cart_item.delete()
            return Response({"Removal Successful"},status=status.HTTP_201_CREATED)
