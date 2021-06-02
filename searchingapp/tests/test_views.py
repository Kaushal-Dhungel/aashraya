from rest_framework.test import APITestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from datetime import date,timedelta
from searchingapp.models import *
import json

from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings


class CommonTestClass(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username = "testUserrrr",password = "testinguser12345")
        self.profile = self.user.profile
        self.item = Item.objects.create(profile = self.profile, category = "room",headline = "dummy title",location = " abc,def",location_customised = "abc123",
                                    latitude = "30",longitude = "30",price = 60.0, details = "dummy text", slug = "dummy")
        self.cartItem = CartItem.objects.create(item = self.item,profile = self.profile)
        self.client.force_authenticate(user = self.user)


class TestItemFilterView(CommonTestClass):

    url = reverse('itemFilterView',args = ['room'])

    def test_get(self):
        data = {'city':'abcdef','minPrice':30 , 'maxPrice': 90}
        res = self.client.get(self.url,data)
        self.assertEquals(res.status_code,200)

    # todo test get with differernt filter in minPrice and maxPrice

class TestItemView(CommonTestClass):
    
    url = reverse('itemView')

    def test_get(self):
        res = self.client.get(self.url)
        self.assertEquals(res.status_code,200)

    def test_post(self):
        img_path = settings.BASE_DIR/'media/elon.jpg'
        img = SimpleUploadedFile(name='elon.jpg', content=open(img_path, 'rb').read(), content_type='image/jpeg')
        data = {
            'category': 'room',
            'headline': "dummy text",
            'location': 'abc,def',
            'location_customised' : 'random',
            'latitude': '30',
            'longitude': '40',
            'price': 50.0,
            'details': "dummy details",
            'slug': 'abc',  
            'photos':  img       
        }

        res = self.client.post(self.url,data,format = "multipart")
        self.assertEquals(res.data['text'],'Addtion successful')
        self.assertEquals(res.status_code,201)


class TestItemDetailiew(CommonTestClass):

    img_path = settings.BASE_DIR/'media/elon.jpg'
    image_file = SimpleUploadedFile(name='elon.jpg', content=open(img_path, 'rb').read(), content_type='image/jpeg')

    def get_img(self):
        return Image.objects.create(item = self.item,image = self.image_file)

    def get_url(self):
        return reverse('itemDetails',args= [self.item.slug])

    def test_get(self):
        res = self.client.get(self.get_url())
        self.assertEquals(res.status_code,200)

    def test_post_remove_img(self):
        data = {'item_id': self.item.id,'action':'remove_img', 'img_id': self.get_img().id}
        res = self.client.post(self.get_url(),data)  # putting format = json gives error idk why
        self.assertEquals(res.status_code,201) 

    #TODO
    # def test_post_add_img(self):
    #     print("img file")
    #     print(self.image_file)
    #     data = {'item_id':self.item.id,'action':'add_img','photos':self.image_file,'img_id':self.img.id}
    #     res = self.client.post(self.url,data,format = "multipart")
    #     print(res)
        # self.assertEquals(res.status_code,201)
    
    def test_put(self):
        data = {
            'category': 'room',
            'headline': "dummy text",
            'location': 'abc,def',
            'location_customised' : 'random',
            'latitude': '30',
            'longitude': '40',
            'price': 50.0,
            'details': "dummy details updated",
            'slug': self.item.slug  
        }

        res =  self.client.put(self.get_url(),data)
        self.assertEquals(res.data['details'],'dummy details updated') 
        self.assertEquals(res.status_code,201) 

    def test_delete(self):
        res =  self.client.delete(self.get_url())
        self.assertEquals(res.data,{'deleted'}) 
        self.assertEquals(res.status_code,200) 


class TestCartView(CommonTestClass):

    url = reverse('cartview')

    def test_get(self):
        res = self.client.get(self.url)
        self.assertEquals(res.status_code,200)

    def test_post_add(self):
        data = {'id': self.item.id,'action':'add'}
        res = self.client.post(self.url,data)
        self.assertEquals(res.status_code,201) 

    def test_post_delete(self):
        data = {'id': self.item.id,'action':'delete'}
        res = self.client.post(self.url,data)
        self.assertEquals(res.status_code,200) 
