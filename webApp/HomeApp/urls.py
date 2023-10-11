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
    path('book_vehicle/<int:schedule_id>/<int:customer_id>/<int:slot>/',views.handle_book_vehicle,name='handle_book_vehicle'),
    path('search_customer/',views.search_customer, name='search_customer'),
    path('view_profile_customer',views.view_profile_customer,name='view_profile_customer'),
    path('view_editprofile',views.view_editprofile,name='view_editprofile'),
    path('upload_images/<int:customerid>/',views.upload_images,name='upload_images'),
    path('save_edit_info/',views.save_edit_info,name='save_edit_info'),
    path('custom_logout/',views.custom_logout, name='custom_logout'),
]
