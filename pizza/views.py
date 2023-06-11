from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from allauth.account.models  import EmailAddress
from django.contrib import admin,messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from allauth.account.decorators import verified_email_required
from allauth_2fa.utils import user_has_valid_totp_device
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from .signals import *
from .models import *
# Ensure users go through the allauth workflow when logging into admin.
admin.site.login = staff_member_required(admin.site.login, login_url='/users/login/')
# Run the standard admin set-up.
admin.autodiscover()

# Create your views here.
def index(request):
    user = request.user
    
    if user.is_authenticated:
        emailuser = EmailAddress.objects.get(user=user)

        if emailuser.verified:
            return HttpResponseRedirect(reverse("pizza:dashboard"))
        else:
            messages.error(request,"Check your email for a verification link,you are not verified")
            return HttpResponseRedirect(reverse("pizza:not_verified"))
    else:
        return render(request,"pizza/index.html")


@login_required(login_url="account_login")
def not_verified(request):
    #confirm user doesn't have a verified email
    user = request.user
    emailuser = EmailAddress.objects.get(user=user)
    if emailuser.verified:
        return HttpResponseRedirect(reverse("index"))

    return render(request,"account/verified_email_required.html")


def lowest(pizzas):
    lowest_pizza = ""

    for pizza in pizzas:
        for second in pizzas:
            if pizza != second:
                if len(pizza.creation_orders.all()) <= len(pizza.creation_orders.all()):
                    if lowest_pizza == "":
                        lowest_pizza = pizza

                    elif len(pizza.creation_orders.all()) < len(lowest_pizza.creation_orders.all()):
                        lowest_pizza = pizza

    return lowest_pizza

def lowestCreator(creators):
    lowest_creator = ""

    for first in creators:
        for second in creators:
            if first != second:
                if len(first.creations.all()) <= len(second.creations.all()):
                    if lowest_creator == "":
                        lowest_creator = first

                    elif len(first.creations.all()) < len(lowest_creator.creations.all()):
                        lowest_creator = first

    return lowest_creator
@login_required(login_url="account_login")
@verified_email_required
def dashboard(request):
    #calculate user total completd orders and total money spent
    user = request.user
    user_money_spent = 0
    user_completed_orders = 0
    user_pending_orders = 0

    try:
        user_orders = user.user_profile.orders.filter(status="COMPLETED")
        user_completed_orders += len(user_orders)
        if len(user_orders) > 0:
            for order in user_orders:
                user_money_spent += order.price

    except Order.DoesNotExist:
        user_money_spent = 0
        user_completed_orders = 0

    #calculate user pending orders
    try:
        user_pending = user.user_profile.orders.filter(status="PENDING")
        user_pending_orders += len(user_pending)
    except Order.DoesNotExist:
        user_pending_orders = 0

    #calculate user creations
    try:
        user_creations = user.creations.all().count()

    except Creation.DoesNotExist:
        user_creations = 0

    #get trending pizzas
    trending_pizzas = set()

    pizzas = Creation.objects.filter(available=True)
    if len(pizzas) > 0:
        for pizza in pizzas:
            for second in pizzas:
                if pizza != second:
                    if len(pizza.creation_orders.all()) > len(second.creation_orders.all()):
                        if len(trending_pizzas) < 6:
                            trending_pizzas.add(pizza)

                        else:
                            lowest_amount = lowest(trending_pizzas)
                            if len(pizza.creation_orders.all()) > len(lowest_amount.creation_orders.all()):
                                trending_pizzas.remove(lowest_amount)
                                trending_pizzas.add(pizza)

    #get trending creators
    trending_creators = set()
    creators = set()
    if len(pizzas) > 0:
        for pizza in pizzas:
            creators.add(pizza.creator)

        for creator in creators:
             for creator2 in creators:
                if creator != creator2:
                    if len(creator.creations.all()) > len(creator2.creations.all()):
                        if len(trending_creators) < 6:
                            trending_creators.add(creator)

                        else:
                            lowest_creator = lowestCreator(trending_creators)
                            if len(creator.creations.all()) > len(lowest_creator.creations.all()):
                                trending_creators.remove(lowest_creator)
                                trending_creators.add(creator)

    
    #check if user 2fa is authenticated
    data = {
        "2fa_verified": user_has_valid_totp_device(user),
        "user_money_spent": user_money_spent,
        "user_completed_orders": user_completed_orders,
        "user_pending_orders": user_pending_orders,
        "user_creations": user_creations,
        "trending_pizzas": trending_pizzas,
        "trending_creators": trending_creators,
    }
    return render(request,"pizza/dashboard.html",data)

