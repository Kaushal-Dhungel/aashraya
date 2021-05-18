from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from django.http import Http404

# Create your views here.
class PopularView(APIView):
    def get(self,request,*args,**kwargs):
        snippets = Popular.objects.all()
        serializer = PopularSerializer(snippets, many=True)
        return Response(serializer.data)

class TestimonialView(APIView):
    def get(self,request,*args,**kwargs):
        snippets = Testimonial.objects.all()
        serializer = TestimonialSerializer(snippets, many=True)
        return Response(serializer.data)