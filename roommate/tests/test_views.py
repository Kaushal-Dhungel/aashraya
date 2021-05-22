from rest_framework.test import APITestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from datetime import date,timedelta
from roommate.models import *
import json

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings


# this class holds the common setUp for other classes
class CommonTestClass(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username = "testUserrrr",password = "testinguser12345")
        self.profile = self.user.profile
        self.roomie = Roomie.objects.create(profile = self.profile, category = "room",headline = "dummy title",location = " abc,def",location_customised = "abc123",
                                    latitude = "30",longitude = "30",price_range = '0-5000', sex_pref = 'female',age_pref = '21-25', details = "dummy text", slug = "dummy")
        self.cartItem = RoomieCartItem.objects.create(item = self.roomie,profile = self.profile)
        self.client.force_authenticate(user = self.user)


class TestRoomieView(CommonTestClass):

    url = reverse('roomieView',args = ['room'])

    def test_get_with_priceRange(self):
        data = {'city':'abcdef','priceRange':'0-5000'}
        res = self.client.get(self.url,data)
        self.assertEquals(len(res.data),1)
        self.assertEquals(res.status_code,200)

    def test_get_without_priceRange(self):
        data = {'city':'abcdef','priceRange':'0'}
        res = self.client.get(self.url,data)
        self.assertEquals(res.status_code,200)


class TestViewRoomie(CommonTestClass):

    url = reverse('viewRoomie')

    def test_get(self):
        res = self.client.get(self.url)
        self.assertEquals(res.status_code,200)

    def test_post(self):
        img_path = settings.BASE_DIR/'media/People/elon.jpg'
        img = SimpleUploadedFile(name='elon.jpg', content=open(img_path, 'rb').read(), content_type='image/jpeg')
        data = {
            'category': 'room',
            'headline': "dummy text",
            'location': 'abc,def',
            'location_customised' : 'random',
            'latitude': '30',
            'longitude': '40',
            'price_range': '0-5000',
            'sex_pref' : 'male',
            'age_pref' : '21-25',
            'details': "dummy details",
            'slug': 'abc',  
            'photos':  img       
        }

        res = self.client.post(self.url,data,format = "multipart")
        self.assertEquals(res.data['text'],'Addtion successful')
        self.assertEquals(res.status_code,201)


class TestRoomieDetailView(CommonTestClass):
    img_path = settings.BASE_DIR/'media/People/elon.jpg'
    image_file = SimpleUploadedFile(name='elon.jpg', content=open(img_path, 'rb').read(), content_type='image/jpeg')

    def get_url(self):
        return reverse('roomieDetails',args= [self.roomie.slug])

    def get_img(self):
        return RoomieImage.objects.create(roomie = self.roomie,image = self.image_file)

    def test_get(self):
        res = self.client.get(self.get_url())
        self.assertEquals(res.status_code,200)

    def test_post_remove_img(self):
        data = {'item_id': self.roomie.id,'action':'remove_img', 'img_id': self.get_img().id}
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
            'price_range': '0-5000',
            'sex_pref': 'female',
            'age_pref': '21-25',
            'details': "dummy details updated",
            'slug': self.roomie.slug  
        }

        res =  self.client.put(self.get_url(),data)
        self.assertEquals(res.data['details'],'dummy details updated') 
        self.assertEquals(res.status_code,201) 

    def test_delete(self):
        res =  self.client.delete(self.get_url())
        self.assertEquals(res.data,{'deleted'}) 
        self.assertEquals(res.status_code,200) 


class TestRoomiePostView(CommonTestClass):

    def test_get(self):
        url = reverse('roomiePost',args = [self.profile.slug])
        res = self.client.get(url)
        self.assertEquals(res.status_code,200) 


class TestRoomieCartView(CommonTestClass):

    url = reverse('roomieCartView')

    def test_get(self):
        res = self.client.get(self.url)
        self.assertEquals(res.status_code,200)

    def test_post_add(self):
        data = {'id': self.roomie.id,'action':'add'}
        res = self.client.post(self.url,data)
        self.assertEquals(res.status_code,201) 

    def test_post_delete(self):
        data = {'id': self.roomie.id,'action':'delete'}
        res = self.client.post(self.url,data)
        self.assertEquals(res.status_code,200) 
