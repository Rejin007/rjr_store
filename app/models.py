from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
# Create your models here.
GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

class Countries(models.Model):
    country_name = models.CharField(max_length=100, unique=True)

class States(models.Model):
    state_name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
class Districts(models.Model):
    district_name = models.CharField(max_length=100, unique=True)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
class Products(models.Model):
    product_name = models.CharField(max_length=100, unique=True) 
    product_price = models.IntegerField() 
    product_image = models.ImageField(upload_to='image')
    product_description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product_mrp = models.CharField(max_length=20)
    product_offer = models.CharField(max_length=10)
    is_active = models.BooleanField(default=False)  # Field to mark product as active or inactive

    def save(self, *args, **kwargs):                 # Override save method to set slug
        if not self.slug:                           # Only set slug if it is not already set
            self.slug = slugify(self.product_name)  # Generate slug from product name 

        super().save(*args, **kwargs)               # Call the original save method
    def __str__(self):                              # String representation of the model
        return self.product_name                    # This will return the product name when the object is printed
    
class Signup(models.Model):
    username = models.CharField(name="username",max_length=50)
    email = models.EmailField(name="email",max_length=50)
    first_name = models.CharField(name="first_name",max_length=20)
    last_name = models.CharField(name="last_name",max_length=20)
    phonenumber = models.CharField(name="phonenumber",max_length=20)
    gender = models.CharField(choices=GENDER_CHOICES,max_length=15)
    dob = models.DateField()
    country = models.ForeignKey(Countries,on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(States,on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(Districts,on_delete=models.SET_NULL, null=True)
    terms = models.BooleanField(name="terms")
    
class OTP(models.Model):
    email = models.EmailField(null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE) # foreign key to acess User model
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    def is_expired(self):
        return timezone.now()>self.created_at+datetime.timedelta(minutes=5)