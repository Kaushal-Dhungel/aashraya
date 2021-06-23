from django.test import TestCase

from core.models import *
from userprofile.models import Profile
from django.contrib.auth.models import User
from datetime import date
from django.template.defaultfilters import slugify

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings


class TestModel(TestCase):
 
    img_path = settings.BASE_DIR/'media/elon.jpg'
    img = SimpleUploadedFile(name='elon.jpg', content=open(img_path, 'rb').read(), content_type='image/jpeg')

    def setUp(self):
        self.popular = Popular.objects.create(city = 'abc,def',image = self.img)   
        self.testi = Testimonial.objects.create(name = 'testname',position = 'CEO,Aashraya',pic = self.img,words = "dummy text")    

    def test_popular_str(self):
        self.assertEqual(str(self.popular),'abc,def')

    def test_city_slug(self):
        self.assertEqual(str(self.popular.city_slug),'abcdef')

    def test_testimonial_str(self):
        self.assertEqual(str(self.testi),'CEO,Aashraya')
