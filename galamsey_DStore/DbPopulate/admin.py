from django.contrib import admin
from django.contrib.auth.models import User
from .models import GSiteData  # Import the GSiteData model

# Register your models here.

#Ensuring that the site is not registered twice and give an error, we always check if the site is registered
if not admin.site.is_registered(User):
    admin.site.register(User)      #Register the user model
if not admin.site.is_registered(GSiteData):
    admin.site.register(GSiteData)  #Register the GSiteData model