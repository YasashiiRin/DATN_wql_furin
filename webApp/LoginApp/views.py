from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password
from allauth.account.utils import send_email_confirmation
from django.core.mail import send_mail
from django.http import HttpResponse
import logging
import os
from .models import CustomerUser
logger = logging.getLogger(__name__)
def login_view(request):
    return render(request, 'LoginApp/login.html')

def handleRegis(request):
    if request.method == 'POST':
        username=request.POST['fullname']
        email=request.POST['email']
        password=request.POST['password']
        hashed_password=make_password(password)
        cu = CustomerUser(username=username,email=email,password=hashed_password)
        cu.save()
        # obcu = CustomerUser.objects.get(username=username)
        # send_email_confirmation(request, obcu)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(base_dir, 'templates/LoginApp/verifyEmail.html')
        with open(template_path, 'r') as email_file:
             email_content = email_file.read()
        subject = 'Xác Thực Tài Khoản'
        from_email='yoemfore@gmail.com'
        message = 'Xác thực tài khoản '
        to_email = [email]
        send_mail(subject,
            message,
            from_email,
            to_email,
            html_message=email_content,)
        return redirect('home')
    return render(request, 'LoginApp/login.html')
def back_home_view(request):
    return redirect('home')
