from telnetlib import LOGOUT
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from CarownerApp.models import Driver
from django.contrib.auth import login,logout
from django.contrib.auth.hashers import check_password
from LoginApp.backends.custom_auth import CustomerBackend
from CarownerApp.models import Driver,Orders,Schedules,Vehicle,CustomSession
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from HomeApp.forms import YourFilterForm
from django.db.models import Q
import numpy as np
import json
from django.http import JsonResponse


def driver(request):
    my_filter_form = YourFilterForm()
    if 'driver_sessionid' in request.session:
        # current_date = timezone.now().date()
        current_date = timezone.localtime(timezone.now()).date()
        current_time = timezone.localtime(timezone.now()).time()
        driver_id= request.driver.id
        state = Driver.objects.get(pk = driver_id).state
        driver_orders = Orders.objects.filter(vehicle__driver_id = driver_id)
        filtered_schedules = Schedules.objects.filter(vehicle__driver = driver_id).all()
        all_shedules= [schedule for schedule in filtered_schedules if schedule.start_date >= current_date]
        schedules_lb1 = [schedule for schedule in all_shedules if schedule.label_schedule == 1]
        schedules_lb2 = [schedule for schedule in all_shedules if schedule.label_schedule == 2]
        if schedules_lb2:
            soft_schedules =np.hstack((schedules_lb1,schedules_lb2))
        else:
            soft_schedules = schedules_lb1
        reversed_list = list(reversed(driver_orders))
        print(reversed_list)     
        context ={
            'driver_orders': reversed_list,
            'notifi_orders': reversed_list,
            'all_schedules' : list(soft_schedules),
            'my_filter_form' : my_filter_form,
            'driver_id' : driver_id,
            'state' : state,
        }
        return render(request, 'DriverApp/driver.html',context)
    else:
        return render(request, 'HomeApp/home.html')
def driver_login(request):
    return render(request, 'DriverApp/driver_login.html')

def handelLogin_driver(request):
   if request.method == 'POST':
        email_driver=request.POST['email']
        password=request.POST['password']
        try :
            user=Driver.objects.get(email_driver=email_driver)
            if check_password(password, user.password_driver):
                if user.verify_driver:
                    print("xác thực thành công")
                    user.backend = 'LoginApp.backends.custom_auth.CustomerBackend'
                    CustomerBackend.custom_login(request,user,'driver')
                    return redirect('driver')  
                else :
                    return render(request, 'DriverApp/driver_login.html',{
                        'islogin': 'noverifi',
                        })  
            else :
                return render(request, 'DriverApp/driver_login.html',{
                    'islogin': 'faildpass',
                   })  
        except Driver.DoesNotExist:
            return render(request, 'DriverApp/driver_login.html',{
                'islogin': 'faild',
 
            })        

def handle_verifi_driver(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        print("email_driver_get :", email)
        print("pass_driver_get :", password)
        token = get_random_string(32)
        try:
            dr=Driver.objects.get(email_driver=email)
        except Driver.DoesNotExist:
            return render(request, 'DriverApp/driver_login.html',{
                'islogin' : 'isNoneAccount'
            })    
        if dr.verify_driver == True:
            return render(request, 'DriverApp/driver_login.html',{
                'islogin' : 'verifi_isexists'
            })
        if check_password(password, dr.password_driver):
            dr.token_driver = token
            dr.save()
            user_id = dr.id
            user_name= dr.name_driver
            subject = 'Xác Thực Tài Khoản'
            from_email='furin.nvt@gmail.com'
            message=''
            contenHTML = render_to_string('LoginApp/verifyEmail.html', {
                'name_user':user_name,
                'activation_url': 'http://127.0.0.1:8000/activateD/{}/{}'.format(user_id,token),
            })
            to_email = [email]
            send_mail(subject,
                message,
                from_email,
                to_email,
                html_message=contenHTML,
            )
            return render(request, 'DriverApp/driver_login.html',{
                'islogin':'sendEmail'
            })
        else :
            return render(request, 'DriverApp/driver_login.html',{
            'islogin': 'faild',
        })
    return render(request, 'DriverApp/driver_login.html')

def activate_driver(request,uid,token):
    try:
        dr = Driver.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Driver().DoesNotExist):
        dr = None
    if dr is not None and dr.token_driver == token:
        dr.verify_driver = True
        dr.save()
        return render(request, 'DriverApp/driver_login.html',{
            'islogin':'verifisuccess'
        }) 
    else:
        raise Http404   
    

