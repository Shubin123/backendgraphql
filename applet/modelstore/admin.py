from django.contrib import admin

# Register your models here.
from applet.modelstore.models import User
# from applet.modelstore.models import Category
# admin.site.register(Category)
admin.site.register(User)
