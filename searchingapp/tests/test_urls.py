from django.test import TestCase, SimpleTestCase
from django.urls import resolve, reverse

from searchingapp.views import  *

class TestSearchingappUrls(SimpleTestCase):

    def test_item_view(self):
        url = resolve(reverse("itemFilterView",args = ["test_category"]))
        self.assertEquals(url.func.view_class,ItemsFilterView) 

    def test_item_details(self):
        url = resolve(reverse("itemDetails",args = ["test_slug"]))
        self.assertEquals(url.func.view_class,ItemDetailView) 

    def test_cart_view(self):
        url = resolve(reverse("cartview"))
        self.assertEquals(url.func.view_class,CartView) 

    def test_view_item(self):
        url = resolve(reverse("itemView"))
        self.assertEquals(url.func.view_class,ItemView) 
