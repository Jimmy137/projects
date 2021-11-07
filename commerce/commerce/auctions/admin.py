from django.contrib import admin
from .models import User, Listing, Bid, Comment, Category, WatchList

# Register your models here.
class ladmin (admin.ModelAdmin):
    list_display = ("id","owner","winner", "title", "category", "price")

class cadmin (admin.ModelAdmin):
    list_display = ("id","commenter","listing", "created")

class badmin (admin.ModelAdmin):
    list_display = ("id", "value", "listing", "bidder")

admin.site.register(User)
admin.site.register(Listing, ladmin)
admin.site.register(Bid, badmin)
admin.site.register(Comment, cadmin)
admin.site.register(Category)
admin.site.register(WatchList)