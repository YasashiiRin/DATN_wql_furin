
from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.conf import settings
class CustomLogoutMiddleware:
    _global_customer_id = None
    
    _global_driver_id = None
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("varible_global_customer: ",CustomLogoutMiddleware._global_customer_id)
        print("varible_global_driver: ",CustomLogoutMiddleware._global_driver_id)
        response = self.get_response(request)
        try:
            if 'customer_sessionid' in request.session:
                print("middleware tồn tại session customer")
                CustomLogoutMiddleware._global_customer_id = request.customer.id
        except:
            CustomLogoutMiddleware._global_customer_id = None
        try:
            if 'driver_sessionid' in request.session:
                print("middleware tồn tại session customer")
                CustomLogoutMiddleware._global_driver_id = request.driver.id
        except:
            CustomLogoutMiddleware._global_driver_id = None

        if request.path == '/admin/logout/':
            print("Custom Logout Middleware: Custom logout action--------------------------------")
            session_key_to_delete = request.session.session_key
            Session.objects.filter(session_key=session_key_to_delete).delete()
            if CustomLogoutMiddleware._global_customer_id is not None:
                print("------------CUSTOMER ID--------------",CustomLogoutMiddleware._global_customer_id,"--------------------------")
                userid = CustomLogoutMiddleware._global_customer_id
                session_key = f'customer_{userid}_session_key'
                request.session[settings.CUSTOMER_SESSION_COOKIE_NAME] = session_key
            if CustomLogoutMiddleware._global_driver_id is not None:
                print("------------DRIVER ID--------------",CustomLogoutMiddleware._global_driver_id,"--------------------------")
                userid = CustomLogoutMiddleware._global_driver_id
                session_key = f'driver_{userid}_session_key'
                request.session[settings.DRIVER_SESSION_COOKIE_NAME] = session_key
            return render(request, 'HomeApp/home.html')
        if request.path=='/logout_driver':
            print("driver_logout_test middelware")
            CustomLogoutMiddleware._global_driver_id = None
            return render(request, 'HomeApp/home.html')
        if request.path=='/handle_logout':
            print("customer_logout_test middelware")
            CustomLogoutMiddleware._global_customer_id = None
            return render(request, 'HomeApp/home.html')
        try:
            if CustomLogoutMiddleware._global_customer_id:
                print("------------CUSTOMER ID--------------",CustomLogoutMiddleware._global_customer_id,"--------------------------")
        except:
            pass
        try:
            if CustomLogoutMiddleware._global_driver_id:
                print("------------DRIVER ID--------------",CustomLogoutMiddleware._global_driver_id,"--------------------------")
        except:
            pass
        return response

