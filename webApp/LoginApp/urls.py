from django.urls import path
from allauth.account.views import ConfirmEmailView
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'), 
    path('register/',views.handleRegis,name='register'),
    path('back_home/', views.back_home_view, name='back_home'),
    path('accounts/confirm-email/<str:key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
]
