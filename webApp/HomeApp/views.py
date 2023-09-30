from django.http import HttpResponseRedirect
from django.shortcuts import render , redirect
from django.contrib.auth import logout
from CarownerApp.models import Driver,Schedules,Vehicle
from django.db.models import Prefetch
from django.http import JsonResponse
from LoginApp.models import Customer
def homeview(request):
    
    return render(request, 'HomeApp/home.html')
def home_customer_view(request):
    all_vehicles = Vehicle.objects.select_related('driver__carowner').prefetch_related(
        Prefetch('schedules_set', queryset=Schedules.objects.all())
    )
    return render(request, 'HomeApp/home_customer.html', {
        'vehicles': all_vehicles
    })
def controller_redirect_register(request):
    return redirect('login')
def controller_redirect_regisCustomer(request):
    return redirect('loginCustomer_view')
def handle_logout(request):
    logout(request)
    return render(request, 'HomeApp/home.html')
def driver_login_view(request):
    return render(request,'DriverApp/driver_login.html')
def handle_book_vehicle(request,vehicle_id,customer_id):
    try:
        vehicle_id = vehicle_id
        customer_id = customer_id
        print("vehicle_id : ", vehicle_id)
        print("customer_id : ", customer_id)
        vehicle = Vehicle.objects.get(pk=vehicle_id)
        customer =Customer.objects.get(pk=customer_id)
        driver = vehicle.driver
        carowner = driver.carowner
        schedule = Schedules.objects.get(vehicle=vehicle_id)
        name_customer_order = customer.name_customer
        name_driver_order = driver.name_driver
     
        name_vehicle_order = vehicle.name_vehicle
        name_carowner_order = carowner.username
        carowner_id = carowner.id
        quantity_slot = 1
        # pickup_location= schedule.start_location
        # dropoff_location = schedule.end_location
        # pickup_datetime= schedule.start_date_time
        # dropoff_datetime=schedule.end_date_time
        name_schedule_order = schedule.name_schedule
        print(" name_customer_order :",name_customer_order )
        print(" name_driver_order :",name_driver_order )
        print(" name_vehicle_order :",name_vehicle_order )
        print(" name_carowner_order :",name_carowner_order )
        print(" carowner_id :",carowner_id )
        print(" quantity_slot :",quantity_slot )
        print(" name_schedule_order :",name_schedule_order )
        # print(" pickup_location :",pickup_location )
        # print(" dropoff_location :",dropoff_location )
        # print(" pickup_datetime :",pickup_datetime )
        # print(" dropoff_datetime :",dropoff_datetime )

        return JsonResponse({'message': 'Đặt xe thành công'})

    except Vehicle.DoesNotExist or Customer.DoesNotExist:
        return JsonResponse({'error': 'Có lỗi xảy ra vui lòng liên hệ với quản trị viên'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)   