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
        
    def test_profile_str(self):
        profile_str = f"{self.user.username}-{self.profile.created.strftime('%d-%m-%Y')}"
        self.assertEqual(str(self.profile),profile_str)

    def test_get_username(self):
        self.assertEqual(self.profile.get_username,self.user.username)

    def test_get_email(self):
        self.assertEqual(self.profile.get_email,self.user.email)

    def test_profile_slug(self):
        self.assertEqual(self.profile.slug,slugify("user--" + str(self.user.id)))
