from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import check_password
from django.http import Http404
from django.contrib.auth import authenticate,login
from LoginApp.backends.custom_auth import OwnerCarBackend
import os
from .models import CustomerUser,OwnerCar
def login_view(request):
    return render(request, 'LoginApp/login.html')
def loginOwnercar_view(request):
    return render(request, 'LoginApp/LoginOwnercar.html')
def handleRegis(request):
    if request.method == 'POST':
        username=request.POST['fullname']
        email=request.POST['email']
        password=request.POST['password']
        hashed_password=make_password(password)
        token = get_random_string(32)
        if CustomerUser.objects.filter(email=email).exists():
            return render(request, 'LoginApp/Login.html',{
                'islogin':'signup'
            })
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
        cu = CustomerUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomerUser().DoesNotExist):
        cu = None

    if cu is not None and cu.token_user == token:
        cu.verify_user = True
        cu.save()
        return render(request, 'LoginApp/verifyEmail_success.html')  # Hiển thị trang xác thực thành công
    else:
        raise Http404
def activate_Ownercar(request,uid,token):
    try:
        oc = OwnerCar.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, OwnerCar().DoesNotExist):
        oc = None

    if oc is not None and oc.token_ownercar == token:
        oc.verify_ownercar = True
        oc.save()
        return render(request, 'LoginApp/verifyEmail_success.html')  # Hiển thị trang xác thực thành công
    else:
        raise Http404      
def handelLogin(request):
   if request.method == 'POST':
        email_user=request.POST['email']
        password_user=request.POST['password']
        try :
            user=CustomerUser.objects.get(email=email_user)
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
        except CustomerUser.DoesNotExist:
                return render(request, 'LoginApp/Login.html',{
                'islogin': 'faild',
            })
def handleRegis_ownercar(request):
    if request.method == 'POST':
        username=request.POST['fullname']
        email=request.POST['email']
        password=request.POST['password']
        hashed_password=make_password(password)
        token = get_random_string(32)
        if OwnerCar.objects.filter(email_ownercar=email).exists():
            return render(request, 'LoginApp/LoginOwnercar.html',{
                'islogin':'signup'
            })
        oc = OwnerCar(name_ownercar=username,email_ownercar=email,password_ownercar=hashed_password,token_ownercar=token)
        oc.save()
        oc_id = oc.id
        oc_name= oc.name_ownercar
        subject = 'Xác Thực Tài Khoản'
        from_email='yoemfore@gmail.com'
        message=''
        contenHTML = render_to_string('LoginApp/verifyEmail.html', {
            'name_user':oc_name,
            'activation_url': 'http://127.0.0.1:8000/activateO/{}/{}'.format(oc_id,token),
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
def handelLogin_ownercar(request):
    if request.method == 'POST':
        email_ownercar=request.POST['email']
        password_ownercar=request.POST['password']
        try :
            user=OwnerCar.objects.get(email_ownercar=email_ownercar)
            if check_password(password_ownercar, user.password_ownercar):
                if user.verify_ownercar:
                    print("xác thực thành công")
                    user.backend = 'LoginApp.backends.custom_auth.OwnerCarBackend'
                    OwnerCarBackend.custom_login(request,user)
                    return redirect('home')   
                else :
                    return render(request, 'LoginApp/LoginOwnercar.html',{
                        'islogin': 'noverifi',
                        })  
            else :
                return render(request, 'LoginApp/LoginOwnercar.html',{
                    'islogin': 'faildpass',
                   })  
        except OwnerCar.DoesNotExist:
            return render(request, 'LoginApp/LoginOwnercar.html',{
                'islogin': 'faild',
            })
