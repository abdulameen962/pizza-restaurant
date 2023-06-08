from django.db.models.signals import pre_save,post_save,pre_delete,post_delete
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from .models import *

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
    #check if an image exists,then create 
    status = ""
    if instance.picture is None:
        #create the picture
        status = False

    if instance.price <= 0:
        #calculate price
        price = 0
        price += instance.pizza.price

        #check if there is at least a topping to calculate it
        if len(instance.toppings.all()) > 0:
            for topping in instance.toppings.all():
                price += topping.price

        #add the computed price
        instance.price = price

@receiver(pre_save,sender=Order)
def order_pre_save_handler(instance,sender,**kwargs):
    #check if there is a price
    if instance.price <= 0:
        price = instance.order.price * instance.pieces
        instance.price = price