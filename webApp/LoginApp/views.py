from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password
from allauth.account.utils import send_email_confirmation
from django.core.mail import send_mail
from django.http import HttpResponse
import logging
from .models import User
logger = logging.getLogger(__name__)
def login_view(request):
    return render(request, 'LoginApp/login.html')
def handleRegis(request):
    if request.method == 'POST':
        username=request.POST['fullname']
        email=request.POST['email']
        password=request.POST['password']
        hashed_password=make_password(password)
        user = User(name=username,email=email,password=hashed_password)
        user.save()
        send_email_confirmation(request, User)
        return redirect('home')
    return render(request, 'LoginApp/login.html')
def back_home_view(request):
    return redirect('home')
