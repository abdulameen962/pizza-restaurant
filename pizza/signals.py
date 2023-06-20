from django.db.models.signals import pre_save,post_save,pre_delete,post_delete
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from .models import *
from cloudinary import api
import cloudinary.uploader
from django.core.files import File
from .image_mixer import mix_image,delete_image
from .helper_functions import image_file_converter
from cloudinary.exceptions import Error as ResourceNotFound
# from django.core.files.storage import default_storage

@receiver(post_save,sender=User)
def user_post_save_handler(instance,sender,**kwargs):
    #check if there is a user profile existing
    try:
        Userprofile.objects.get(user=instance)

    except Userprofile.DoesNotExist:
        Userprofile.objects.create(user=instance)

    #check whether to send an email or not if user just joined
    today = timezone.now()
    today = timezone.localtime(today)
    today = today.strftime("%m/%d/%Y %I:%M %p")
    today = datetime.strptime(today,"%m/%d/%Y %I:%M %p")
    date_joined = instance.date_joined
    date_joined = timezone.localtime(date_joined)
    date_joined = date_joined.strftime("%m/%d/%Y %I:%M %p")
    date_joined = datetime.strptime(date_joined,"%m/%d/%Y %I:%M %p")
    difference = today - date_joined
    difference = difference.total_seconds()
    
    #convert to a minute
    difference = difference / 60
    if difference <= 1:
        #send email
        print("it is less than it")
        header = f"Welcome to the Pizza Restaurant App {instance.username}"
        html_message = render_to_string("pizza/welcome_message.html",{"username":instance.username})
        plain_message = strip_tags(html_message)
        print("it is working up to here")
        send_mail(message=plain_message, from_email=settings.EMAIL_HOST_USER,subject=header,recipient_list=[instance.email],fail_silently=False,html_message=html_message)


@receiver(pre_save,sender=Creation)
def creation_pre_save_handler(instance,sender,**kwargs):
    #check if the name exists
    state = False
    try:
        creation_counts = Creation.objects.filter(name=instance.name)
        if len(creation_counts) > 1:
            state = True

        elif len(creation_counts) == 1:
            creation = Creation.objects.get(name=instance.name)
            if instance.id != creation.id:
                # it is a new creation
                state = True

        if state:
            count = creation_counts.count()
            instance.name = f"{instance.name} {count}"

    except Creation.DoesNotExist:
        state = not state

    instance.slug = (slugify(instance.name))

@receiver(post_save,sender=Creation)
def creation_post_save_handler(instance,sender,**kwargs):
    #check if an image exists,then create 
    if instance.price <= 0:
        #calculate price
        price = 0
        price += instance.pizza.price

        #check if there is at least a topping to calculate it
        if len(instance.toppings.all()) > 0:
            for topping in instance.toppings.all():
                price += topping.price

        #add the computed price
        # print(price)
        instance.price = price
        instance.save()

    if instance.picture is None:
        #create the picture
        toppings = []
        for topping in instance.toppings.all():
            toppings.append(topping.picture.url)

        new_image = mix_image(instance.pizza.picture.url,toppings)
        path = new_image.filename
        # print(new_image)

        #delete image
        if path:
            if image_file_converter(path) is not None:
                instance.picture = image_file_converter(path)
                instance.save()

            
        delete_image(path)
        

@receiver(pre_save,sender=Order)
def order_pre_save_handler(instance,sender,**kwargs):
    #check if there is a price
    if instance.price <= 0:
        price = instance.order.price * instance.pieces
        instance.price = price


#deletion handler for creation
@receiver(pre_delete,sender=Creation)
def creation_pre_delete_handler(instance,sender,**kwargs):
    if instance.picture is not None:
        try:
            image_info = api.resource(instance.picture.url)

            public_id = image_info["public_id"]
            cloudinary.uploader.destroy(public_id)
        
        except ResourceNotFound:
            state = False
    

#signal for removing availability of creation when topping is made not available
@receiver(post_save,sender=Topping)
def topping_post_handler(instance,sender,**kwargs):
    if instance.available == False:
        topping_creations = instance.toppings_creation.all()
        if len(topping_creations) > 0:
            for creation in topping_creations:
                if creation.available:
                    creation.available = False
                    creation.save()

#signal for removing availability of creation when pizza is made unavailable
@receiver(post_save,sender=Pizza)
def pizza_post_save_handler(instance,sender,**kwargs):
    if instance.available == False:
        pizza_creations = instance.pizza_creation.all()
        if len(pizza_creations) > 0:
            for creation in pizza_creations:
                if creation.available:
                    creation.available = False
                    creation.save()