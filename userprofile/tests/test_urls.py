from django.test import TestCase, SimpleTestCase
from django.urls import resolve, reverse

from userprofile.views import  *

class TestRoomieUrls(SimpleTestCase):
    
    def test_profile_view(self):
        url = resolve(reverse("profileview",args = ["test_category"]))
        self.assertEquals(url.func.view_class,ProfileView) 

    def test_userprofile_view(self):
        url = resolve(reverse("userprofileview"))
        self.assertEquals(url.func.view_class,UserProfileView) 