from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.http import Http404
import os
from .models import CustomerUser
def login_view(request):
    return render(request, 'LoginApp/login.html')

def handleRegis(request):
    if request.method == 'POST':
        username=request.POST['fullname']
        email=request.POST['email']
        password=request.POST['password']
        hashed_password=make_password(password)
        token = get_random_string(32)
        cu = CustomerUser(username=username,email=email,password=hashed_password,token_user=token)
        cu.save()
        user_id = cu.id
        user_name= cu.username
        subject = 'Xác Thực Tài Khoản'
        from_email='yoemfore@gmail.com'
        message=''
        contenHTML = render_to_string('LoginApp/verifyEmail.html', {
            'name_user':user_name,
            'activation_url': 'http://127.0.0.1:8000/activate/{}/{}'.format(user_id,token),
        })
        to_email = [email]
        send_mail(subject,
            message,
            from_email,
            to_email,
            html_message=contenHTML,
            )
        return render(request, 'LoginApp/notify_loading.html')
    return render(request, 'LoginApp/verifyEmail.html')
def back_home_view(request):
    return redirect('home')
def verifyEmail_view(request):
    return render(request, 'LoginApp/verifyEmail.html',{
        'name': 'verifyEmail'
    })

def activate(request,uid,token):
    try:
        cu = CustomerUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomerUser().DoesNotExist):
        cu = None

    if cu is not None and cu.token_user == token:
        cu.verify_user = True
        cu.save()
        return render(request, 'LoginApp/verifyEmail_success.html')  # Hiển thị trang xác thực thành công
    else:
        raise Http404 
