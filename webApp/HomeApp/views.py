import os
from django.http import HttpResponseRedirect
from django.shortcuts import render , redirect
from django.contrib.auth import logout
from CarownerApp.models import Driver,Schedules,Vehicle,Orders
from django.db.models import Prefetch

import shutil
from django.conf import settings

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

from LoginApp.models import Customer
from django.utils import timezone
from .forms import YourFilterForm
from .forms import ImageUploadForm
from django.db.models import Q
from datetime import datetime
from CarownerApp.models import CustomSession
from django.contrib.sessions.models import Session
def homeview(request):
    my_filter_form = YourFilterForm()
    current_date = timezone.localtime(timezone.now()).date()
    current_time = timezone.localtime(timezone.now()).time()
    filtered_schedules = Schedules.objects.select_related('vehicle__driver__carowner').all()
    all_shedules= [schedule for schedule in filtered_schedules if schedule.start_date > current_date or (schedule.start_date == current_date and schedule.start_time > current_time)]
    return render(request, 'HomeApp/home.html',{
        'schedules' :all_shedules,
        'my_filter_form' : my_filter_form,
    })
def home_customer_view(request):
    if 'customer_sessionid' in request.session:
        print("has session customer.....")
        customerid = request.customer.id
        # current_date = timezone.now().date()
        current_date = timezone.localtime(timezone.now()).date()
        current_time = timezone.localtime(timezone.now()).time()
        print("current_date:....................... ",current_date)
        my_filter_form = YourFilterForm()
        my_orders = Orders.objects.filter(customer = customerid).all()
        filtered_schedules = Schedules.objects.select_related('vehicle__driver__carowner').all()
        all_shedules= [schedule for schedule in filtered_schedules if schedule.start_date > current_date or (schedule.start_date == current_date and schedule.start_time > current_time)]

        print("current_time:....................... ",current_time)
        return render(request, 'HomeApp/home_customer.html', {
            'schedules': all_shedules,
            'my_orders' : my_orders,
            'my_filter_form' : my_filter_form,
            'current_date' : current_date,
        })
    else:
        return render(request, 'HomeApp/home.html')
    
    
def controller_redirect_register(request):
    return redirect('login')
def controller_redirect_regisCustomer(request):
    return redirect('loginCustomer_view')


def handle_logout(request):
    my_filter_form = YourFilterForm()
    current_date = timezone.localtime(timezone.now()).date()
    current_time = timezone.localtime(timezone.now()).time()
    filtered_schedules = Schedules.objects.select_related('vehicle__driver__carowner').all()
    all_shedules= [schedule for schedule in filtered_schedules if schedule.start_date > current_date or (schedule.start_date == current_date and schedule.start_time > current_time)]
    try:
        session_key = request.session.get(settings.CUSTOMER_SESSION_COOKIE_NAME)
        if session_key:
            try:
                custom_session = CustomSession.objects.get(session_key=session_key)
                custom_session.delete()
                del request.session[settings.CUSTOMER_SESSION_COOKIE_NAME]
                print("delete_Session for customer......")
            except CustomSession.DoesNotExist:
                pass
    except:
        print("customer is logout...................")
        pass        
    return render(request, 'HomeApp/home.html',{
        'schedules' :all_shedules,
        'my_filter_form' : my_filter_form,
    })

def custom_logout(request):
    # session_key_to_delete = request.session.session_key
    # Session.objects.filter(session_key=session_key_to_delete).delete() 
    # if 'customer_sessionid' in request.session:
    #     print("tồn tại customer")
    #     request.session[settings.CUSTOMER_SESSION_COOKIE_NAME] = {
    #             'id_customer': request.customer.id,
    #     }
    # if 'driver_sessionid' in request.session:
    #     print("tồn tại driver")
    #     request.session[settings.DRIVER_SESSION_COOKIE_NAME] = {
    #             'id_driver': request.driver.id,
    #     } 
    return render(request, 'HomeApp/home.html')

def driver_login_view(request):
    return render(request,'DriverApp/driver_login.html')


def view_profile_customer(request):
    
    id_customer = request.customer.id
    my_filter_form = ImageUploadForm()
    img_customer = request.customer.img_customer
    my_profile = Customer.objects.get(pk=id_customer)
    return render(request,'HomeApp/profile_customer.html',{
        'myinfo': my_profile,
        'customer_id' : id_customer,
        'form_upload' : my_filter_form,
        'img_customer' : img_customer
    })

