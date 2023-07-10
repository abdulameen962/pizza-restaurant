from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.utils import timezone
import uuid
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    pass

    def serialize(self):
        return{
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

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
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "picture": self.picture.url if self.picture is not None else '#'
        }

class Category(models.Model):
    title = models.CharField(max_length=50)
    code = models.CharField(max_length=5)
    objects = models.Manager()

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    def serialize(self):
        return{
            "id": self.id,
            "title": self.title,
            "code": self.code,
        }
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
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "picture": self.picture.url if self.picture is not None else '#',
            "price": self.price
        }
class Creation(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE,related_name="creations")
    name = models.CharField(max_length=150)
    slug = models.SlugField(blank=True,null=True,max_length=200,default=None)
    description = models.TextField(max_length=500)
    pizza = models.ForeignKey(Pizza, on_delete=models.PROTECT,related_name="pizza_creation")
    category = models.ForeignKey(Category, on_delete=models.PROTECT,related_name="pizza_category",null=True,blank=True)
    toppings = models.ManyToManyField(Topping,related_name="toppings_creation",blank=True,default=None)
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

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "picture": self.picture.url if self.picture is not None else '#',
            "price": self.price,
            "creator": self.creator.serialize(),
            "pizza": self.pizza.serialize(),
            "toppings": [topping.serialize() for topping in self.toppings.all()],
            "category": self.category.serialize()

        }
    

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
    # name = models.CharField(_("Name of event"),blank=True,max_length=255)
    status = models.CharField(choices=STATUS_CHOICES,default="PENDING")

    def __str__(self):
        return f"{self.id} {self.user.username}"
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    
class Cart(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    items = models.ManyToManyField(Order,related_name="order_cart",blank=True,default=None)
    order_completed_date = models.DateTimeField(auto_now_add=False,blank=True,default=timezone.now)
    user = models.OneToOneField(User, on_delete=models.PROTECT,related_name="user_cart")
    price = models.FloatField(_("Total price"),default=0.0)
    created_at = models.DateTimeField(auto_now_add=False,default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username}'s cart has {len(self.items.all)} items all worth {self.price}"
    
    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ("created_at",)
    
#uuid primary id field
#     id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
