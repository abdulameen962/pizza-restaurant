from django.urls import path

from .import views

app_name = "pizza"
urlpatterns = [
    path("",views.index,name="index"),
    path("not-verified/",views.not_verified,name="not_verified"),
    path("dashboard/",views.dashboard,name="dashboard"),
]
