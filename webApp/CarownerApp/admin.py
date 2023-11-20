from django.contrib import admin
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Max
from LoginApp.models import CarOwner,Customer
from django.contrib.auth.hashers import make_password
from .models import Driver, Vehicle,Schedules, Orders
from django import forms
from django.forms.widgets import HiddenInput
from datetime import timedelta
from django.db.models import F
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe
from django.contrib.admin import AdminSite
from django.urls import reverse_lazy
from django.urls import reverse
from django.utils.html import format_html
from datetime import datetime
from django.utils import timezone
from django.db.models import Q
import numpy as np
from django.conf import settings

def login_success(request):
    session_key = request.session[settings.CAROWNER_SESSION_COOKIE_NAM]
    print(session_key,"-----------------------------------------------")

# -------------Custom Admin site----------

# --------------------------------------------    
class DriverInline(admin.TabularInline):  
    model = Driver
    extra = 0
class VehicleInline(admin.TabularInline):  
    model = Vehicle
    extra = 0

 
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name_customer', 'email_customer', 'password_customer','address_customer','phone_customer','last_login','verify_customer')
    search_fields = ('name_customer','email_customer')
    def save_model(self, request, obj, form, change):
        if 'password_customer' in form.changed_data:
            obj.password_customer = make_password(obj.password_customer)
        super().save_model(request, obj, form, change)     

class CarOwnerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_carowner','address_carowner','verify_carowner')
    inlines = [DriverInline]
    actions = ['custom_logout']

    def custom_logout(self, request, queryset):
        if 'customer_sessionid' in request.session:
            print("isexists sessionid")
            del request.session['sessionid']
    custom_logout.short_description = "Custom Logout"
    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


class DriverAdminForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['state'].widget = forms.widgets.HiddenInput()
        self.fields['state'].required = False
        if not self.user.is_superuser:
            self.fields['carowner'].widget = forms.widgets.HiddenInput()
            self.fields['carowner'].required = False

    def save(self,commit=True):
        
        if not self.instance.carowner and not self.user.is_superuser:
            self.instance.carowner = self.user
        else:
            print('chưa add id ')    
        return super().save(commit)  
        
