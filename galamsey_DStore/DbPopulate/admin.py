from django.contrib import admin
from django.contrib.auth.models import User
# Register your models here.
if not admin.site.is_registered(User):
    admin.site.register(User)