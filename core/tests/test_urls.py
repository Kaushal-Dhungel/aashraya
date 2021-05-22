from django.test import TestCase, SimpleTestCase
from django.urls import resolve, reverse

from core.views import  *

class TestRoomieUrls(SimpleTestCase):
    
    def test_popular(self):
        url = resolve(reverse("popular"))
        self.assertEquals(url.func.view_class,PopularView) 

    def test_testimonial(self):
        url = resolve(reverse("testimonial"))
        self.assertEquals(url.func.view_class,TestimonialView) 