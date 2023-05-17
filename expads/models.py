from django.db import models
#from django.contrib.auth.models import User
from accounts.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from sorl.thumbnail import get_thumbnail

from phonenumber_field.modelfields import PhoneNumberField

class Countrycode(models.Model):
    name = models.CharField(max_length=128)
    
    def __str__(self):
         return self.name

class Purpose(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
         return self.name


class CityCode(models.Model):
    name = models.CharField(max_length=128)
    countrycode = models.ForeignKey(Countrycode, on_delete=models.CASCADE, related_name='countrycode')

    def __str__(self):
         return self.name


class LocationCode(models.Model):
    name = models.CharField(max_length=128)
    locationcode = models.ForeignKey(CityCode, on_delete=models.CASCADE, related_name='locationcode')

    def __str__(self):
         return self.name


class SubLocationCode(models.Model):
    name = models.CharField(max_length=128)
    sublocationCode = models.ForeignKey(LocationCode, on_delete=models.CASCADE, related_name='sublocationCode')

    def __str__(self):
         return self.name


class Category(models.Model):
    name = models.CharField(max_length = 150 , null = False)
    slug = models.CharField(max_length = 150 , null = False , unique = True)
    thumbnail = models.ImageField(upload_to='users/thumnail', blank=True, null=True)   
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('-created','-updated')
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def clean(self):
        self.category_name = self.name.capitalize()

    def get_url(self):
        return reverse('expads_by_category', args=[self.slug])

    def __str__(self):
        return self.name

class Expatad(models.Model):
    user = models.ForeignKey(User ,  on_delete=models.CASCADE)
    category = models.ForeignKey(Category ,  on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150)
    countrycode = models.ForeignKey(Countrycode ,default='Saudi Arabia',  on_delete=models.CASCADE)
    purpose = models.ForeignKey(Purpose , on_delete=models.CASCADE)
    citycode = models.ForeignKey(CityCode ,  default='Jeddah',on_delete=models.CASCADE)
    locationcode =models.CharField(max_length=200)
    sublocationcode = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    area = models.CharField(max_length=100,default=100)
    areameasurement = models.CharField(max_length=40,default='Square Feet')
    contactno = PhoneNumberField()
    zipcode = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    Description = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('-created','-updated')
        verbose_name = 'expatad'
        verbose_name_plural = 'expatads'

    def __str__(self):
        return self.fullname

    def delete(self):
        self.cover_photo.delete()
        super().delete()


class ExpatImage(models.Model):
    expatads = models.ForeignKey(Expatad, on_delete=models.CASCADE,related_name='expatads')
    images = models.FileField(upload_to='users/images', blank=True, null=True)

    

    @property
    def thumbnail(self):
        if self.images:
            return get_thumbnail(self.images, '50x50', quality=90)
        return None
    
    def __str__(self):
        return self.expatads.contactno


 #   def delete(self):
        self.cover_photo.delete()
        super().delete()
 #       
 #   year = models.PositiveSmallIntegerField(
 #       validators=[
 #           MinValueValidator(1895),
 #           MaxValueValidator(2050),
 #       ])

 #   rating = models.PositiveSmallIntegerField(choices=(
 #       (1, "★☆☆☆☆"),
 #       (2, "★★☆☆☆"),
 #       (3, "★★★☆☆"),
 #       (4, "★★★★☆"),
 #       (5, "★★★★★"),        



class Contactme(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150)
    contactno = PhoneNumberField()
    email = models.CharField(max_length=150)
    Description = models.CharField(max_length=500)
    is_fallowed = models.CharField(max_length=100,default="Yet Not Followed This Message")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname

class Interested(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150)
    contactno = PhoneNumberField()
    email = models.CharField(max_length=150)
    Description = models.CharField(max_length=500)
    is_fallowed = models.CharField(max_length=100,default="Yet Not Followed This Message")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname