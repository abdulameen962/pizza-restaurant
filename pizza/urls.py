from django.urls import path

from .import views

app_name = "pizza"
urlpatterns = [
    path("",views.index,name="index"),
    path("not-verified/",views.not_verified,name="not_verified"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("menus/",views.menus.as_view(),name="menus"),
    path("menus/<str:slug>/",views.menu_single.as_view(),name="menu_single"),
    path("creators/",views.creators.as_view(),name="creators"),
    path("creators/<str:username>/",views.creator_single.as_view(),name="creator_single"),
    

    #Api routes
    path("search/<str:method>/",views.search,name="search"),
    path("creations/<int:page>",views.creations,name="creation_pages"),
]
