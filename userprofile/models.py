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
    avatar = models.ImageField(default='avatar_qlg7p2.png', upload_to='avatars/') # django auto creates 'avatars' folder
    facebook_link = models.CharField(max_length=200, blank=True)
    twitter_link = models.CharField(max_length=200, blank=True)
    instagram_link = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"

    @property
    def get_username(self):
        return self.user.username

    @property
    def get_email(self):
        return self.user.email

    # __initial_first_name = None
    # __initial_last_name = None

    # __initial_first_name = user.first_name
    # __initial_last_name = user.last_name

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.__initial_first_name = self.first_name
    #     self.__initial_last_name = self.last_name



    # def save(self, *args, **kwargs):
    #     ex = False
    #     to_slug = self.slug
    #     if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug=="":
    #         if self.first_name and self.last_name:
    #             to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
    #             ex = Profile.objects.filter(slug=to_slug).exists()
    #             while ex:
    #                 to_slug = slugify(to_slug + " " + str(get_random_code()))
    #                 ex = Profile.objects.filter(slug=to_slug).exists()
    #         else:
    #             to_slug = str(self.user)
        

    #     self.slug = to_slug
        
    #     super().save(*args, **kwargs)


    def save(self,*args, **kwargs):

        fname = self.user.first_name
        lname = self.user.last_name
        email = self.user.email 

        if email != '':
            if self.email == '':
                self.email = email
            
            else:
                self.email = self.email
                self.user.email = self.email
                self.user.save()
                
        else:
            self.email = self.email
            self.user.email = self.email
            self.user.save()


        if fname != '':
            if self.first_name == '':
                self.first_name = fname
            
            else:
                self.first_name = self.first_name
                self.user.first_name = self.first_name
                self.user.save()
        else:
            self.first_name = self.first_name
            self.user.first_name = self.first_name
            self.user.save()

        if lname != '':
            if self.last_name == '':
                self.last_name = lname
            
            else:
                self.last_name = self.last_name
                self.user.last_name = self.last_name
                self.user.save()
        else:
            self.last_name = self.last_name
            self.user.last_name = self.last_name
            self.user.save()


        self.slug = slugify( "user--" + str(self.user.id))
        super().save(*args, **kwargs)