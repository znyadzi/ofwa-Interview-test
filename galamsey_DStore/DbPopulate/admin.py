from django.contrib import admin
from django.contrib.auth.models import User
from .models import UploadedFile, SiteRecords  # Importing the models

# Register the User model if not already registered
if not admin.site.is_registered(User):
    admin.site.register(User)

# Register UploadedFile model
@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'FileName', 'DateUploaded')
    search_fields = ('FileName',)
    list_filter = ('DateUploaded',)

# Register SiteRecords model
@admin.register(SiteRecords)
class SiteRecordsAdmin(admin.ModelAdmin):
    list_display = ('id', 'Town', 'Region', 'Number_of_Galamsay_Sites', 'FileID')
    search_fields = ('Town', 'Region')
    list_filter = ('Region',)
