from django.contrib import admin
from django.contrib.auth.models import User
from .models import GSiteData  # Import the GSiteData model
from django.apps import apps

# Register your models here.

#Ensuring that the site is not registered twice and give an error, we always check if the site is registered
if not admin.site.is_registered(User):
    admin.site.register(User)      #Register the user model

if not admin.site.is_registered(GSiteData):
    admin.site.register(GSiteData)  #Register the GSiteData model

if GSiteData not in admin.site._registry:
    @admin.register(GSiteData)
    class GSiteDataAdmin(admin.ModelAdmin):
        list_display = ('Town', 'Region', 'Number_of_Galamsay_Sites')
        search_fields = ('Town', 'Region')
        list_filter = ('Region',)