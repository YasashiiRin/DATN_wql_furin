from django.contrib import admin
from django.shortcuts import redirect, render
from LoginApp.models import CarOwner,Customer
from django.contrib.auth.hashers import make_password
from .models import Driver, Vehicle,Schedules, Orders
from django import forms
from django.forms.widgets import HiddenInput
from datetime import timedelta



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
    def save_model(self, request, obj, form, change):
        if 'password_customer' in form.changed_data:
            obj.password_customer = make_password(obj.password_customer)
        super().save_model(request, obj, form, change)     
class CarOwnerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_carowner','address_carowner')
    inlines = [DriverInline]
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
    list_display = ('carowner','name_driver', 'email_driver', 'password_driver', 'address_driver', 'phone_driver', 'verify_driver','token_driver','comfirm_account')
    inlines = [VehicleInline]
    form = DriverAdminForm
    def save_model(self, request, obj, form, change):
        if 'password_driver' in form.changed_data:
            obj.password_driver = make_password(obj.password_driver)
        super().save_model(request, obj, form, change)
    def get_queryset(self, request):
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
        if  self.user and not self.instance.driver:
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
        if  self.user and not self.instance.vehicle:
            carowner = self.user
            self.fields['vehicle'].queryset = Vehicle.objects.filter(driver__carowner = carowner)
        else:
            print("chưa thay đổi queryset của vehicle")  
    # def save(self, commit=True):
    #     selected_vehicle = self.cleaned_data.get('vehicle')
    #     name_schedule = self.cleaned_data.get('name_schedule')
    #     start_location = self.cleaned_data.get('start_location')
    #     end_location = self.cleaned_data.get('end_location')
    #     start_time = self.cleaned_data.get('start_time')
    #     end_time = self.cleaned_data.get('end_time')
    #     number_of_days = self.cleaned_data.get('number_of_days')
    #     start_date = self.cleaned_data.get('start_date')
    #     print("start_day :", start_date)
    #     print("number_of_day :" , number_of_days)
    #     schedules = []
    #     if selected_vehicle:
    #         vehicle_info = Vehicle.objects.get(pk=selected_vehicle.pk)
    #         print("slot :", vehicle_info.slot_vehicle)
    #         for i in range(number_of_days):
    #             new_schedule = Schedules(
    #                 vehicle = selected_vehicle,
    #                 name_schedule = name_schedule,
    #                 slot_vehicle=vehicle_info.slot_vehicle,
    #                 start_location = start_location,
    #                 end_location = end_location,
    #                 start_time = start_time,
    #                 end_time = end_time,
    #                 day_schedule = start_date + timedelta(days=i), 
    #                 start_date=start_date + timedelta(days=i),  
    #             )
    #             schedules.append(new_schedule)
    #         if commit:
    #             Schedules.objects.bulk_create(schedules)
    #     return super().save(commit=commit)
    
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('vehicle','name_schedule','slot_vehicle','start_location','end_location','start_time','end_time','day_schedule')
    form = ScheduleAdminForm
    def get_queryset(self, request):
        qs = super(ScheduleAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(vehicle__driver__carowner=request.user)
        return qs 
    def save_model(self, request, obj, form, change):
        selected_vehicle = form.cleaned_data['vehicle']
        number_of_days = form.cleaned_data['number_of_days']
        start_date = form.cleaned_data['start_date']
        selected_vehicle = form.cleaned_data['vehicle']
        name_schedule = form.cleaned_data['name_schedule']
        start_location = form.cleaned_data['start_location']
        end_location = form.cleaned_data['end_location']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        number_of_days = form.cleaned_data['number_of_days']
        start_date = form.cleaned_data['start_date']
        print("start_day :", start_date)
        print("number_of_day :" , number_of_days)
        vehicle_info = Vehicle.objects.get(pk=selected_vehicle.pk)
        for i in range(number_of_days):
            new_schedule = Schedules(
                vehicle = selected_vehicle,
                name_schedule = name_schedule,
                slot_vehicle=vehicle_info.slot_vehicle,
                start_location = start_location,
                end_location = end_location,
                start_time = start_time,
                end_time = end_time,
                day_schedule = start_date + timedelta(days=i), 
                start_date=start_date + timedelta(days=i),  
            )
            new_schedule.save()
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.user = request.user
        return form
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('vehicle','name_customer_order','name_driver_order','name_schedule_order','name_vehicle_order','name_carowner_order','quantity_slot','pickup_location','dropoff_location','start_date_time','dropoff_datetime','state_order')

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

