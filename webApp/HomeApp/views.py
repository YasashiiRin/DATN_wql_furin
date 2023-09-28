from django.http import HttpResponseRedirect
from django.shortcuts import render , redirect
from django.contrib.auth import logout
def homeview(request):
    customername = None

    if hasattr(request, 'customer') and request.customer:
        customername = request.customer.name_customer

    return render(request, 'HomeApp/home.html', {
        'loginname': customername
    })

def controller_redirect_register(request):
    return redirect('login')
def controller_redirect_regisCustomer(request):
    return redirect('loginCustomer_view')
def handle_logout(request):
    logout(request)
    return render(request, 'HomeApp/home.html')
def driver_login_view(request):
    return render(request,'DriverApp/driver_login.html')