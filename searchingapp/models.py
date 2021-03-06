from django.db import models
from django.db.models.deletion import CASCADE
from userprofile.models import Profile
from django.template.defaultfilters import slugify

# Create your models here.


class Item(models.Model):

    CHOICES = (
    ('room', 'room'),
    ('flat', 'flat'),
    ('house', 'house'),
    ('hostel', 'hostel'),
    ('land', 'land'),
    )

    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="item_model")
    category = models.CharField(max_length=30, choices = CHOICES)
    headline = models.CharField(max_length=400,null= False, blank = False)
    location = models.CharField(max_length=200,null= False, blank = False)
    location_customised = models.CharField(max_length=200,null= False, blank = False)
    latitude = models.CharField(max_length=200,null= False, blank = False)
    longitude = models.CharField(max_length=200,null= False, blank = False)
    price = models.DecimalField(max_digits= 10, decimal_places=2)
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
        original_slug = slugify(f"{self.profile.user.username}-{self.category}")
        queryset = Item.objects.all().filter(slug__iexact = original_slug).count()  # count the no of items with same slug

        count = 1
        slug = original_slug 

        while(queryset):  # if there is any queryset, i.e while(1), if not queryset then it becomes while(0) so this part will be skipped
            slug = original_slug + "-" + str(count)
            count += 1 
            queryset = Item.objects.all().filter(slug__iexact = slug).count()  # count the no of items with same slug
 
        self.slug = slug

        location = self.location.replace(',','') # remove commas
        location = location.replace(' ','')   # remove whitespaces
        
        self.location_customised = location

        super().save(*args, **kwargs)

    
class Image(models.Model):

    def generate_filename(self, filename) -> str:
        url = "imgs/%s/%s" % (self.item.profile.user.username, filename)
        return url

    item = models.ForeignKey(Item,on_delete=models.CASCADE,related_name="images")
    image = models.ImageField(upload_to=generate_filename)

    def __str__(self) -> str:
        return str(f"{self.item}---{self.id}")


class CartItem(models.Model):
    """
    item was previously OneToOne now ForeignKey because once the item is removed from cart it couldn't be added again and
    would give Unique Constraint failed error.
    """
    item = models.ForeignKey(Item,on_delete = models.CASCADE,related_name="cart_items")
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return str(f"{self.item}---{self.profile.user.username}")

    