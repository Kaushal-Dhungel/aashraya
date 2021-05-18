from django.test import TestCase

from searchingapp.models import *
from userprofile.models import Profile
from django.contrib.auth.models import User
from datetime import date
from django.template.defaultfilters import slugify


class TestModel(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = "dummyUser",email = "hello@localhost.com",password = "testinguser12345")
        self.profile = self.user.profile
        self.item = Item.objects.create(profile = self.profile, category = "room",headline = "dummy title",location = " abc,def",location_customised = "abc123",
                                    latitude = "30",longitude = "30",price = 60.0, details = "dummy text", slug = "dummy")
        self.cartItem = CartItem.objects.create(item = self.item,profile = self.profile)

    def test_model_item_str(self):
        item_str = f"{self.user.username}--{self.item.category}--{self.item.created.strftime('%d-%m-%Y')}"
        self.assertEqual(str(self.item),item_str)

    def test_profile_slug_method(self):
        self.assertEqual(self.item.profile_slug,self.profile.slug)

    def test_item_slug(self):
        item_slug = slugify(f"{self.profile.user.username}-{self.item.category}")
        self.assertEqual(self.item.slug,item_slug)

    def test_location_customised(self):  # this was done in models to remove comma from location fetched from mapbox
        self.assertEqual(self.item.location_customised,'abcdef')

    
    #-------------------------------------- new model ------------------------------------------------
    def test_model_cart_item_str(self):
        cart_str = f"{self.item}---{self.profile.user.username}"
        self.assertEqual(str(self.cartItem),cart_str)
