from rest_framework.test import APITestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from datetime import date,timedelta
from searchingapp.models import *
import json

from io import StringIO, BytesIO
from django.core.files import File
# from django.utils.six import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings


# def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
#    """
#    Generate a test image, returning the filename that it was saved as.

#    If ``storage`` is ``None``, the BytesIO containing the image data
#    will be passed instead.
#    """
#    data = BytesIO()
#    img = Image.new(image_mode, size).save(data, image_format)
#    return img
#    data.seek(0)
#    if not storage:
#        return data
#    image_file = ContentFile(data.read())
#    return storage.save(filename, image_file)

class TestItemView(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username = "testUserrrr",password = "testinguser12345")
        self.profile = self.user.profile
        self.item = Item.objects.create(profile = self.profile, category = "room",headline = "dummy title",location = " abc,def",location_customised = "abc123",
                                    latitude = "30",longitude = "30",price = 60.0, details = "dummy text", slug = "dummy")
        self.cartItem = CartItem.objects.create(item = self.item,profile = self.profile)
        self.url = reverse('itemView',args = ['room'])

    def test_get(self):
        data = {'city':'abcdef','minPrice':30 , 'maxPrice': 90}
        res = self.client.get(self.url,data)
        self.assertEquals(res.status_code,200)

    # todo test get with differernt filter in minPrice and maxPrice

class TestViewItem(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username = "testUserrrr",password = "testinguser12345")
        self.profile = self.user.profile
        self.item = Item.objects.create(profile = self.profile, category = "room",headline = "dummy title",location = " abc,def",location_customised = "abc123",
                                    latitude = "30",longitude = "30",price = 60.0, details = "dummy text", slug = "dummy")
        self.cartItem = CartItem.objects.create(item = self.item,profile = self.profile)
        self.url = reverse('viewItem')
        self.client.force_authenticate(user = self.user)

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
            'price': 50.0,
            'details': "dummy details",
            'slug': 'abc',  
            'photos':  img       
        }

        res = self.client.post(self.url,data,format = "multipart")
        self.assertEquals(res.data['text'],'Addtion successful')
        self.assertEquals(res.status_code,201)


class TestItemDetailiew(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username = "testUserrrr",password = "testinguser12345")
        self.profile = self.user.profile
        self.item = Item.objects.create(profile = self.profile, category = "room",headline = "dummy title",location = " abc,def",location_customised = "abc123",
                                    latitude = "30",longitude = "30",price = 60.0, details = "dummy text", slug = "dummy")

        img_path = settings.BASE_DIR/'media/People/elon.jpg'
        self.image_file = SimpleUploadedFile(name='elon.jpg', content=open(img_path, 'rb').read(), content_type='image/jpeg')
        self.img = Image.objects.create(item = self.item,image = self.image_file)
        self.cartItem = CartItem.objects.create(item = self.item,profile = self.profile)
        self.url = reverse('itemDetails',args= [self.item.slug])
        self.client.force_authenticate(user = self.user)

    def test_get(self):
        res = self.client.get(self.url)
        self.assertEquals(res.status_code,200)

    def test_post_remove_img(self):
        data = {'item_id': self.item.id,'action':'remove_img', 'img_id': self.img.id}
        res = self.client.post(self.url,data)  # putting format = json gives error idk why
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

        res =  self.client.put(self.url,data)
        self.assertEquals(res.data['details'],'dummy details updated') 
        self.assertEquals(res.status_code,201) 

    def test_delete(self):
        res =  self.client.delete(self.url)
        self.assertEquals(res.data,{'deleted'}) 
        self.assertEquals(res.status_code,200) 


class TestCartView(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username = "testUserrrr",password = "testinguser12345")
        self.profile = self.user.profile
        self.item = Item.objects.create(profile = self.profile, category = "room",headline = "dummy title",location = " abc,def",location_customised = "abc123",
                                    latitude = "30",longitude = "30",price = 60.0, details = "dummy text", slug = "dummy")
        self.cartItem = CartItem.objects.create(item = self.item,profile = self.profile)
        self.url = reverse('cartview')
        self.client.force_authenticate(user = self.user)

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
