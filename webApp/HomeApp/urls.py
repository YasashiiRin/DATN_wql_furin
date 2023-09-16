from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeview, name='home'), 
    path('redirectRegister',views.controller_redirect_register, name='redirectRegister'),
]
