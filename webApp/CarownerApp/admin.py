from django.contrib import admin
from django.shortcuts import redirect, render
from LoginApp.models import CarOwner
from django.contrib.auth.hashers import make_password
from .models import Driver, Vehicle,Schedules
from django.contrib.admin import AdminSite
# -------------Custom Admin site----------
class CustomAdminSite(AdminSite):
    site_header = 'Your Custom Admin Header'
    site_title = 'Your Custom Admin Title'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logout_template = 'admin/logout.html'  # Tùy chỉnh template logout nếu cần
    
    def logout(self, request, extra_context=None):
        # Sử dụng URL của view đăng xuất tùy chỉnh
        return redirect('LoginApp/login.html')

custom_admin_site = CustomAdminSite(name='customadmin')   
# --------------------------------------------    
class DriverInline(admin.TabularInline):  
    model = Driver
    extra = 0
    
class CarOwnerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_carowner','address_carowner')
    inlines = [DriverInline]
    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)
# ----------Driver-----------
class VehicleInline(admin.TabularInline):  
    model = Vehicle
    extra = 0
class DriverAdmin(admin.ModelAdmin):
    list_display = ('carowner','name_driver', 'email_driver', 'password_driver', 'address_driver', 'phone_driver', 'verify_driver','token_driver','comfirm_account')
    inlines = [VehicleInline]
    def save_model(self, request, obj, form, change):
        if 'password_driver' in form.changed_data:
            obj.password_driver = make_password(obj.password_driver)
        super().save_model(request, obj, form, change)
    def get_queryset(self, request):
        qs = super(DriverAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(carowner=request.user)
        return qs    
# -----------------------------
class SchedulesInline(admin.TabularInline):
    model= Schedules
    extra =0 
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('driver', 'name_vehicle','img_vehicle','description','slot_vehicle','type_vehicle')
    inlines =[SchedulesInline]
    def get_queryset(self, request):
        qs = super(VehicleAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(driver__carowner=request.user)
        return qs 
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'vehicle','name_schedule','start_location','end_location','start_date_time','end_date_time')



admin.site.register(CarOwner, CarOwnerAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Schedules,ScheduleAdmin)

