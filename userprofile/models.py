from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(default='media/avatars/avatar.png', upload_to='avatars/') # django auto creates 'avatars' folder
    facebook_link = models.CharField(max_length=200, blank=True)
    twitter_link = models.CharField(max_length=200, blank=True)
    instagram_link = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"

    @property
    def get_username(self):
        return self.user.username

    @property
    def get_email(self):
        return self.user.email

    def save(self,*args, **kwargs):
        self.slug = slugify( "user--" + str(self.user.id))
        super().save(*args, **kwargs) 