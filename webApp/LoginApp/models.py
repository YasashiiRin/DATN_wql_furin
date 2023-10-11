from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

class CarOwner(AbstractUser):
    address_carowner = models.CharField(max_length=100, null=True)
    phone_carowner = models.IntegerField(null=True)
    verify_carowner = models.BooleanField(default=False)
    token_carowner = models.CharField(max_length=255, null=True, blank=True)
    carowner_groups = models.ManyToManyField('auth.Group', verbose_name=_('carowner groups'), blank=True)
    carowner_permissions = models.ManyToManyField('auth.Permission', verbose_name=_('carowner permissions'), blank=True)

    class Meta:
        db_table = 'carowner'
class Customer(models.Model):
    name_customer = models.CharField(max_length=255)
    email_customer = models.EmailField(max_length=255)
    password_customer = models.CharField(max_length=255)
    address_customer = models.CharField(max_length=100, null=True)
    phone_customer = models.IntegerField(null=True)
    img_customer =models.ImageField(null=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_authenticated=models.BooleanField(default=False)
    verify_customer = models.BooleanField(default=False)
    token_customer = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        db_table = 'customer'
    def __str__(self):
        return self.name_customer