def search_list_schedules(request):
    current_date = timezone.localtime(timezone.now()).date()
    current_time = timezone.localtime(timezone.now()).time()
    driver_id= request.driver.id
    driver_orders = Orders.objects.filter(vehicle__driver_id = driver_id)
    filtered_schedules = Schedules.objects.filter(vehicle__driver = driver_id).all()
    my_filter_form = YourFilterForm()
    if request.method == 'GET':
        my_filter_form = YourFilterForm(request.GET)
        if my_filter_form.is_valid():
            print("isvalid")
            print("Search at Driver............................................")
            search_query = my_filter_form.cleaned_data.get('search_query', '')
            time_years = search_query.split('-')
            time_parts = search_query.split(':')
            time_with_vn = search_query.split(' ')
            print("Search_query: ", search_query)
            if search_query.isdigit():
                print("is integer")
                filter_search=filtered_schedules.filter(
                    Q(slot_vehicle= int(search_query)) 
                )
            elif len(time_parts) >=2 :
                print(time_parts)
                try:
                    hour = int(time_parts[0])
                    minute = int(time_parts[1])
                    filter_search = filtered_schedules.filter(
                        Q(start_time__hour =hour, start_time__minute =minute)
                    )
                except ValueError:
                    pass
            elif len(time_years) >=2 :
                print(time_years)
                try:
                    month = int(time_years[0])
                    day = int(time_years[1])
                    filter_search = filtered_schedules.filter(
                        Q(day_schedule__month = month, day_schedule__day = day)
                    )
                except ValueError:
                    pass
            elif len(time_with_vn) >= 2:
                if time_with_vn[0] == 'ngày' or time_with_vn[0] == 'Ngày':
                    print("search time vn:",time_with_vn)
                    try:
                        day = int(time_with_vn[1])
                        filter_search = filtered_schedules.filter(
                            Q(day_schedule__day = day)
                        )
                        if len(time_with_vn) >=3:
                            month = int(time_with_vn[2])
                            filter_search = filtered_schedules.filter(
                                Q( day_schedule__month= month, day_schedule__day = day)
                            )
                    except ValueError:
                        pass 
                elif time_with_vn[0] == 'tháng' or time_with_vn[0] == 'Tháng':
                    print("search time vn:",time_with_vn)
                    try:
                        month = int(time_with_vn[1])
                        filter_search = filtered_schedules.filter(
                            Q(day_schedule__month = month)
                        )
                        if len(time_with_vn) >=3:
                            day = int(time_with_vn[2])
                            filter_search = filtered_schedules.filter(
                                Q( day_schedule__month= month, day_schedule__day = day)
                            )
                    except ValueError:
                        
                        pass
                else:
                    filter_search = filtered_schedules.filter(
                        Q(name_schedule__icontains=search_query) |
                        Q(start_location__icontains = search_query) |
                        Q(end_location__icontains=search_query) |
                        Q(label_schedule__icontains=search_query) 
                    )
            else:
                filter_search = filtered_schedules.filter(
                        Q(name_schedule__icontains=search_query) |
                        Q(start_location__icontains = search_query) |
                        Q(end_location__icontains=search_query) |
                        Q(label_schedule__icontains=search_query) 
                )
            try:
                all_shedules= [schedule for schedule in filter_search if schedule.start_date >= current_date]
                searchvalue = ''
                if not filter_search :
                    searchvalue = 'search_err_schedules'
                else:
                    searchvalue = 'search_success_schedules'
                return render(request, 'DriverApp/driver.html', {
                    'driver_orders': driver_orders ,
                    'all_schedules' : list(all_shedules),
                    'my_filter_form' : my_filter_form,
                    'notifi_search' : searchvalue,
                })
            except:
                return render(request, 'DriverApp/driver.html', {
                    'driver_orders':driver_orders,
                    'all_schedules' : list(all_shedules),
                    'my_filter_form' : my_filter_form,
                    'notifi_search' : 'search_err_schedules'
                })
        else:
             print("novalid")

    return render(request, 'DriverApp/driver.html', {'my_filter_form': my_filter_form, 'driver_orders': driver_orders, 'all_schedules' : list(all_shedules), 'notifi_search' : 'search_err_schedules' })


