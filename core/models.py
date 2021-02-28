from django.db import models

# Create your models here.

class Popular(models.Model):
    city = models.CharField(max_length=400,null= False, blank = False)
    city_slug = models.CharField(max_length=700, null= True, blank= True)
    image = models.ImageField( upload_to='Popular/')

    def __str__(self) -> str:
        return self.city

    def save(self,*args, **kwargs):
        city = self.city.split(",")  # first separate using comma
        city = "".join(i.strip() for i in city)
        city = city.split(" ")      # separate using white space
        city = "".join(i.strip() for i in city)  

        self.city_slug = city
        super().save(*args, **kwargs)


class Testimonial(models.Model):
    name = models.CharField(max_length=400,null= False, blank = False)
    position = models.CharField(max_length=400,null= False, blank = False)
    pic = models.ImageField(upload_to='People/')
    words = models.TextField(null= False, blank = False)

    def __str__(self) -> str:
        return f'{self.name} -- {self.position}'


