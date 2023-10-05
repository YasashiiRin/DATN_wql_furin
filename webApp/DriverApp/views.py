from telnetlib import LOGOUT
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from CarownerApp.models import Driver
from django.contrib.auth import login,logout
from django.contrib.auth.hashers import check_password
from LoginApp.backends.custom_auth import CustomerBackend
from CarownerApp.models import Driver,Orders,Schedules,Vehicle
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.crypto import get_random_string


def driver(request):
    current_date = timezone.now().date()
    driver_id= request.driver.id
    driver_orders = Orders.objects.filter(vehicle__driver_id = driver_id)
    vehicle = Vehicle.objects.filter(driver=driver_id).all()
    filtered_schedules = Schedules.objects.filter(vehicle__driver = driver_id).all()
    all_shedules= [schedule for schedule in filtered_schedules if schedule.start_date >= current_date]
    context ={
        'driver_orders': driver_orders,
        'all_schedules' : list(all_shedules),
    }
    return render(request, 'DriverApp/driver.html',context)
def driver_login(request):
    return render(request, 'DriverApp/driver_login.html')
def handelLogin_driver(request):
   if request.method == 'POST':
        email_driver=request.POST['email']
        password=request.POST['password']
        try :
            user=Driver.objects.get(email_driver=email_driver)
            if check_password(password, user.password_driver):
                if user.verify_driver:
                    print("xác thực thành công")
                    user.backend = 'LoginApp.backends.custom_auth.CustomerBackend'
                    CustomerBackend.custom_login(request,user,'driver')
                    return redirect('driver')  
                else :
                    return render(request, 'DriverApp/driver_login.html',{
                        'islogin': 'noverifi',
                        })  
            else :
                return render(request, 'DriverApp/driver_login.html',{
                    'islogin': 'faildpass',
                   })  
        except Driver.DoesNotExist:
            return render(request, 'DriverApp/driver_login.html',{
                'islogin': 'faild',
 
            })        
def handle_verifi_driver(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        print("email_driver_get :", email)
        print("pass_driver_get :", password)
        token = get_random_string(32)
        dr=Driver.objects.get(email_driver=email)
        if dr.verify_driver == True:
            return render(request, 'DriverApp/driver_login.html',{
                'islogin' : 'verifi_isexists'
            })
        if check_password(password, dr.password_driver):
            dr.token_driver = token
            dr.save()
            user_id = dr.id
            user_name= dr.name_driver
            subject = 'Xác Thực Tài Khoản'
            from_email='yoemfore@gmail.com'
            message=''
            contenHTML = render_to_string('LoginApp/verifyEmail.html', {
                'name_user':user_name,
                'activation_url': 'http://127.0.0.1:8000/activateD/{}/{}'.format(user_id,token),
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
        else :
            return render(request, 'DriverApp/driver_login.html',{
            'islogin': 'faild',
        })
    return render(request, 'DriverApp/driver_login.html')        
def logout_driver(request):
    logout(request)
    return render(request, 'DriverApp/driver_login.html')