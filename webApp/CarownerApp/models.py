from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from LoginApp.models import CarOwner

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
    def __str__(self):
        return self.email_driver
    class Meta:
        db_table = 'driver'
class Vehicle(models.Model):
    driver =models.OneToOneField(Driver, on_delete=models.CASCADE,null=True)
    name_vehicle = models.CharField(max_length=255)
    img_vehicle =models.ImageField(upload_to='vehicle_img/')
    description = models.CharField(max_length=255)
    slot_vehicle= models.IntegerField()
    type_vehicle=models.CharField(max_length=255)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'vehicle'
class Schedules(models.Model):
    vehicle= models.ForeignKey(Vehicle,on_delete=models.CASCADE, null=True)
    name_schedule= models.CharField(max_length=255,null=True)
    start_location = models.CharField(max_length=255,null=True)
    end_location = models.CharField(max_length=255,null=True)
    start_date_time = models.DateTimeField(null=True)
    end_date_time = models.DateTimeField(null=True)    
    class Meta:
        db_table = 'shedules'    
    