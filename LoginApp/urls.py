from django.urls import path
from allauth.account.views import ConfirmEmailView
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'), 
    path('register/',views.handleRegis,name='register'),
    path('back_home/', views.back_home_view, name='back_home'),
    path('verifyEmail/', views.verifyEmail_view, name='verifyEmail'),
    path('activate/<str:uid>/<str:token>/', views.activate, name='activate'),
    path('handleLogin/',views.handelLogin,name='handleLogin'),
    path('handleRegis_customer/',views.handleRegis_customer,name='handleRegis_customer'),
    path('handelLogin_customer/',views.handelLogin_customer,name='handelLogin_customer'),
    path('loginCustomer_view/', views.loginCustomer_view, name='loginCustomer_view'), 
    path('activateO/<str:uid>/<str:token>/', views.activate_Customer, name='activateO'),

    path('activateS/<str:email>/', views.handle_forgetPass, name='activateS'),
    path('sendEmail_forgetPass/', views.sendEmail_forgetPass, name='sendEmail_forgetPass'),
    # path('activateD/<str:uid>/<str:token>/',views.activate_driver, name='activateD'),
]
