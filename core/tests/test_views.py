from rest_framework.test import APITestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from core.models import *
import json
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings


class TestCheckUserView(APITestCase):
    url = reverse('checkuser')

    def test_get_with_username(self):
        data = {'username':'testuser','email':''}
        res = self.client.get(self.url,data)
        self.assertEquals(res.status_code,200)

    def test_get_with_email(self):
        data = {'username':'','email':'test@localhost.com'}
        res = self.client.get(self.url,data)
        self.assertEquals(res.status_code,200)

class TestPopularView(APITestCase):
    img_path = settings.BASE_DIR/'media/elon.jpg'
    img = SimpleUploadedFile(name='elon.jpg', content=open(img_path, 'rb').read(), content_type='image/jpeg')

    def setUp(self):
        self.url = reverse("popular")
        self.popular = Popular.objects.create(city = 'abc,def',image = self.img)   

    def test_get(self):
        res = self.client.get(self.url)
        self.assertEquals(res.status_code,200)

class TestTestimonialView(APITestCase):
    img_path = settings.BASE_DIR/'media/elon.jpg'
    img = SimpleUploadedFile(name='elon.jpg', content=open(img_path, 'rb').read(), content_type='image/jpeg')

    def setUp(self):
        self.url = reverse("testimonial")
        self.testi = Testimonial.objects.create(name = 'testname',position = 'CEO,Aashraya',pic = self.img,words = "dummy text")    

    def test_get(self):
        res = self.client.get(self.url)
        self.assertEquals(res.status_code,200)