class DriverAdmin(admin.ModelAdmin):
    list_display = ('carowner','name_driver', 'email_driver', 'address_driver', 'phone_driver', 'verify_driver','state','comfirm_account')
    inlines = [VehicleInline]
    search_fields = ('name_driver','phone_driver','email_driver')
    form = DriverAdminForm
    class Media:
        css = {
            'all': ('CSS/custom_admin.css',),
        }
    
    def save_model(self, request, obj, form, change):
        if 'password_driver' in form.changed_data:
            obj.password_driver = make_password(obj.password_driver)
        super().save_model(request, obj, form, change)
    def get_queryset(self, request):
        request.session['user_id'] = request.user.id
        
        qs = super(DriverAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(carowner=request.user)
        return qs
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.user = request.user
        return form
# -----------------------------

class SchedulesInline(admin.TabularInline):
    model= Schedules
    extra =0 
class OrdersInline(admin.TabularInline):
    model = Orders
    extra = 0  
class VehicleAdminForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['name_driver'].widget = forms.widgets.HiddenInput()
        self.fields['name_driver'].required = False
        self.fields['email_driver'].widget = forms.widgets.HiddenInput()
        self.fields['email_driver'].required = False
        if  self.user and not self.instance.driver and not self.user.is_superuser :
            carowner = self.user
            self.fields['driver'].queryset = Driver.objects.filter(carowner=carowner)
        else:
            print("chưa thay đổi queryset của vehicle")  
    def save(self, commit=True):
        vehicle = super().save(commit=False)
        selected_driver = self.cleaned_data.get('driver')
        if selected_driver:
            driver_info = Driver.objects.get(pk=selected_driver.pk)
            vehicle.name_driver = driver_info.name_driver
            vehicle.email_driver = driver_info.email_driver
        if commit:
            vehicle.save()

        return vehicle             
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('driver', 'name_vehicle','name_driver','email_driver','img_vehicle','description','slot_vehicle','type_vehicle')
    # inlines =[SchedulesInline,OrdersInline]
    search_fields = ('name_vehicle','name_driver','slot_vehicle')
    class Media:
        css = {
            'all': ('CSS/custom_admin.css',),
        }
    form = VehicleAdminForm
    def get_queryset(self, request):
        qs = super(VehicleAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(driver__carowner=request.user)
        return qs 
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.user = request.user
        return form
    
class ScheduleAdminForm(forms.ModelForm):    
    class Meta:
        model = Schedules
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['slot_vehicle'].widget = forms.widgets.HiddenInput()
        self.fields['slot_vehicle'].required = False
        if  self.user and not self.instance.vehicle and not self.user.is_superuser:
            carowner = self.user
            self.fields['vehicle'].queryset = Vehicle.objects.filter(driver__carowner = carowner)
        else:
            print("chưa thay đổi queryset của vehicle")  
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('vehicle','label_schedule','name_schedule','slot_vehicle','start_location','end_location','start_time','end_time','start_date')
    form = ScheduleAdminForm
    search_fields = ('start_location','start_date')
    actions = ["filter_schedules_with_max_start_day"]
    class Media:
        css = {
            'all': ('CSS/custom_admin.css',),
        }

    def get_queryset(self, request):
        qs = super(ScheduleAdmin, self).get_queryset(request)
        print("qs :", qs)
        if not request.user.is_superuser:
            qs = qs.filter(vehicle__driver__carowner=request.user)
        return qs 
    
    def filter_schedules_with_max_start_day(self, request, queryset):
        carowner = request.user
        if carowner.is_superuser:
            max_start_dates = Schedules.objects.filter().values('name_schedule').annotate(max_start_date=Max('start_date'))
        else:
            max_start_dates = Schedules.objects.filter(vehicle__driver__carowner = carowner ).values('name_schedule').annotate(max_start_date=Max('start_date'))
        max_start_schedules1 = []
        max_start_schedules2 = []
        for item in max_start_dates:
            name_schedule = item['name_schedule']
            max_start_date = item['max_start_date']

            schedule1 = Schedules.objects.filter(name_schedule=name_schedule, start_date=max_start_date , label_schedule=1).first()
            schedule2 = Schedules.objects.filter(name_schedule=name_schedule, start_date=max_start_date , label_schedule=2).first()
            # print("list1 ",schedule1.id)
            # print("list2 ",schedule2.id)
            if schedule1:
                max_start_schedules1.append(schedule1)
            if schedule2:
                max_start_schedules2.append(schedule2)
        max_start_schedules = np.hstack((max_start_schedules1,max_start_schedules2)) 
        messages_list = []        
        for schedule in max_start_schedules:
            messages_item = f'<div class="info1">Name Schedule : {schedule.name_schedule} - Driver: {schedule.vehicle.name_driver}</div>   <div class="info2">Lịch trình số: {schedule.label_schedule} - Max start_day : {schedule.start_date}</div>'
            messages_list.append(mark_safe(messages_item))
            print(f"Vehicle ID: {schedule.vehicle.email_driver},lable : {schedule.label_schedule}, Max Start Day: {schedule.start_date}")
        for message in messages_list:
            messages.success(request, message)
    filter_schedules_with_max_start_day.short_description = _("Filter Schedules with Max Start Day")


    def save_model(self, request, obj, form, change):
        selected_vehicle = form.cleaned_data['vehicle']
        label_schedule = form.cleaned_data['label_schedule']
        number_of_days = form.cleaned_data['number_of_days']
        start_date = form.cleaned_data['start_date']
        name_schedule = form.cleaned_data['name_schedule']
        start_location = form.cleaned_data['start_location']
        end_location = form.cleaned_data['end_location']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        current_date = timezone.localtime(timezone.now()).date()
        current_time = timezone.localtime(timezone.now()).time()
        vehicle_info = Vehicle.objects.get(pk=selected_vehicle.pk)
        count_schedule = Schedules.objects.filter(
            Q(vehicle=vehicle_info) &
            (Q(start_date__gt=current_date) |
            (Q(start_date=current_date) & Q(start_time__gt=current_time)))
        ).count()
        print("số lịch trình hiện hành hiện tại......................",count_schedule)
        if (count_schedule + number_of_days) <= 12 and number_of_days <= 12:
            try:
                existing_schedule = Schedules.objects.get(id = obj.id)
                print("existing_schedule :",existing_schedule.id)
            except Schedules.DoesNotExist:
                for i in range(number_of_days):
                    new_schedule = Schedules(
                        vehicle=selected_vehicle,
                        label_schedule =label_schedule,
                        name_schedule=name_schedule,
                        slot_vehicle=vehicle_info.slot_vehicle,
                        start_location=start_location,
                        end_location=end_location,
                        start_time=start_time,
                        end_time=end_time,
                        day_schedule=start_date + timedelta(days=i),
                        start_date=start_date + timedelta(days=i),
                    )
                    new_schedule.save()
            else:
                if number_of_days == 0:  
                    existing_schedule.label_schedule = label_schedule    
                    existing_schedule.name_schedule = name_schedule
                    existing_schedule.slot_vehicle = vehicle_info.slot_vehicle
                    existing_schedule.start_location = start_location
                    existing_schedule.end_location = end_location
                    existing_schedule.start_time = start_time
                    existing_schedule.end_time = end_time
                    existing_schedule.save()
                elif number_of_days >=1 :  
                    for i in range(number_of_days):
                        new_schedule = Schedules(
                            vehicle=selected_vehicle,
                            label_schedule = label_schedule,
                            name_schedule=name_schedule,
                            slot_vehicle=vehicle_info.slot_vehicle,
                            start_location=start_location,
                            end_location=end_location,
                            start_time=start_time,
                            end_time=end_time,
                            day_schedule=start_date + timedelta(days=i),
                            start_date=start_date + timedelta(days=i),
                        )
                        new_schedule.save()
        else:
            nummax = 12 - count_schedule
            messages_list = []        
            messages_item = f'<div class="info1">Số ngày mà bạn muốn gia đã vượt quá giới hạn bạn chỉ có thể thêm : {nummax} Ngày </div>   <div class="info2"></div>'
            messages_list.append(mark_safe(messages_item))
            for message in messages_list:
                messages.success(request, message)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.user = request.user
        return form

    def sort_by_start_day_descending(self, request, queryset):
        print("start sort ")
        queryset = queryset.order_by('-start_day')
        
        self.message_user(request, f'Sorted by start_day descending')
        return queryset
    sort_by_start_day_descending.short_description = 'Sort by Start Day'
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('vehicle','name_customer_order','pickup_daytime','quantity_slot','name_driver_order','name_schedule_order','name_vehicle_order','name_carowner_order','pickup_location','dropoff_location','start_date_time','dropoff_datetime','state_book')
    search_fields = ('name_customer_order','name_driver_order','name_schedule_order','quantity_slot')
    class Media:
        css = {
            'all': ('CSS/custom_admin.css',),
        }
    def get_queryset(self, request):
        qs = super(OrdersAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(vehicle__driver__carowner=request.user)
        return qs  

admin.site.register(CarOwner, CarOwnerAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Schedules,ScheduleAdmin)
admin.site.register(Orders, OrdersAdmin)

