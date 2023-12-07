from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from LoginApp.models import CarOwner
from LoginApp.models import Customer
from django.db.models import JSONField

class Driver(models.Model):
    carowner =models.ForeignKey(CarOwner,on_delete=models.CASCADE,null=True)
    name_driver = models.CharField(max_length=100,null=True)
    email_driver = models.EmailField(max_length=255,null=True)
    password_driver = models.CharField(max_length=255,null=True)
    address_driver = models.CharField(max_length=100, null=True)
    phone_driver = models.IntegerField(null=True)
    verify_driver = models.BooleanField(default=False)
    token_driver = models.CharField(max_length=255, null=True, blank=True)
    comfirm_account=models.BooleanField(default=False)
    state = models.CharField(max_length=30, default='Đang dừng')
    def __str__(self):
        return self.email_driver
    class Meta:
        db_table = 'driver'
class Vehicle(models.Model):
    driver =models.OneToOneField(Driver, on_delete=models.CASCADE,null=True)
    name_vehicle = models.CharField(max_length=255)
    name_driver = models.CharField(max_length=255,null=True)
    email_driver =models.EmailField(null=True)
    # img_vehicle =models.ImageField(upload_to='vehicle_img/')
    img_vehicle =models.ImageField(null=True)
    description = models.CharField(max_length=255)
    slot_vehicle= models.IntegerField()
    type_vehicle=models.CharField(max_length=255)
    def __str__(self):
        return str(self.email_driver)
    class Meta:
        db_table = 'vehicle'
class Schedules(models.Model):
    vehicle= models.ForeignKey(Vehicle,on_delete=models.CASCADE, null=True)
    name_schedule= models.CharField(max_length=255,null=True)
    slot_vehicle = models.IntegerField(null=True)
    start_location = models.CharField(max_length=255,null=True)
    end_location = models.CharField(max_length=255,null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)  
    day_schedule = models.DateField(null=True)
    start_date = models.DateField(null=True)
    number_of_days = models.PositiveIntegerField(default=1) 
    label_schedule = models.IntegerField(default=1)
    price_schedule = models.IntegerField(null=True)
    class Meta:
        db_table = 'shedules'    
class Orders(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedules, on_delete=models.CASCADE,null=True)
    name_customer_order = models.CharField(max_length=255, null=True)
    name_driver_order = models.CharField(max_length=255, null=True)
    name_schedule_order = models.CharField(max_length=255, null=True)
    name_vehicle_order = models.CharField(max_length=255, null=True)
    name_carowner_order = models.CharField(max_length=255, null=True)
    carowner_id = models.IntegerField(null=True)
    quantity_slot = models.IntegerField(null=True)
    pickup_location= models.CharField(max_length=255,null=True)
    dropoff_location= models.CharField(max_length=255, null=True)
    start_date_time= models.TimeField(null=True)
    dropoff_datetime= models.TimeField(null=True)
    state_order = models.BooleanField(default=False)
    day_schedule = models.DateField(null=True)
    pickup_daytime = models.DateTimeField(null=True)
    state_book = models.CharField(max_length=255,null=True)
    total_price = models.IntegerField(null=True)
    class Meta:
        db_table= 'orders'
class Income(models.Model):
    driver =models.OneToOneField(Driver, on_delete=models.CASCADE,null=True)
    name_driver = models.CharField(max_length=255, null=True)
    total_income = models.IntegerField(null=True)

class CustomSession(models.Model):
    session_key = models.CharField(max_length=40, primary_key=True)
    session_data = models.TextField(null=True)
    expire_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'custom_session'