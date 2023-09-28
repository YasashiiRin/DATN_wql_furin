# from django.contrib.sessions.models import Session
# from CarownerApp.models import Driver

# class CustomDriverAuthMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if 'id' in request.session:
#             id = request.session['id']
#             driver = Driver.objects.get(pk=id)
#             print(driver)
#             request.driver = driver
#             print(request.driver)
#         else:
#             print("check middleware function __call__ not activate")
#             request.driver = None

#         response = self.get_response(request)
#         return response
