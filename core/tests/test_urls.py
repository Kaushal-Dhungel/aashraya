from django.test import TestCase, SimpleTestCase
from django.urls import resolve, reverse

from core.views import  *

class TestCoreUrls(SimpleTestCase):
    
    def test_registeruser(self):
        url = resolve(reverse("register"))
        self.assertEquals(url.func.view_class,RegisterUser) 

    def test_checkuser(self):
        url = resolve(reverse("checkuser"))
        self.assertEquals(url.func.view_class,CheckUser) 

    def test_popular(self):
        url = resolve(reverse("popular"))
        self.assertEquals(url.func.view_class,PopularView) 

    def test_testimonial(self):
        url = resolve(reverse("testimonial"))
        self.assertEquals(url.func.view_class,TestimonialView) 