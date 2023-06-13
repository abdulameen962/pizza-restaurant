from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from allauth.account.models  import EmailAddress
from django.contrib import admin,messages
from django.views.generic import View,ListView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from allauth.account.decorators import verified_email_required
from allauth_2fa.utils import user_has_valid_totp_device
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from .signals import *
import random
from django.contrib.auth.mixins import UserPassesTestMixin
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
                if len(first.creations.filter(available=True)) <= len(second.creations.filter(available=True)):
                    if lowest_creator == "":
                        lowest_creator = first

                    elif len(first.creations.filter(available=True)) < len(lowest_creator.creations.filter(available=True)):
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
        user_creations = user.creations.filter(available=True).count()

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
                    if len(creator.creations.filter(available=True)) > len(creator2.creations.filter(available=True)):
                        if len(trending_creators) < 6:
                            trending_creators.add(creator)

                        else:
                            lowest_creator = lowestCreator(trending_creators)
                            if len(creator.creations.filter(available=True)) > len(lowest_creator.creations.filter(available=True)):
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


@login_required(login_url="account_login")
@verified_email_required
def search(request,method):
    user = request.user

    data = request.body
    command = data.get("command",)
    search_term = data.get("search_term",)

    if request.method == "POST":
        results = set()
        if command == "category":
            categories = Category.objects.all()
            for category in categories:
                state = False
                if search_term in category.title:
                    state = True

                elif search_term in category.code:
                    state = True

                if state:
                    category_creations = category.pizza_category.filter(available=True)
                    if len(category_creations) > 0:
                        for creation in category_creations:
                            results.add(creation)

                state = False

        elif command == "menu":
            menus = Creation.objects.filter(available=True)
            for menu in menus:
                if search_term in menu.name:
                    results.add(menu)

                elif search_term in menu.description:
                    results.add(menu)

        
        elif command == "topping":
            toppings = Topping.objects.filter(available=True)
            if toppings.count() > 0:
                for topping in toppings:
                    if search_term in topping.name:
                        #return all the creations with the topping
                        topping_creations = topping.toppings_creation.filter(available=True)
                        if len(topping_creations) > 0:
                            for creation in topping_creations:
                                results.add(creation)


        elif command == "pizza":
            pizzas = Pizza.objects.filter(available=True)
            if pizzas.count() > 0:
                for pizza in pizzas:
                    if search_term in pizza.name:
                        #return all creations with the pizza
                        pizza_creations = pizza.pizza_creation.filter(available=True)
                        if len(pizza_creations) > 0:
                            for creation in pizza_creations:
                                results.add(creation)

        if method == "checker":
            #the redirect vibe
            if len(results) > 0:
                responses = []
                for creation_result in results:
                    url = request.build_absolute_uri(reverse('menu_single',args=[creation_result.slug]))
                    creation_result_add = {"creation":creation_result.serialize(),"link": url}
                    responses.append(creation_result_add)

                return JsonResponse(responses,status=200,safe=False)

        elif method == "mover":
            if len(results) > 0:
                responses = []
                for creation_result in results:
                    url = request.build_absolute_uri(reverse('menu_single',args=[creation_result.slug]))
                    responses.append(url)

                redirect_url = random.choices(responses,k=1)[0]

                return HttpResponseRedirect(redirect_url)

        return JsonResponse({"message":"Search term not found or no pizza creation for your search term"},status=200)

    return JsonResponse({"message":"wrong request method"},status=400)


class menus(ListView,UserPassesTestMixin):
    model = Creation
    template_name = "pizza/menus.html"
    context_object_name = "menus"
    paginate_by = 15

    login_url = "account_login"

    def test_func(self):
        user = self.request.user
        emailuser = EmailAddress.objects.get(user=user)
        return user.is_authenticated and emailuser.verified

    def get_queryset(self):
        creations = Creation.objects.filter(available=True)

        return creations

    def get_context_data(self, **kwargs) :
        creations = Creation.objects.filter(available=True)
        creations = Paginator(creations,15)
        context = super().get_context_data(**kwargs)

        context["max_num"] = creations.num_pages
        context["page_request_var"] = "page"
        context["page_range"] = creations.page_range

        return context

class menu_single(View,UserPassesTestMixin):
    login_url = "account_login"

    def test_func(self):
        user = self.request.user
        emailuser = EmailAddress.objects.get(user=user)
        return user.is_authenticated and emailuser.verified

    def get(self,request,slug):
        try:
            menu = Creation.objects.get(slug=slug,available=True)
            data = {"menu":menu}
            return render(request,"pizza/menu_single.html",data)
        except Creation.DoesNotExist:
            return HttpResponseRedirect(reverse("pizza:menus"))

