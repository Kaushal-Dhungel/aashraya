from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from django.http import Http404, response
from userprofile.models import Profile
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django.db.models import Max


class ItemsFilterView(APIView):
    """
    For filtering the items using City and Price Range 
    """
    def get(self,request,category,format= None):
        # snippets = Item.objects.filter(category = category)
        city = request.query_params.get('city')
        min_price = request.query_params.get('minPrice')
        max_price = request.query_params.get('maxPrice')

        if max_price == "-1":  # this means no max price is applied while filtering
            max_price = Item.objects.aggregate(Max("price")) ['price__max']

        snippets = Item.objects.filter(location_customised__iexact = city,category = category,price__gte = min_price, price__lte = max_price   )
        serializer = ItemSerializer(snippets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ItemView(APIView):

    # don't think this has any use case as of now
    def get(self,request,format = None):
        snippets = Item.objects.all()
        serializer = ItemSerializer(snippets, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    # for creating an item
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
            'price': request.data['price'],
            'details': request.data['details'],
            'slug': 'abc',            
        }

        try:
            serializer = ItemSerializer(data = newdict)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            for img in request.data.getlist('photos'):   
                imgdict = {
                    'item' : serializer.data['id'],
                    'image': img,
                }

                img_serializer = ImageSerializer(data =imgdict)
                img_serializer.is_valid(raise_exception=True)
                img_serializer.save()

            responses = {
                "slug" : serializer.data['slug'],
                "text" : "Addtion successful"
            }
            return Response(responses,status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response("Thats bad mate",status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ItemDetailView(APIView):

    # parser_classes = (MultiPartParser, FormParser)

    def get_object(self, slug):
        try:
            return Item.objects.get(slug=slug)
        except Item.DoesNotExist:
            raise Http404

    def get(self, request,slug, format=None):
        snippets = self.get_object(slug)
        serializer = ItemSerializer(snippets)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    # this post is not for creating but for removing/adding images
    def post(self,request, *args, **kwargs):
        item_id = request.data.get('item_id')
        item = Item.objects.get(id = item_id)

        if request.data.get('action') == 'remove_img':
            img_id = request.data.get('img_id')
            img = Image.objects.get(id = img_id)
            img.delete()

        else:
            try:
                for img in request.data.getlist('photos'):
                    Image.objects.create(item = item,image = img)
            except Exception as e:
                print(e)
                return Response({'sorry'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = ItemSerializer(item)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
      
    # slug is changing everytime 
    def put(self,request,slug,*args, **kwargs):
        item = Item.objects.get(slug = slug)
        profile = Profile.objects.get(user = request.user.id)

        newdict = {
            'profile': profile.id,
            'category': request.data['category'],
            'headline': request.data['headline'],
            'location': request.data['location'],
            'location_customised' : item.location_customised,
            'latitude': request.data['latitude'],
            'longitude': request.data['longitude'],
            'price': request.data['price'],
            'details': request.data['details'],
            'slug': item.slug,            
        }
        serializer = ItemSerializer(item,data= newdict)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,slug,*args, **kwargs):
        print(slug)
        try:
            item = Item.objects.get(slug = slug)
            item.delete()
            return Response({'deleted'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'sorry'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CartView(APIView):
    def get(self,request,format = None):
        profile = Profile.objects.get(user = request.user.id)
        snippets = CartItem.objects.filter(profile = profile)
        serializer = CartItemSerializer(snippets, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args, **kwargs):
        item_id = request.data.get('id')
        action = request.data.get("action")
        item = Item.objects.get(id = item_id)
        profile = Profile.objects.get(user = request.user.id)

        try:
            if action == "add":
                cart_item, is_created = CartItem.objects.get_or_create(item = item, profile = profile)
                
                if is_created:
                    serializer = CartItemSerializer(cart_item)
                    return Response(serializer.data,status=status.HTTP_201_CREATED)
                else:
                    return Response({"Already exists"},status=status.HTTP_201_CREATED)

            else:
                cart_item = CartItem.objects.get(item = item)
                cart_item.delete()
                return Response({"Removal Successful"},status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({"Removal Successful"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
