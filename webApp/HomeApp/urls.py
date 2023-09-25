from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.homeview, name='home'), 
    path('redirectRegister',views.controller_redirect_register, name='redirectRegister'),
    path('handle_logout',views.handle_logout,name='handle_logout'),
    path('controller_redirect_regisCustomer',views.controller_redirect_regisCustomer, name='controller_redirect_regisCustomer'),
]
