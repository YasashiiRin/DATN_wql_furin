from django.contrib.sessions.models import Session
from LoginApp.models import Customer, CarOwner
from CarownerApp.models import Driver
from django.conf import settings

from CarownerApp.models import CustomSession
import json
class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
          try:
               isexist_session = CustomSession.objects.filter().all()
               print("have datas session")
               if isexist_session:
                    try: 
                         callback_sesson_customer = CustomSession.objects.get(session_key='customer_session_key')
                         if callback_sesson_customer:
                              print("callback_session for customer")
                              session_key = 'customer_session_key'
                              request.session[settings.CUSTOMER_SESSION_COOKIE_NAME] = session_key
                              
                    except CustomSession.DoesNotExist:
                         print("callback_customer_session is failed.....")
                         pass
               if isexist_session:
                    try:
                         callback_sesson_driver = CustomSession.objects.get(session_key='driver_session_key')
                         if callback_sesson_driver:
                              print("callback_session for driver.......")
                              session_key = 'driver_session_key'
                              request.session[settings.DRIVER_SESSION_COOKIE_NAME] = session_key  
                    except CustomSession.DoesNotExist:
                         print("callback_driver_session is failed.......")                               
          except CustomSession.DoesNotExist:
               print("haven't datas session.......")
               pass          
          if hasattr(settings, 'CUSTOMER_SESSION_COOKIE_NAME') and settings.CUSTOMER_SESSION_COOKIE_NAME in request.session:
               session_key = request.session[settings.CUSTOMER_SESSION_COOKIE_NAME]
               print("session_key : ", session_key)
               try:
                    custom_session = CustomSession.objects.get(session_key=session_key)
                    print("custom_session : ", custom_session)
                    session_data = json.loads(custom_session.session_data)
                    print("session_data : ", session_data)
                    user_id = session_data.get('user_id')
                    user_type = session_data.get('user_type')
                    print("user_id : ", user_id)
                    print("user_type : ", user_type)
                    if user_id:
                         try:
                              customer = Customer.objects.get(pk=user_id)
                              request.customer = customer
                         except Customer.DoesNotExist:
                              pass
            
               except CustomSession.DoesNotExist:
                    pass
          if hasattr(settings, 'DRIVER_SESSION_COOKIE_NAME') and settings.DRIVER_SESSION_COOKIE_NAME in request.session:
               session_key = request.session[settings.DRIVER_SESSION_COOKIE_NAME]
               print("session_key : ", session_key)
               try:
                    custom_session = CustomSession.objects.get(session_key=session_key)
                    print("custom_session : ", custom_session)
                    session_data = json.loads(custom_session.session_data)
                    print("session_data : ", session_data)
                    user_id = session_data.get('user_id')
                    user_type = session_data.get('user_type')
                    print("user_id : ", user_id)
                    print("user_type : ", user_type)
                    if user_id:
                         if user_id:
                              try:
                                   driver = Driver.objects.get(pk=user_id)
                                   request.driver = driver
                              except Driver.DoesNotExist:
                                   pass
            
               except CustomSession.DoesNotExist:
                    pass     
          response = self.get_response(request)
          return response
          # if hasattr(settings, 'CUSTOMER_SESSION_COOKIE_NAME') and settings.CUSTOMER_SESSION_COOKIE_NAME in request.session:
          #      info = request.session[settings.CUSTOMER_SESSION_COOKIE_NAME]
          #      id = info.get('id_customer')
          #      if id:
          #           try:
          #                customer = Customer.objects.get(pk=id)
          #                request.customer = customer
          #           except Customer.DoesNotExist:
          #                pass

          # if hasattr(settings, 'DRIVER_SESSION_COOKIE_NAME') and settings.DRIVER_SESSION_COOKIE_NAME in request.session:
          #      info = request.session[settings.DRIVER_SESSION_COOKIE_NAME]
          #      id = info.get('id_driver')
          #      if id:
          #           try:
          #                driver = Driver.objects.get(pk=id)
          #                request.driver = driver
          #           except Driver.DoesNotExist:
          #                pass

          # response = self.get_response(request)
          # return response
          # if 'customer_sessionid' in request.session:
          #      info = request.session['customer_sessionid']       
          #      id = info['id_customer']
          #      print("session_id",id)
          #      try:
          #           customer = Customer.objects.get(pk=id)
          #           request.customer = customer
          #           print("check user login :", customer.name_customer)
          #      except Customer.DoesNotExist:
          #           pass
          # if 'driver_sessionid' in request.session:
          #      info = request.session['driver_sessionid']       
          #      id = info['id_driver']
          #      print("session_id",id)
          #      try:
          #           driver = Driver.objects.get(pk=id)
          #           request.driver = driver
          #      except Driver.DoesNotExist:
          #           pass                                                                                                                              
          # response = self.get_response(request)
          # return response
