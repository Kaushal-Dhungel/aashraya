from django.test import TestCase, SimpleTestCase
from django.urls import resolve, reverse

from roommate.views import  *

class TestRoomieUrls(SimpleTestCase):

    def test_roomie_view(self):
        url = resolve(reverse("roomieView",args = ["test_category"]))
        self.assertEquals(url.func.view_class,RoomieView) 

    def test_roomie_details(self):
        url = resolve(reverse("roomieDetails",args = ["test_slug"]))
        self.assertEquals(url.func.view_class,RoomieDetailView) 

    def test_cart_view(self):
        url = resolve(reverse("roomieCartView"))
        self.assertEquals(url.func.view_class,RoomieCartView) 

    def test_view_roomie(self):
        url = resolve(reverse("viewRoomie"))
        self.assertEquals(url.func.view_class,ViewRoomie) 

    def test_roomit_post(self):
        url = resolve(reverse('roomiePost',args = ["test_slug"]))
        self.assertEquals(url.func.view_class,RoomiePostView) 
