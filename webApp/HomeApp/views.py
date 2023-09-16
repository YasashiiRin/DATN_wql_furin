from django.shortcuts import render , redirect

def homeview(request):
    return render(request, 'HomeApp/home.html')
def controller_redirect_register(request):
    return redirect('login')
