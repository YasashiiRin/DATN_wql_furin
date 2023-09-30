from telnetlib import LOGOUT
from django.shortcuts import render, redirect
from CarownerApp.models import Driver
from django.contrib.auth import login,logout
from django.contrib.auth.hashers import check_password
from LoginApp.backends.custom_auth import CustomerBackend
from CarownerApp.models import Driver,Orders

def driver(request):
    driver_id= request.driver.id
    driver_orders = Orders.objects.filter(vehicle__driver_id = driver_id)
    context ={
        'driver_orders': driver_orders
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
def handle_regis_driver(request):
    return render(request, 'DriverApp/driver_login.html')        
def logout_driver(request):
    logout(request)
    return render(request, 'DriverApp/driver_login.html')