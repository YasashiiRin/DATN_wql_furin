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
    
    return render(request, 'HomeApp/home.html')
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
    return render(request, 'HomeApp/home.html')

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
def handle_book_vehicle(request,schedule_id,customer_id,slot):
    try:
        current_datetime = datetime.now()
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
            od = Orders(customer=customer,vehicle= vehicle,schedule=schedule,name_customer_order=name_customer_order, name_driver_order = name_driver_order,name_schedule_order = name_schedule_order , name_vehicle_order = name_vehicle_order , name_carowner_order = name_carowner_order , carowner_id = carowner_id , quantity_slot = slot , pickup_location = pickup_location , dropoff_location = dropoff_location , start_date_time = start_time , dropoff_datetime = end_time, day_schedule =start_day, pickup_daytime =current_datetime )
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
            time_years = search_query.split('-')
            time_parts = search_query.split(':')
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
            else:
                filtered_schedules = Schedules.objects.filter(
                Q(vehicle__driver__carowner__username__icontains=search_query) |
                Q(start_location__icontains=search_query) |
                Q(end_location__icontains=search_query) |
                Q(vehicle__type_vehicle__icontains=search_query)
            )
            all_shedules= [schedule for schedule in filtered_schedules if schedule.start_date > current_date or (schedule.start_date == current_date and schedule.start_time > current_time)]
            searchvalue = ''   
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

        else:
             print("novalid")

    return render(request, 'HomeApp/home_customer.html', {'my_filter_form': my_filter_form, 'schedules': all_shedules_return,  'my_orders' : my_orders, 'notifi_search' : 'search_err' })

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