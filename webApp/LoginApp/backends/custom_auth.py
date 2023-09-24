
from LoginApp.models import Customer
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password

class CustomerBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Customer.objects.get(email_customer=email)
            print("authen"+ user.email_customer)
            print("authen"+ user.password_customer)
            print("authen"+ password)
            if check_password(password,user.password_customer):
                return user       
        except ObjectDoesNotExist:
            pass  

        return None 

    def custom_login(request, user):
        request.session['id'] = user.id
        print("check id :", user.id)
        return user