def view_editprofile(request):
    id_customer = request.customer.id
    my_filter_form = ImageUploadForm()
    my_profile = Customer.objects.get(pk=id_customer)
    img_customer = request.customer.img_customer
    print("img_customer....................: ", img_customer)
    return render(request,'HomeApp/edit_profile.html',{
        'myinfo': my_profile,
        'customer_id' : id_customer,
        'form_upload' : my_filter_form,
        'img_customer' : img_customer,
    })

def checkBeforeBook(request,schedule_id,customer_id,slots):
    try:
        current_datetime = datetime.now()
        schedule_id = schedule_id
        customer_id = customer_id
        print("vehicle_id : ", schedule_id)
        print("customer_id_book3 : ", customer_id)
        schedule = Schedules.objects.get(pk=schedule_id)
        check_cm = Orders.objects.filter(customer=customer_id,schedule=schedule)
        name_schedule_order = schedule.name_schedule
        start_time = schedule.start_time
        day_schedule = schedule.day_schedule
        if check_cm :
            slot = Orders.objects.get(customer=customer_id,schedule=schedule).quantity_slot
            print(" Quantiti slots: ", slot)
            print(" tồn tại người dùng ở lịch trình này ..............")
            return JsonResponse({'message': 'isexits','nameschedule' :name_schedule_order,'slots': slot,'start_time': start_time ,'day_schedule':day_schedule,'newslots': slots})
        else:
            print(" không tồn tại người dùng ở lịch trình này ..............")
            return JsonResponse({'message': 'isnotexits'})    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 

