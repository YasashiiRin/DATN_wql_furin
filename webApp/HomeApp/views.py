from django.shortcuts import render , redirect
from django.contrib.auth import logout

def homeview(request):
    if request.owner:
        print("--ownercar -")
        return render(request, 'HomeApp/home.html',{
            'loginname': request.owner.name_ownercar
         })
    elif request.user:
        print("---user----")
        return render(request, 'HomeApp/home.html',{
            'loginname' : request.user.username,
        })

def controller_redirect_register(request):
    return redirect('login')
def controller_redirect_regisOwnercar(request):
    return redirect('loginOwnercar_view')
def handle_logout(request):
    logout(request)
    return render(request, 'HomeApp/home.html')
