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
        fname = self.user.first_name
        lname = self.user.last_name
        email = self.user.email 

        # if user model HAS email
        if email != '':  
            if self.email == '':  # but profile doesn't have, means when tried to remove the email, but we don't do that here, haha
                self.email = email
            
            else:                  # and profile have it as well, means the profile/email is probably going to be updated,
                self.email = self.email
                self.user.email = self.email   # need to update the user model's email as well
                self.user.save()

        # this doesn't happpen coz email is made mandatory for registration
        # if user model doesn't have email and the user is adding it for the very first time
        else:
            self.email = self.email
            self.user.email = self.email
            self.user.save()

        # if user model HAS the first name , but how?? there is no way the user model can have first name already without profile having it?? 
        # there is a special case, like user adds first name which becomes the first name of user model as well and then tries removing the first name from profile
        if fname != '':
            if self.first_name == '':   # but the profile doesn't have
                self.first_name = fname
            
            else:
                self.first_name = self.first_name  # and profile have it as well, means the profile/firstname is probably going to be updated,
                self.user.first_name = self.first_name
                self.user.save()
        
        # if user model doesn't have first name and the user is adding it for the very first time
        else:
            self.first_name = self.first_name
            self.user.first_name = self.first_name
            self.user.save()

        # if user model HAS last name
        if lname != '':
            if self.last_name == '':   # but the profile doesn't have
                self.last_name = lname
            
            else:                       # and profile have it as well, means the profile/lastname is probably going to be updated,
                self.last_name = self.last_name
                self.user.last_name = self.last_name
                self.user.save()
        
        # if user model doesn't have last name and the user is adding it for the very first time
        else:
            self.last_name = self.last_name
            self.user.last_name = self.last_name
            self.user.save()

        self.slug = slugify( "user--" + str(self.user.id))
        super().save(*args, **kwargs)