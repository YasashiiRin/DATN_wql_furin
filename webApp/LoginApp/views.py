from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import check_password
from django.http import Http404
from django.contrib.auth import authenticate,login
from LoginApp.backends.custom_auth import CustomerBackend
import os
from .models import CarOwner,Customer
def login_view(request):
    return render(request, 'LoginApp/login.html')
def loginCustomer_view(request):
    return render(request, 'LoginApp/LoginCustomer.html')
def handleRegis(request):
    if request.method == 'POST':
        username=request.POST['fullname']
        email=request.POST['email']
        password=request.POST['password']
        hashed_password=make_password(password)
        token = get_random_string(32)
        if CarOwner.objects.filter(email=email).exists():
            return render(request, 'LoginApp/Login.html',{
                'islogin':'signup'
            })
        ca = CarOwner(username=username,email=email,password=hashed_password,token_carowner=token)
        ca.save()
        user_id = ca.id
        user_name= ca.username
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
        return render(request, 'LoginApp/notify_loading.html',{
            'islogin':'faild'
        })
    return render(request, 'LoginApp/verifyEmail.html')
def back_home_view(request):
    return redirect('home')
def verifyEmail_view(request):
    return render(request, 'LoginApp/verifyEmail.html',{
        'name': 'verifyEmail'
    })

def activate(request,uid,token):
    try:
        ca = CarOwner.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CarOwner().DoesNotExist):
        ca = None

    if ca is not None and ca.token_carowner == token:
        ca.verify_carowner = True
        ca.save()
        return render(request, 'LoginApp/verifyEmail_success.html')  # Hiển thị trang xác thực thành công
    else:
        raise Http404
def activate_Customer(request,uid,token):
    try:
        cm = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Customer().DoesNotExist):
        cm = None

    if cm is not None and cm.token_customer == token:
        cm.verify_customer = True
        cm.save()
        return render(request, 'LoginApp/verifyEmail_success.html')  # Hiển thị trang xác thực thành công
    else:
        raise Http404      
def handelLogin(request):
   if request.method == 'POST':
        email_user=request.POST['email']
        password_user=request.POST['password']
        try :
            user=CarOwner.objects.get(email=email_user)
            if user.check_password(password_user):
                if user.verify_user:
                    login(request,user,backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('home')
                else :
                    return render(request, 'LoginApp/Login.html',{
                    'islogin': 'faild',
                 })  
            else :
                 return render(request, 'LoginApp/Login.html',{
                'islogin': 'faild',
            })
        except CarOwner.DoesNotExist:
                return render(request, 'LoginApp/Login.html',{
                'islogin': 'faild',
            })
def handleRegis_customer(request):
    if request.method == 'POST':
        username=request.POST['fullname']
        email=request.POST['email']
        password=request.POST['password']
        hashed_password=make_password(password)
        token = get_random_string(32)
        if Customer.objects.filter(email_customer=email).exists():
            return render(request, 'LoginApp/LoginCustomer.html',{
                'islogin':'signup'
            })
        cm = Customer(name_customer=username,email_customer=email,password_customer=hashed_password,token_customer=token)
        cm.save()
        cm_id = cm.id
        cm_name= cm.name_customer
        subject = 'Xác Thực Tài Khoản'
        from_email='yoemfore@gmail.com'
        message=''
        contenHTML = render_to_string('LoginApp/verifyEmail.html', {
            'name_user':cm_name,
            'activation_url': 'http://127.0.0.1:8000/activateO/{}/{}'.format(cm_id,token),
        })
        to_email = [email]
        send_mail(subject,
            message,
            from_email,
            to_email,
            html_message=contenHTML,
            )
        return render(request, 'LoginApp/notify_loading.html',{
            'islogin':'faild'
        })
    return render(request, 'LoginApp/verifyEmail.html')        
def handelLogin_customer(request):
    if request.method == 'POST':
        email_customer=request.POST['email']
        password_customer=request.POST['password']
        try :
            user=Customer.objects.get(email_customer=email_customer)
            if check_password(password_customer, user.password_customer):
                if user.verify_customer:
                    print("xác thực thành công")
                    user.backend = 'LoginApp.backends.custom_auth.CustomerBackend'
                    CustomerBackend.custom_login(request,user)
                    return redirect('home')   
                else :
                    return render(request, 'LoginApp/LoginCustomer.html',{
                        'islogin': 'noverifi',
                        })  
            else :
                return render(request, 'LoginApp/LoginCustomer.html',{
                    'islogin': 'faildpass',
                   })  
        except Customer.DoesNotExist:
            return render(request, 'LoginApp/LoginCustomer.html',{
                'islogin': 'faild',
            })
