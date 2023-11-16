from django.urls import path
from .import views

urlpatterns = [
    path('driver/',views.driver,name='driver'),
    path('driver_login/',views.driver_login,name='driver_login'),
    path('handelLogin_driver/',views.handelLogin_driver, name='handelLogin_driver'),
    path('handle_verifi_driver/',views.handle_verifi_driver,name='handle_verifi_driver'),
    path('logout_driver',views.logout_driver,name='logout_driver'),
    path('activateD/<str:uid>/<str:token>/',views.activate_driver, name='activateD'),
    path('search_order/',views.search_order, name='search_order'),
    path('search_list_schedules/',views.search_list_schedules, name='search_list_schedules'),

    path('change_state/<int:driver_id>/<int:checkstate>/',views.change_state, name='change_state'),
]
