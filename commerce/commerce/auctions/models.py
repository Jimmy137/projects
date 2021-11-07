from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator



class User(AbstractUser):
    pass

class Category(models.Model):
   
    name = models.CharField(max_length= 15)
    
    def __str__ (self):
        return f"{self.name}"

    class Meta:
        ordering = ['name']


class Listing(models.Model):
    
    owner = models.ForeignKey(User,on_delete=models.CASCADE , related_name="listings")
    winner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="won",  blank=True, null=True )
    created = models.DateTimeField(default = datetime.datetime.now)
    initialbid = models.FloatField(default= 0.0,validators=[MinValueValidator(0.1)])
    title = models.CharField(max_length=64)
    discription = models.TextField(max_length= 300)
    photo = models.URLField(default="", blank=True, null=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="listings", blank=True, null=True)

    

    def __str__ (self):
        return f"Listing no.{self.id} {self.title.capitalize()}"

    class Meta:
        ordering = ['-created']

    
class WatchList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name="watchlist")
    listings = models.ManyToManyField(Listing, blank=True, related_name="watchlist")


class Bid(models.Model):
    bidder = models.ForeignKey(User,  on_delete=models.CASCADE , related_name="bids")
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE , related_name="price")
    value =  models.FloatField(default=0.0)

    def __str__ (self):
        return f"{self.value}" 

    



class Comment(models.Model):
    commenter = models.ForeignKey(User,  on_delete=models.CASCADE , related_name="comments")
    content = models.TextField(max_length= 300)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE , related_name="comments")
    created = models.DateTimeField(default = datetime.datetime.now)



