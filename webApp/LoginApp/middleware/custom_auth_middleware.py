from django.contrib.sessions.models import Session
from LoginApp.models import OwnerCar

class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'id' in request.session:
            id = request.session['id']
            owner = OwnerCar.objects.get(pk=id)
            print(owner)
            request.owner = owner
            print(request.owner)
        else:
            print("check middleware activate")
            request.owner = None

        response = self.get_response(request)
        return response
