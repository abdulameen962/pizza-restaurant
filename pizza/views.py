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


@login_required(login_url="account_login")
@verified_email_required
def dashboard(request):
    #check if user 2fa is authenticated

    return render(request,"pizza/dashboard.html",{
        "2fa_verified": user_has_valid_totp_device(request.user)
    })

