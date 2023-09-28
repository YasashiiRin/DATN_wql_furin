from django.urls import path
from .import views

urlpatterns = [
    path('driver/',views.driver,name='driver'),
    path('driver_login/',views.driver_login,name='driver_login'),
    path('handelLogin_driver/',views.handelLogin_driver, name='handelLogin_driver'),
    path('handle_regis_driver/',views.handelLogin_driver,name='handle_regis_driver'),
    path('logout_driver',views.logout_driver,name='logout_driver'),
]