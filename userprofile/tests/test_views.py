from rest_framework.test import APITestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from datetime import date,timedelta
from roommate.models import *
import json

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings


class TestProfileView(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username = "testUserrrr",password = "testinguser12345")
        self.profile = self.user.profile
        self.url = reverse("profileview",args = [self.profile.slug])

    def test_get(self):
        res = self.client.get(self.url)
        self.assertEquals(res.status_code,200)

class TestUserProfileView(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username = "testUserrrr",password = "testinguser12345")
        self.profile = self.user.profile
        self.client.force_authenticate(user = self.user)
        self.url = reverse("userprofileview")

    def test_get(self):
        res = self.client.get(self.url)
        self.assertEquals(res.status_code,200)

    def test_post_remove_pic(self):
        data = {'action':'remove_pic'}
        res = self.client.post(self.url)
        self.assertEquals(res.status_code,200)

    def test_post_add_pic(self):
        img_path = settings.BASE_DIR/'media/People/elon.jpg'
        img = SimpleUploadedFile(name='elon.jpg', content=open(img_path, 'rb').read(), content_type='image/jpeg')
        data = {'action':'add_pic','avatar':img}


        res = self.client.post(self.url)
        self.assertEquals(res.status_code,200)

    def test_patch(self):
        data = {'first_name':'','last_name':'','email':'','phone':"9816967736",'facebook_link':'','twitter_link':'','instagram_link':''}
        res = self.client.patch(self.url,data,format = 'json')
        self.assertEquals(res.status_code,200)

    def test_delete(self):
        res = self.client.delete(self.url)
        self.assertEquals(res.status_code,200)