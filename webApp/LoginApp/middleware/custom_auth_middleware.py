from django.contrib.sessions.models import Session
from LoginApp.models import Customer
from CarownerApp.models import Driver

class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
            if 'info_login' in request.session:
                 info = request.session['info_login']       
                 user_type = info['user_type']   
                 id = info['id']
                 print("session_id",id)
                 print("session_user_type :", user_type)
                 if user_type == 'customer':
                      try:
                           customer = Customer.objects.get(pk=id)
                           request.customer = customer
                           print("check user login :", customer.name_customer)
                      except Customer.DoesNotExist:
                           pass
                 elif user_type == 'driver':
                      try:
                           driver = Driver.objects.get(pk=id)
                           request.driver = driver
                      except Driver.DoesNotExist:
                           pass               
                         
                                                                                                                                                                                                
            response = self.get_response(request)
            return response
