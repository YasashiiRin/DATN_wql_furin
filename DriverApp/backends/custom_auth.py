
# from CarownerApp.models import Driver 
# from django.contrib.auth.backends import ModelBackend
# from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.hashers import check_password

# class DriverBackend(ModelBackend):
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         try:
#             user = Driver.objects.get(email_driver=email)
#             print("authen"+ user.email_driver)
#             print("authen"+ user.password_driver)
#             print("authen"+ password)
#             if check_password(password,user.password_driver):
#                 return user       
#         except ObjectDoesNotExist:
#             pass  

#         return None 

#     def custom_login(request, user):
#         request.session['id'] = user.id
#         print("check id :", user.id)
#         return user
