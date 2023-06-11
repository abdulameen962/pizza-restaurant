from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    pass

class Pizza(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    picture = CloudinaryField("image",blank=True,default=None,null=True)
    available = models.BooleanField(default=True)
    objects = models.Manager()

    class Meta:
        verbose_name = "Pizza"
        verbose_name_plural = "Pizza"
        ordering = ("-name",)

    def __str__(self):
        return f"{self.name} pizza"
    

class Category(models.Model):
    title = models.CharField(max_length=50)
    code = models.CharField(max_length=5)
    objects = models.Manager()

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
class Topping(models.Model):
    name = models.CharField(max_length=150)
    picture = CloudinaryField("image",blank=True,default=None,null=True)
    price = models.FloatField(default=0)
    available = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=False,default=timezone.now)
    objects = models.Manager()

    class Meta:
        ordering = ("-date_created",)

    def __str__(self):
        return f"{self.name}"
    

class Creation(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE,related_name="creations")
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE,related_name="pizza_creation")
    category = models.ForeignKey(Pizza, on_delete=models.CASCADE,related_name="pizza_category",null=True,blank=True)
    toppings = models.ManyToManyField(Topping,related_name="toppings_creation",blank=True)
    picture = CloudinaryField("image",blank=True,default=None,null=True)
    price = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=False,default=timezone.now)
    available = models.BooleanField(default=True)
    objects = models.Manager()

    class Meta:
        verbose_name = "Creation"
        verbose_name_plural = "Creations"
        ordering = ("-created",)

    def __str__(self):
        return f"{self.name}"
    

class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="user_profile")
    profile_pic = CloudinaryField("image",blank=True,default=None,null=True)
    objects = models.Manager()

    class Meta:
        verbose_name = "User profile"
        verbose_name_plural = "Users profiles"

    def __str__(self):
        return f"{self.user.username}"


class Order(models.Model):
    STATUS_CHOICES = (
        ("PENDING","PENDING"),
        ("COMPLETED","COMPLETED"),
    )
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE,related_name="orders")
    order = models.ForeignKey(Creation, on_delete=models.CASCADE,related_name="creation_orders")
    pieces = models.IntegerField()
    price = models.FloatField()
    order_date = models.DateTimeField(auto_now_add=False,default=timezone.now)
    order_completed_date = models.DateTimeField(auto_now_add=False,blank=True)
    status = models.CharField(choices=STATUS_CHOICES,default="PENDING")

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    