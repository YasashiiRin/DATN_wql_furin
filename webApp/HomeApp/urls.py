from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeview, name='home'), 
    path('redirectRegister',views.controller_redirect_register, name='redirectRegister'),
    path('handle_logout',views.handle_logout,name='handle_logout'),
    path('controller_redirect_regisOwnercar',views.controller_redirect_regisOwnercar, name='controller_redirect_regisOwnercar'),
]
