from django.http import HttpResponseRedirect
from django.shortcuts import render , redirect
from django.contrib.auth import logout
from CarownerApp.models import Driver,Schedules,Vehicle,Orders
from django.db.models import Prefetch
from django.http import JsonResponse
from LoginApp.models import Customer
from django.utils import timezone
from .forms import YourFilterForm
from django.db.models import Q
def homeview(request):
    
    return render(request, 'HomeApp/home.html')
def home_customer_view(request):
    current_date = timezone.now().date()
    my_filter_form = YourFilterForm()
    my_orders = Orders.objects.filter(customer = request.customer.id).all()
    filtered_schedules = Schedules.objects.select_related('vehicle__driver__carowner').all()
    all_shedules= [schedule for schedule in filtered_schedules if schedule.start_date >= current_date]
    return render(request, 'HomeApp/home_customer.html', {
        'schedules': all_shedules,
        'my_orders' : my_orders,
        'my_filter_form' : my_filter_form,
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
def handle_book_vehicle(request,schedule_id,customer_id,slot):
    try:
        schedule_id = schedule_id
        customer_id = customer_id
        slot = slot
        print("vehicle_id : ", schedule_id)
        print("customer_id : ", customer_id)
        schedule = Schedules.objects.get(pk=schedule_id)
        start_day = schedule.start_date
        customer =Customer.objects.get(pk=customer_id)
        vehicle =schedule.vehicle
        driver = vehicle.driver
        carowner = driver.carowner
        name_customer_order = customer.name_customer
        name_driver_order = driver.name_driver
     
        name_vehicle_order = vehicle.name_vehicle
        name_carowner_order = carowner.username
        carowner_id = carowner.id
        pickup_location= schedule.start_location
        dropoff_location = schedule.end_location
        start_time= schedule.start_time
        end_time=schedule.end_time
        name_schedule_order = schedule.name_schedule
        slot_vehicle = schedule.slot_vehicle
        slot_t = slot_vehicle - slot
        if slot_t >= 0:
            schedule.slot_vehicle = slot_t
            schedule.save()
            od = Orders(customer=customer,vehicle= vehicle,name_customer_order=name_customer_order, name_driver_order = name_driver_order,name_schedule_order = name_schedule_order , name_vehicle_order = name_vehicle_order , name_carowner_order = name_carowner_order , carowner_id = carowner_id , quantity_slot = slot , pickup_location = pickup_location , dropoff_location = dropoff_location , start_date_time = start_time , dropoff_datetime = end_time, day_schedule =start_day )
            od.save()
            return JsonResponse({'message': 'Đặt xe thành công'})

        else:
            return JsonResponse({'message': 'không đủ chỗ '})
    except Vehicle.DoesNotExist or Customer.DoesNotExist:
        return JsonResponse({'error': 'Có lỗi xảy ra vui lòng liên hệ với quản trị viên'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 
    

def search_customer(request):
    current_date = timezone.now().date()
    my_orders = Orders.objects.filter(customer = request.customer.id).all()
    schedules = Schedules.objects.select_related('vehicle__driver__carowner').all()
    my_filter_form = YourFilterForm()
    if request.method == 'GET':
        my_filter_form = YourFilterForm(request.GET)  # Khởi tạo form với dữ liệu GET
        if my_filter_form.is_valid():
            print("isvalid")
            search_query = my_filter_form.cleaned_data.get('search_query', '')
            # search_carowner = my_filter_form.cleaned_data.get('search_carowner')
            # search_slot = my_filter_form.cleaned_data.get('search_slot')
            # search_start_location = my_filter_form.cleaned_data.get('search_start_location')
            # search_end_location = my_filter_form.cleaned_data.get('search_end_location')
            # search_start_time = my_filter_form.cleaned_data.get('search_start_time')
            # search_name_driver = my_filter_form.cleaned_data.get('search_name_driver')
            # print("isvali: :" ,search_slot)
            # print("isvali: :" ,search_end_location)
            # print("isvali: :" ,search_name_driver)
            # query = Q()

            # # if search_carowner:
            # #     query |= Q(vehicle__driver__carowner__username=search_carowner)

            # if search_slot:
            #     query |= Q(slot_vehicle = search_slot)

            # if search_start_location:
            #     query |= Q(start_location=search_start_location)

            # if search_end_location:
            #     query |= Q(end_location=search_end_location)    

            # if search_name_driver:
            #     query |= Q(vehicle__driver__name_driver=search_name_driver)      

            # filtered_schedules = Schedules.objects.filter(query)     
            filtered_schedules = Schedules.objects.filter(
                Q(vehicle__driver__carowner__username__icontains=search_query) |
                Q(slot_vehicle__icontains=search_query) |
                Q(start_location__icontains=search_query) |
                Q(end_location__icontains=search_query) |
                Q(start_date__icontains=search_query)   |
                Q(start_time__icontains=search_query) 
            )
            all_shedules= [schedule for schedule in filtered_schedules if schedule.start_date >= current_date]          
          
            return render(request, 'HomeApp/home_customer.html', {'my_filter_form': my_filter_form, 'schedules': all_shedules,  'my_orders' : my_orders, })

        else:
             print("novalid")

    return render(request, 'HomeApp/home_customer.html', {'my_filter_form': my_filter_form, 'schedules': schedules,  'my_orders' : my_orders, })

      