def search_order(request):
    current_date = timezone.localtime(timezone.now()).date()
    current_time = timezone.localtime(timezone.now()).time()
    driver_id= request.driver.id
    driver_orders = Orders.objects.filter(vehicle__driver_id = driver_id)
    filtered_schedules = Schedules.objects.filter(vehicle__driver = driver_id).all()
    all_shedules= [schedule for schedule in filtered_schedules if schedule.start_date >= current_date]
    schedules_lb1 = [schedule for schedule in all_shedules if schedule.label_schedule == 1]
    schedules_lb2 = [schedule for schedule in all_shedules if schedule.label_schedule == 2]
    if schedules_lb2:
        soft_schedules =np.hstack((schedules_lb1,schedules_lb2))
    else:
        soft_schedules = schedules_lb1
    reversed_list = list(reversed(driver_orders))
    print(reversed_list)     
    my_filter_form = YourFilterForm()
    if request.method == 'GET':
        my_filter_form = YourFilterForm(request.GET)
        if my_filter_form.is_valid():
            print("isvalid")
            print("Search at Driver............................................")
            search_query = my_filter_form.cleaned_data.get('search_query', '')
            time_years = search_query.split('-')
            time_parts = search_query.split(':')
            time_with_vn = search_query.split(' ')
            print("Search_query: ", search_query)
            if search_query.isdigit():
                print("is integer")
                filter_orders=driver_orders.filter(
                    Q(quantity_slot= int(search_query)) 
                )
            elif len(time_parts) >=2 :
                print(time_parts)
                try:
                    hour = int(time_parts[0])
                    minute = int(time_parts[1])
                    filter_orders = driver_orders.filter(
                        Q(start_date_time__hour =hour, start_date_time__minute =minute)
                    )
                except ValueError:
                    pass
            elif len(time_years) >=2 :
                print(time_years)
                try:
                    month = int(time_years[0])
                    day = int(time_years[1])
                    filter_orders = driver_orders.filter(
                        Q(day_schedule__month = month, day_schedule__day = day)
                    )
                except ValueError:
                    pass
            elif len(time_with_vn) >= 2:
                if time_with_vn[0] == 'ngày' or time_with_vn[0] == 'Ngày':
                    print("search time vn:",time_with_vn)
                    try:
                        day = int(time_with_vn[1])
                        filter_orders = driver_orders.filter(
                            Q(day_schedule__day = day)
                        )
                        if len(time_with_vn) >=3:
                            month = int(time_with_vn[2])
                            filter_orders = driver_orders.filter(
                                Q( day_schedule__month= month, day_schedule__day = day)
                            )
                    except ValueError:
                        pass 
                elif time_with_vn[0] == 'tháng' or time_with_vn[0] == 'Tháng':
                    print("search time vn:",time_with_vn)
                    try:
                        month = int(time_with_vn[1])
                        filter_orders = driver_orders.filter(
                            Q(day_schedule__month = month)
                        )
                        if len(time_with_vn) >=3:
                            day = int(time_with_vn[2])
                            filter_orders = driver_orders.filter(
                                Q( day_schedule__month= month, day_schedule__day = day)
                            )
                    except ValueError:
                        pass
                else:
                    filter_orders = driver_orders.filter(
                        Q(name_customer_order__icontains=search_query) |
                        Q(name_driver_order__icontains = search_query) |
                        Q(name_schedule_order__icontains=search_query) |
                        Q(name_vehicle_order__icontains=search_query) 
                    )
            else:
                filter_orders = driver_orders.filter(
                        Q(name_customer_order__icontains=search_query) |
                        Q(name_driver_order__icontains = search_query) |
                        Q(name_schedule_order__icontains=search_query) |
                        Q(name_vehicle_order__icontains=search_query) 
                )
            try:
                searchvalue = ''
                if not filter_orders :
                    searchvalue = 'search_err'
                else:
                    searchvalue = 'search_success'
                return render(request, 'DriverApp/driver.html', {
                    'driver_orders': filter_orders,
                    'notifi_orders': reversed_list,
                    'all_schedules' : soft_schedules,
                    'my_filter_form' : my_filter_form,
                    'notifi_search' : searchvalue,
                })
            except:
                return render(request, 'DriverApp/driver.html', {
                    'driver_orders': filter_orders,
                    'notifi_orders': reversed_list,
                    'all_schedules' : soft_schedules,
                    'my_filter_form' : my_filter_form,
                    'notifi_search' : 'search_err'
                })
        else:
             print("novalid")

    return render(request, 'DriverApp/driver.html', {
        'my_filter_form': my_filter_form,
        'notifi_orders': reversed_list,
        'driver_orders': driver_orders,
        'all_schedules' : list(all_shedules),
        'notifi_search' : 'search_err' })
             
def logout_driver(request):
    try:
        session_key = request.session[settings.DRIVER_SESSION_COOKIE_NAME] 
        if session_key:
            try:
                custom_session = CustomSession.objects.get(session_key=session_key)
                custom_session.delete()
                del request.session[settings.DRIVER_SESSION_COOKIE_NAME]
                print("delete_Session for driver......")
            except CustomSession.DoesNotExist:
                pass
    except:
        print(" Driver Logged out...............")   
        pass     
    return render(request, 'DriverApp/driver_login.html')

def change_state(request,driver_id,checkstate):
    print("start change state................................................")
    try:
        print("id driver at state driver :", driver_id)
        print("check state at state driver :", checkstate)
        driver = Driver.objects.get(pk = driver_id)
        if driver:
            if checkstate == 1:
                driver.state = 'Đang khởi hành'
                driver.save()
                return JsonResponse({'notifiCancel': 'Cancel order Successfull.......'})
            elif checkstate == 0 :
                driver.state = 'Đang dừng'
                driver.save()
                return JsonResponse({'notifiCancel': 'Cancel order Successfull.......'})
        else:
            return JsonResponse({'error_Cancel': 'Cancel order failed.......'})
    except Orders.DoesNotExist:
        return JsonResponse({'error': 'Có lỗi xảy ra vui lòng liên hệ với quản trị viên'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 