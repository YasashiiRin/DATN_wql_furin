
from LoginApp.models import OwnerCar
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password

class OwnerCarBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = OwnerCar.objects.get(email_ownercar=email)
            print("authen"+ user.email_ownercar)
            print("authen"+ user.password_ownercar)
            print("authen"+ password)
            if check_password(password,user.password_ownercar):
                return user       
        except ObjectDoesNotExist:
            pass  

        return None 

    def custom_login(request, user):
        request.session['id'] = user.id
        print("check id :", user.id)
        return user
