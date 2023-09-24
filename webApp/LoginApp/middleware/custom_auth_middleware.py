from django.contrib.sessions.models import Session
from LoginApp.models import Customer

class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'id' in request.session:
            id = request.session['id']
            customer = Customer.objects.get(pk=id)
            print(customer)
            request.customer = customer
            print(request.customer)
        else:
            print("check middleware activate")
            request.customer = None

        response = self.get_response(request)
        return response