def handle_book_vehicle_second(request,schedule_id,customer_id,slot):
    try:
        current_datetime = datetime.now()
        schedule_id = schedule_id
        customer_id = customer_id
        slot = slot
        print("vehicle_id : ", schedule_id)
        print("customer_id_book2 : ", customer_id)
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
        handel_slots = slot
        check_cm = Orders.objects.get(customer=customer_id,schedule=schedule)
        if check_cm :
            if slot > check_cm.quantity_slot:
                if slot_t >= 0:
                    schedule.slot_vehicle = slot_t
                    schedule.save()
                    check_cm.delete()
                    new_order_update = Orders(customer = customer,vehicle = vehicle,schedule=schedule,name_customer_order=name_customer_order, name_driver_order = name_driver_order,name_schedule_order = name_schedule_order , name_vehicle_order = name_vehicle_order , name_carowner_order = name_carowner_order , carowner_id = carowner_id , quantity_slot = slot , pickup_location = pickup_location , dropoff_location = dropoff_location , start_date_time = start_time , dropoff_datetime = end_time, day_schedule =start_day, pickup_daytime = current_datetime ,state_book = 'Đã chỉnh sửa đơn')
                    new_order_update.save()
                    return JsonResponse({'message': 'Đặt xe thành công'})

                else:
                    return JsonResponse({'error': 'không đủ chỗ '})
            elif slot < check_cm.quantity_slot:
                schedule.slot_vehicle = schedule.slot_vehicle + check_cm.quantity_slot
                check_cm.delete()
                new_order_update = Orders(customer = customer,vehicle = vehicle,schedule=schedule,name_customer_order=name_customer_order, name_driver_order = name_driver_order,name_schedule_order = name_schedule_order , name_vehicle_order = name_vehicle_order , name_carowner_order = name_carowner_order , carowner_id = carowner_id , quantity_slot = slot , pickup_location = pickup_location , dropoff_location = dropoff_location , start_date_time = start_time , dropoff_datetime = end_time, day_schedule =start_day, pickup_daytime = current_datetime ,state_book = 'Đã chỉnh sửa đơn')
                schedule.save()
                new_order_update.save()
                return JsonResponse({'message': 'Đặt xe thành công'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 


def handle_book_vehicle(request,schedule_id,customer_id,slot):
    try:
        current_datetime = datetime.now()
        schedule_id = schedule_id
        customer_id = customer_id
        slot = slot
        print("vehicle_id : ", schedule_id)
        print("customer_id_book1 : ", customer_id)
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
            od = Orders(customer=customer,vehicle= vehicle,schedule=schedule,name_customer_order=name_customer_order, name_driver_order = name_driver_order,name_schedule_order = name_schedule_order , name_vehicle_order = name_vehicle_order , name_carowner_order = name_carowner_order , carowner_id = carowner_id , quantity_slot = slot , pickup_location = pickup_location , dropoff_location = dropoff_location , start_date_time = start_time , dropoff_datetime = end_time, day_schedule =start_day, pickup_daytime =current_datetime,state_book = '')
            od.save()
            return JsonResponse({'message': 'Đặt xe thành công'})

        else:
            return JsonResponse({'error': 'không đủ chỗ '})
    except Vehicle.DoesNotExist or Customer.DoesNotExist:
        return JsonResponse({'error': 'Có lỗi xảy ra vui lòng liên hệ với quản trị viên'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 

def handle_cancel_order(request,idorder):
    print("start handle cancel order................................................")
    try:
        print("id order :", idorder)
        order = Orders.objects.get(pk=idorder)
        print("")
        schedule = order.schedule
        if schedule:
            slots_order = order.quantity_slot
            slots_schedule = schedule.slot_vehicle
            total_slot = slots_schedule + slots_order
            order.delete()
            schedule.slot_vehicle = total_slot
            schedule.save()
            return JsonResponse({'notifiCancel': 'Cancel order Successfull.......'})
        else:
            return JsonResponse({'error_Cancel': 'Cancel order failed.......'})
    except Orders.DoesNotExist:
        return JsonResponse({'error': 'Có lỗi xảy ra vui lòng liên hệ với quản trị viên'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 

def search_datetime_and_word(request):
    
    current_date = timezone.localtime(timezone.now()).date()
    current_time = timezone.localtime(timezone.now()).time()

    id_customer = request.customer.id

    my_orders = Orders.objects.filter(customer = id_customer).all()
    filtered_schedules_return = Schedules.objects.select_related('vehicle__driver__carowner').all()
    all_shedules_return= [schedule for schedule in filtered_schedules_return if schedule.start_date > current_date or (schedule.start_date == current_date and schedule.start_time > current_time)]
    if request.method == 'GET':
        
        search_query_time_inputdate = request.GET['input_date']
        search_query_hours = request.GET['hours']
        search_query_minutes = request.GET['minutes']
        search_query_search_text = request.GET['search_text']
            
        if  search_query_time_inputdate and search_query_hours and search_query_search_text:
            print("check_search_datetime_and_word.....Cả 3 thông tin ")
            time_years = search_query_time_inputdate.split('-')
            if len(time_years) >=2:
                print(time_years)
            try:
                hour = int(search_query_hours)
                month = int(time_years[1])
                day = int(time_years[2])
                if search_query_minutes:
                    minute = int(search_query_minutes)
                    filtered_schedules = Schedules.objects.filter(
                        Q(vehicle__driver__carowner__username__icontains=search_query_search_text ,start_date__month = month, start_date__day = day ,start_time__hour =hour, start_time__minute =minute) |
                        Q(vehicle__driver__name_driver__icontains = search_query_search_text ,start_date__month = month, start_date__day = day ,start_time__hour =hour, start_time__minute =minute) |
                        Q(start_location__icontains=search_query_search_text ,start_date__month = month, start_date__day = day ,start_time__hour =hour, start_time__minute =minute) |
                        Q(end_location__icontains=search_query_search_text ,start_date__month = month, start_date__day = day ,start_time__hour =hour, start_time__minute =minute) |
                        Q(vehicle__type_vehicle__icontains=search_query_search_text ,start_date__month = month, start_date__day = day ,start_time__hour =hour, start_time__minute =minute)
                    )
                else:
                    minute = 00
                    filtered_schedules = Schedules.objects.filter(
                        Q(vehicle__driver__carowner__username__icontains=search_query_search_text ,start_date__month = month, start_date__day = day ,start_time__hour =hour, start_time__minute =minute) |
                        Q(vehicle__driver__name_driver__icontains = search_query_search_text ,start_date__month = month, start_date__day = day ,start_time__hour =hour, start_time__minute =minute) |
                        Q(start_location__icontains=search_query_search_text ,start_date__month = month, start_date__day = day ,start_time__hour =hour, start_time__minute =minute) |
                        Q(end_location__icontains=search_query_search_text ,start_date__month = month, start_date__day = day ,start_time__hour =hour, start_time__minute =minute) |
                        Q(vehicle__type_vehicle__icontains=search_query_search_text ,start_date__month = month, start_date__day = day ,start_time__hour =hour, start_time__minute =minute)
                    )    
            except ValueError:
                pass
        elif  search_query_hours and search_query_search_text:
                print("check_search_datetime_and_word.....search_query_hours and search_query_search_text")
                try:
                    hour = int(search_query_hours)
                    if search_query_minutes:
                        minute = int(search_query_minutes)
                        filtered_schedules = Schedules.objects.filter(
                            Q(vehicle__driver__carowner__username__icontains=search_query_search_text ,start_time__hour =hour, start_time__minute =minute) |
                            Q(vehicle__driver__name_driver__icontains = search_query_search_text ,start_time__hour =hour, start_time__minute =minute) |
                            Q(start_location__icontains=search_query_search_text ,start_time__hour =hour, start_time__minute =minute) |
                            Q(end_location__icontains=search_query_search_text ,start_time__hour =hour, start_time__minute =minute) |
                            Q(vehicle__type_vehicle__icontains=search_query_search_text ,start_time__hour =hour, start_time__minute =minute)
                        )
                    else:
                        minute = 00
                        filtered_schedules = Schedules.objects.filter(
                            Q(vehicle__driver__carowner__username__icontains=search_query_search_text ,start_time__hour =hour, start_time__minute =minute) |
                            Q(vehicle__driver__name_driver__icontains = search_query_search_text ,start_time__hour =hour, start_time__minute =minute) |
                            Q(start_location__icontains=search_query_search_text ,start_time__hour =hour, start_time__minute =minute) |
                            Q(end_location__icontains=search_query_search_text ,start_time__hour =hour, start_time__minute =minute) |
                            Q(vehicle__type_vehicle__icontains=search_query_search_text ,start_time__hour =hour, start_time__minute =minute)
                        )    
                except ValueError:
                    pass   
        elif  search_query_time_inputdate and search_query_search_text:
            print("check_search_datetime_and_word.....search_query_time_inputdate and search_query_search_text")
            time_years = search_query_time_inputdate.split('-')
            if len(time_years) >=2:
                print(time_years)
            try:
                month = int(time_years[1])
                day = int(time_years[2])
                filtered_schedules = Schedules.objects.filter(
                    Q(vehicle__driver__carowner__username__icontains=search_query_search_text ,start_date__month = month, start_date__day = day) |
                    Q(vehicle__driver__name_driver__icontains = search_query_search_text ,start_date__month = month, start_date__day = day) |
                    Q(start_location__icontains=search_query_search_text ,start_date__month = month, start_date__day = day) |
                    Q(end_location__icontains=search_query_search_text ,start_date__month = month, start_date__day = day) |
                    Q(vehicle__type_vehicle__icontains=search_query_search_text ,start_date__month = month, start_date__day = day)
                )
            
            except ValueError:
                pass 

        elif  search_query_time_inputdate and search_query_hours:
            print("check_search_datetime_and_word.....search_query_time_inputdate and search_query_hours: ")
            time_years = search_query_time_inputdate.split('-')
            if len(time_years) >=2:
                print(time_years)
            try:
                hour = int(search_query_hours)
                month = int(time_years[1])
                day = int(time_years[2])
                if search_query_minutes:
                    minute = int(search_query_minutes)
                    filtered_schedules = Schedules.objects.filter(
                        Q(start_date__month = month, start_date__day = day ,start_time__hour =hour, start_time__minute =minute)
                    )
                else:
                    minute = 00
                    filtered_schedules = Schedules.objects.filter(
                        Q(start_date__month = month, start_date__day = day ,start_time__hour =hour, start_time__minute =minute)
                    )    
            except ValueError:
                pass
        elif search_query_time_inputdate:
            print("check_search_datetime_and_word.....search_query_time_inputdate")
            time_years = search_query_time_inputdate.split('-')
            if len(time_years) >=2:
                print(time_years)
            try:
                month = int(time_years[1])
                day = int(time_years[2])
                filtered_schedules = Schedules.objects.filter(
                    Q(start_date__month = month, start_date__day = day)
                )
            except ValueError:
                pass
            print("check_search_datetime_and_word......",search_query_time_inputdate,search_query_hours,search_query_minutes)
        elif  search_query_hours:
            print("check_search_datetime_and_word.....search_query_hours")
            try:
                hour = int(search_query_hours)
                if search_query_minutes:
                    minute = int(search_query_minutes)
                    filtered_schedules = Schedules.objects.filter(
                    Q(start_time__hour =hour, start_time__minute =minute)
                )
                else:
                    minute = 00
                    filtered_schedules = Schedules.objects.filter(
                        Q(start_time__hour =hour, start_time__minute =minute)
                    )
            except ValueError:
                    pass
        elif  search_query_search_text:
            print("check_search_datetime_and_word.....search_query_search_text")
            filtered_schedules = Schedules.objects.filter(
                Q(vehicle__driver__carowner__username__icontains=search_query_search_text) |
                Q(vehicle__driver__name_driver__icontains = search_query_search_text) |
                Q(start_location__icontains=search_query_search_text) |
                Q(end_location__icontains=search_query_search_text) |
                Q(vehicle__type_vehicle__icontains=search_query_search_text)
            )                                
        try:
            searchvalue = ''
            all_shedules= [schedule for schedule in filtered_schedules if schedule.start_date > current_date or (schedule.start_date == current_date and schedule.start_time > current_time)] 
            if not all_shedules :
                searchvalue = 'search_err'
            else:
                searchvalue = 'search_success'
            return render(request, 'HomeApp/home.html', {
                    'schedules': all_shedules,
                    'my_orders' : my_orders,
                    'current_date' : current_date,
                    'notifi_search' : searchvalue
                })
        except:
                return render(request, 'HomeApp/home.html', {
                    'schedules': '',
                    'my_orders' : my_orders,
                    'current_date' : current_date,
                    'notifi_search' : 'search_err'
                })    


    return render(request, 'HomeApp/home.html', {'schedules': all_shedules_return,  'my_orders' : my_orders, 'notifi_search' : 'search_err' })


def search_customer(request):

    current_date = timezone.localtime(timezone.now()).date()
    current_time = timezone.localtime(timezone.now()).time()

    id_customer = request.customer.id

    my_orders = Orders.objects.filter(customer = id_customer).all()
    filtered_schedules_return = Schedules.objects.select_related('vehicle__driver__carowner').all()
    all_shedules_return= [schedule for schedule in filtered_schedules_return if schedule.start_date > current_date or (schedule.start_date == current_date and schedule.start_time > current_time)]
    my_filter_form = YourFilterForm()
    if request.method == 'GET':
        my_filter_form = YourFilterForm(request.GET)
        if my_filter_form.is_valid():
            print("isvalid")
            search_query = my_filter_form.cleaned_data.get('search_query', '')
            time_years = search_query.split('-')
            time_parts = search_query.split(':')
            time_with_vn = search_query.split(' ')
            if search_query.isdigit():
                print("is integer")
                filtered_schedules = Schedules.objects.filter(
                    Q(slot_vehicle= int(search_query)) # Tìm kiếm theo năm
                )       
            elif len(time_parts) >=2 :
                print(time_parts)
                try:
                    hour = int(time_parts[0])
                    minute = int(time_parts[1])
                    filtered_schedules = Schedules.objects.filter(
                        Q(start_time__hour =hour, start_time__minute =minute)
                    )
                except ValueError:
                    pass
            elif len(time_years) >=2 :
                print(time_years)
                try:
                    month = int(time_years[0])
                    day = int(time_years[1])
                    filtered_schedules = Schedules.objects.filter(
                        Q(start_date__month = month, start_date__day = day)
                    )
                except ValueError:
                    pass
            elif len(time_with_vn) >= 2:
                if time_with_vn[0] == 'ngày' or time_with_vn[0] == 'Ngày':
                    print("search time vn:",time_with_vn)
                    try:
                        day = int(time_with_vn[1])
                        filtered_schedules = Schedules.objects.filter(
                            Q(start_date__day = day)
                        )
                        if len(time_with_vn) >=3:
                            month = int(time_with_vn[2])
                            filtered_schedules = Schedules.objects.filter(
                                Q( start_date__month= month,start_date__day = day)
                            )
                    except ValueError:
                        pass 
                elif time_with_vn[0] == 'tháng' or time_with_vn[0] == 'Tháng':
                    print("search time vn:",time_with_vn)
                    try:
                        month = int(time_with_vn[1])
                        filtered_schedules = Schedules.objects.filter(
                            Q(start_date__month = month)
                        )
                        if len(time_with_vn) >=3:
                            day = int(time_with_vn[2])
                            filtered_schedules = Schedules.objects.filter(
                                Q( start_date__month= month, start_date__day = day)
                            )
                    except ValueError:
                        pass
                else:
                    filtered_schedules = Schedules.objects.filter(
                        Q(vehicle__driver__carowner__username__icontains=search_query) |
                        Q(vehicle__driver__name_driver__icontains = search_query) |
                        Q(start_location__icontains=search_query) |
                        Q(end_location__icontains=search_query) |
                        Q(vehicle__type_vehicle__icontains=search_query)
                    )
            else:
                filtered_schedules = Schedules.objects.filter(
                    Q(vehicle__driver__carowner__username__icontains=search_query) |
                    Q(start_location__icontains=search_query) |
                    Q(end_location__icontains=search_query) |
                    Q(vehicle__type_vehicle__icontains=search_query)
                )
            try:
                searchvalue = ''
                all_shedules= [schedule for schedule in filtered_schedules if schedule.start_date > current_date or (schedule.start_date == current_date and schedule.start_time > current_time)] 
                if not all_shedules :
                    searchvalue = 'search_err'
                else:
                    searchvalue = 'search_success'
                return render(request, 'HomeApp/home_customer.html', {
                    'my_filter_form': my_filter_form,
                    'schedules': all_shedules,
                    'my_orders' : my_orders,
                    'current_date' : current_date,
                    'notifi_search' : searchvalue
                })
            except:
                return render(request, 'HomeApp/home_customer.html', {
                    'my_filter_form': my_filter_form,
                    'schedules': '',
                    'my_orders' : my_orders,
                    'current_date' : current_date,
                    'notifi_search' : 'search_err'
                })
        else:
             print("novalid")

    return render(request, 'HomeApp/home_customer.html', {'my_filter_form': my_filter_form, 'schedules': all_shedules_return,  'my_orders' : my_orders, 'notifi_search' : 'search_err' })

def search_home(request):

    current_date = timezone.localtime(timezone.now()).date()
    current_time = timezone.localtime(timezone.now()).time()
    filtered_schedules_return = Schedules.objects.select_related('vehicle__driver__carowner').all()
    all_shedules_return= [schedule for schedule in filtered_schedules_return if schedule.start_date > current_date or (schedule.start_date == current_date and schedule.start_time > current_time)]
    my_filter_form = YourFilterForm()
    if request.method == 'GET':
        my_filter_form = YourFilterForm(request.GET)
        if my_filter_form.is_valid():
            print("isvalid")
            search_query = my_filter_form.cleaned_data.get('search_query', '')
            time_years = search_query.split('-')
            time_parts = search_query.split(':')
            time_with_vn = search_query.split(' ')
            if search_query.isdigit():
                print("is integer")
                filtered_schedules = Schedules.objects.filter(
                    Q(slot_vehicle= int(search_query)) # Tìm kiếm theo năm
                )       
            elif len(time_parts) >=2 :
                print(time_parts)
                try:
                    hour = int(time_parts[0])
                    minute = int(time_parts[1])
                    filtered_schedules = Schedules.objects.filter(
                        Q(start_time__hour =hour, start_time__minute =minute)
                    )
                except ValueError:
                    pass
            elif len(time_years) >=2 :
                print(time_years)
                try:
                    month = int(time_years[0])
                    day = int(time_years[1])
                    filtered_schedules = Schedules.objects.filter(
                        Q(start_date__month = month, start_date__day = day)
                    )
                except ValueError:
                    pass
            elif len(time_with_vn) >= 2:
                if time_with_vn[0] == 'ngày' or time_with_vn[0] == 'Ngày':
                    print("search time vn:",time_with_vn)
                    try:
                        day = int(time_with_vn[1])
                        filtered_schedules = Schedules.objects.filter(
                            Q(start_date__day = day)
                        )
                        if len(time_with_vn) >=3:
                            month = int(time_with_vn[2])
                            filtered_schedules = Schedules.objects.filter(
                                Q( start_date__month= month,start_date__day = day)
                            )
                    except ValueError:
                        pass 
                elif time_with_vn[0] == 'tháng' or time_with_vn[0] == 'Tháng':
                    print("search time vn:",time_with_vn)
                    try:
                        month = int(time_with_vn[1])
                        filtered_schedules = Schedules.objects.filter(
                            Q(start_date__month = month)
                        )
                        if len(time_with_vn) >=3:
                            day = int(time_with_vn[2])
                            filtered_schedules = Schedules.objects.filter(
                                Q( start_date__month= month, start_date__day = day)
                            )
                    except ValueError:
                        pass
                else:
                    filtered_schedules = Schedules.objects.filter(
                        Q(vehicle__driver__carowner__username__icontains=search_query) |
                        Q(vehicle__driver__name_driver__icontains = search_query) |
                        Q(start_location__icontains=search_query) |
                        Q(end_location__icontains=search_query) |
                        Q(vehicle__type_vehicle__icontains=search_query)
                    )
            else:
                filtered_schedules = Schedules.objects.filter(
                Q(vehicle__driver__carowner__username__icontains=search_query) |
                Q(start_location__icontains=search_query) |
                Q(end_location__icontains=search_query) |
                Q(vehicle__type_vehicle__icontains=search_query)
            )
            try:
                searchvalue = ''
                all_shedules= [schedule for schedule in filtered_schedules if schedule.start_date > current_date or (schedule.start_date == current_date and schedule.start_time > current_time)] 
                if not all_shedules :
                    searchvalue = 'search_err'
                else:
                    searchvalue = 'search_success'
                return render(request, 'HomeApp/home.html', {
                    'my_filter_form': my_filter_form,
                    'schedules': all_shedules,
                    'current_date' : current_date,
                    'notifi_search' : searchvalue
                })
            except:
                return render(request, 'HomeApp/home.html', {
                    'my_filter_form': my_filter_form,
                    'schedules': '',
                    'current_date' : current_date,
                    'notifi_search' : 'search_err'
                })
        else:
             print("novalid")

    return render(request, 'HomeApp/home.html', {'my_filter_form': my_filter_form, 'schedules': all_shedules_return,'notifi_search' : 'search_err' })

def upload_images(request,customerid):
    my_filter_form = ImageUploadForm()
    img_customer = request.customer.img_customer

    id_customer = request.customer.id
    my_profile = Customer.objects.get(pk=id_customer)
    if request.method == 'POST':
        print(request.POST)  
        print(request.FILES) 
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.cleaned_data['image_upload']
            print("check img :",uploaded_image)
            c = Customer.objects.get(pk=customerid)
            c.img_customer = uploaded_image
            c.save()
            return render(request,'HomeApp/edit_profile.html',{
                'myinfo': my_profile,
                'customer_id' : id_customer,
                'form_upload' : my_filter_form,
                'img_customer' : img_customer,
            })
        else:
            print(form.errors)
            return JsonResponse({'error': 'không đủ chỗ '})
    else:
        form = ImageUploadForm()
    return render(request, 'HomeApp/edit_profile.html', {'form_upload': form, 'myinfo' : my_profile})
def save_edit_info(request):
    id_customer = request.customer.id
    my_profile = Customer.objects.get(pk=id_customer)
    form = ImageUploadForm()
    if request.method =='POST' :
        try:
            data = json.loads(request.body) 
            # Xử lý dữ liệu ở đây
            received_name = data.get('name')
            received_email = data.get('email')
            received_phone = data.get('phone')
            received_address = data.get('address')
            c = Customer.objects.get(pk=id_customer)
            c.name_customer = received_name
            c.address_customer = received_address
            c.phone_customer = received_phone
            c.save()
            return JsonResponse({'message': 'Dữ liệu đã được lưu thành công'})
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer dost not exits'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Lỗi trong quá trình phân tích chuỗi JSON'}, status=400)
    return render(request, 'HomeApp/edit_profile.html', {'form_upload': form, 'myinfo' : my_profile})      