from django.db import models
from userprofile.models import Profile
from django.template.defaultfilters import slugify

# Create your models here.

class Roomie(models.Model):
    CHOICES = (
    ('room', 'room'),
    ('flat', 'flat'),
    ('hostel', 'hostel'),
    )

    CHOICES_SEX = (
    ('male', 'male'),
    ('female', 'female'),
    ('male/female', 'male/female'),
    )

    CHOICES_AGE = (
    ('15-20', '15-20'),
    ('21-25', '21-25'),
    ('26-30', '26-30'),
    ('31-35', '31-35'),
    ('36-40', '36-40'),
    ('40+', '40+'),
    )

    CHOICES_PRICE = (
    ('0-5000', '0-5000'),
    ('5001-10,000', '5001-10,000'),
    ('10001-15000', '10001-15000'),
    ('15001-20000', '15001-20000'),
    ('20000+', '20000+'),

    )


    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    category = models.CharField(max_length=30, choices = CHOICES)
    headline = models.CharField(max_length=400,null= False, blank = False)
    location = models.CharField(max_length=200,null= False, blank = False)
    location_customised = models.CharField(max_length=200,null= False, blank = False)
    latitude = models.CharField(max_length=200,null= False, blank = False)
    longitude = models.CharField(max_length=200,null= False, blank = False)
    price_range = models.CharField(max_length=200,choices = CHOICES_PRICE)
    sex_pref = models.CharField(max_length=200,choices = CHOICES_SEX)
    age_pref = models.CharField(max_length=200,choices = CHOICES_AGE)
    details = models.TextField(null= False, blank = False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()
 
    def __str__(self) -> str:
        return f"{self.profile.user.username}--{self.category}--{self.created.strftime('%d-%m-%Y')}"

    @property
    def profile_slug(self):
        return self.profile.slug

    def save(self,*args, **kwargs):
        original_slug = slugify(f"{self.profile.user.username}-{self.category}--{self.sex_pref}")
        queryset = Roomie.objects.all().filter(slug__iexact = original_slug).count()  # count the no of Roomies with same slug

        count = 1
        slug = original_slug 

        while(queryset):  # if there is any queryset, i.e while(1), if not queryset then it becomes while(0) so this part will be skipped
            slug = original_slug + "-" + str(count)
            count += 1 
            queryset = Roomie.objects.all().filter(slug__iexact = slug).count()  # count the no of Roomies with same slug
 
        self.slug = slug

        location = self.location.split(",")  # first separate using comma
        location = "".join(i.strip() for i in location)
        location = location.split(" ")      # separate using white space
        location = "".join(i.strip() for i in location)  
        
        self.location_customised = location

        super().save(*args, **kwargs)

class RoomieImage(models.Model):

    def generate_filename(self, filename) -> str:
        url = "roomie/%s/%s" % (self.roomie.profile.user.username, filename)
        return url

    roomie = models.ForeignKey(Roomie,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to=generate_filename)

    def __str__(self) -> str:
        return str(f"{self.roomie}---{self.id}")

class RoomieCartItem(models.Model):
    item = models.OneToOneField(Roomie,on_delete = models.CASCADE,related_name="cart_roomie")
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return str(f"{self.item}---{self.profile.user.username}")