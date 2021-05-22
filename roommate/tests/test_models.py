from django.test import TestCase

from roommate.models import *
from userprofile.models import Profile
from django.contrib.auth.models import User
from datetime import date
from django.template.defaultfilters import slugify


class TestModel(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = "dummyUser",email = "hello@localhost.com",password = "testinguser12345")
        self.profile = self.user.profile
        self.roomie = Roomie.objects.create(profile = self.profile, category = "room",headline = "dummy title",location = " abc,def",location_customised = "abc123",
                                    latitude = "30",longitude = "30",price_range = '0-5000', sex_pref = 'female', details = "dummy text", slug = "dummy")
        self.cartItem = RoomieCartItem.objects.create(item = self.roomie,profile = self.profile)

    def test_model_roomie_str(self):
        roomie_str = f"{self.user.username}--{self.roomie.category}--{self.roomie.created.strftime('%d-%m-%Y')}"
        self.assertEqual(str(self.roomie),roomie_str)

    def test_roomie_profile_slug_method(self):
        self.assertEqual(self.roomie.profile_slug,self.profile.slug)

    def test_roomie_slug(self):
        roomie_slug = slugify(f"{self.profile.user.username}-{self.roomie.category}--{self.roomie.sex_pref}")
        self.assertEqual(self.roomie.slug,roomie_slug)

    def test_roomie_location_customised(self):  # this was done in models to remove comma from location fetched from mapbox
        self.assertEqual(self.roomie.location_customised,'abcdef')

    
    #-------------------------------------- new model ------------------------------------------------
    def test_model_roomie_cart_item_str(self):
        cart_str = f"{self.roomie}---{self.profile.user.username}"
        self.assertEqual(str(self.cartItem),cart_str)
