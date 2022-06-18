from django.contrib import admin

# Register your models here.
from applet.modelstore.models import Category, Item

admin.site.register(Category)
admin.site.register(Item)