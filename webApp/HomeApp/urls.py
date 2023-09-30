from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.homeview, name='home'), 
    path('home_customer_view',views.home_customer_view,name='home_customer_view'),
    path('redirectRegister',views.controller_redirect_register, name='redirectRegister'),
    path('handle_logout',views.handle_logout,name='handle_logout'),
    path('controller_redirect_regisCustomer',views.controller_redirect_regisCustomer, name='controller_redirect_regisCustomer'),
    path('driver_login_view/',views.driver_login_view,name='driver_login_view'),
    path('book_vehicle/<int:vehicle_id>/<int:customer_id>/',views.handle_book_vehicle,name='handle_book_vehicle')
]
