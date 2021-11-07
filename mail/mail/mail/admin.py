from django.contrib import admin
from .models import User, Email

# Register your models here.
class ladmin (admin.ModelAdmin):
    list_display = ("id","sender", "subject")

admin.site.register(User)
admin.site.register(Email,ladmin)