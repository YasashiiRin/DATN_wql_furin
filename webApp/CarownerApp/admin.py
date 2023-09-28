from django.contrib import admin
from django.shortcuts import redirect, render
from LoginApp.models import CarOwner,Customer
from django.contrib.auth.hashers import make_password
from .models import Driver, Vehicle,Schedules, Orders
from django import forms
from django.forms.widgets import HiddenInput



# -------------Custom Admin site----------
# --------------------------------------------    
class DriverInline(admin.TabularInline):  
    model = Driver
    extra = 0
class VehicleInline(admin.TabularInline):  
    model = Vehicle
    extra = 0

class SchedulesInline(admin.TabularInline):
    model= Schedules
    extra =0 
class OrdersInline(admin.TabularInline):
    model = Orders
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
    inlines =[SchedulesInline,OrdersInline]
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
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('vehicle','name_schedule','start_location','end_location','start_date_time','end_date_time')

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('vehicle','name_customer_order','name_driver_order','name_schedule_order','name_vehicle_order','name_carowner_order','quantity_slot','pickup_location','dropoff_location','pickup_datetime','dropoff_datetime','state_order')


admin.site.register(CarOwner, CarOwnerAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Schedules,ScheduleAdmin)
admin.site.register(Orders, OrdersAdmin)

