from django.contrib.sessions.models import Session
from LoginApp.models import Customer
from CarownerApp.models import Driver

class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
            if 'id' in request.session:
                id = request.session['id']
                try:
                    driver = Driver.objects.get(pk=id)
                    request.driver = driver
                except Driver.DoesNotExist:
                    try:
                        customer = Customer.objects.get(pk=id)
                        request.customer = customer
                    except Customer.DoesNotExist:
                        pass
            else:
                print("check middleware activate")
            response = self.get_response(request)
            return response
