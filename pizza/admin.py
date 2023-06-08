from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Creation)
admin.site.register(Userprofile)
admin.site.register(Order)
admin.site.register(Category)