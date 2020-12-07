from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from django.http import Http404
from userprofile.models import Profile
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class ItemView(APIView):

    def get(self,request,category,format= None):
        # snippets = Item.objects.filter(category = category)
        city = request.query_params.get('city')
        print(city)
        print(category)
        snippets = Item.objects.filter(city__iexact = city,category = category)
        print(snippets)
        serializer = ItemSerializer(snippets, many=True)
        return Response(serializer.data)


class ViewItem(APIView):
    def get(self,request,format = None):
        snippets = Item.objects.all()
        serializer = ItemSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self,request,format = None):
        print(request.data)
        print(request.data.getlist('photos'))
        profile = Profile.objects.get(user = request.user.id)

        newdict = {
            'profile': profile.id,
            'category': request.data['category'],
            'headline': request.data['headline'],
            'location': request.data['location'],
            'city': request.data['city'],
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
            return Response(responses)

        except Exception as e:
            print(e)
            return Response("Thats bad mate")


    # def patch(self,request,*args, **kwargs):


class ItemDetailView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self, slug):
        try:
            return Item.objects.get(slug=slug)
        except Item.DoesNotExist:
            raise Http404


    def get(self, request,slug, format=None):
        snippets = self.get_object(slug)
        
        serializer = ItemSerializer(snippets)
        
        return Response(serializer.data)
    
    def post(self,request, *args, **kwargs):
        
        item_id = request.data.get('item_id')
        item = Item.objects.get(id = item_id)

        if request.data.get('action') == 'remove_img':
            # print(request.data)
            img_id = request.data.get('img_id')
            print(img_id,item_id)

            img = Image.objects.get(id = img_id)
            img.delete()

        
        else:
            print(request.data)
            try:
                for img in request.data.getlist('photos'):
                    Image.objects.create(item = item,image = img)
            except Exception as e:
                print(e)


        serializer = ItemSerializer(item)

        return Response(serializer.data)
      

# slug is changing everytime 
    def put(self,request,slug,*args, **kwargs):
        print(slug)
        print(request.data)
        item = Item.objects.get(slug = slug)
        profile = Profile.objects.get(user = request.user.id)

        newdict = {
            'profile': profile.id,
            'category': request.data['category'],
            'headline': request.data['headline'],
            'location': request.data['location'],
            'city': request.data['city'],
            'price': request.data['price'],
            'details': request.data['details'],
            'slug': item.slug,            
        }
        serializer = ItemSerializer(item,data= newdict)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response()











# class ImageView(APIView):

#     def get(self,request,format = None):
#         snippets = Image.objects.all()
#         serializer = ImageSerializer(snippets, many=True)
#         return Response(serializer.data)

#     def post(self,request, format = None):
#         img_id = request.data['id']
#         item_id = request.data['item_id']
#         print(img_id,item_id)

#         img = Image.objects.get(id = img_id)
#         img.delete()
#         # print(img)
#         return Response("delete successful")