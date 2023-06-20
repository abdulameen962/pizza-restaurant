from django.contrib import admin

from .models import *
# Register your models here.
class CreationAdmin(admin.ModelAdmin):
    list_display = ("name","description","created","available",)
    filter_horizontal = ("toppings",)



admin.site.register(User)
admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Creation,CreationAdmin)
admin.site.register(Userprofile)
admin.site.register(Order)
admin.site.register(Category)