from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

class CustomerUser(AbstractUser):
    address_user = models.CharField(max_length=100, null=True)
    phone_user = models.IntegerField(null=True)
    verify_user = models.BooleanField(default=False)
    token_user = models.CharField(max_length=255, null=True, blank=True)
    user_groups = models.ManyToManyField('auth.Group', verbose_name=_('user groups'), blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', verbose_name=_('user permissions'), blank=True)

    class Meta:
        db_table = 'customeruser'
class OwnerCar(models.Model):
    name_ownercar = models.CharField(max_length=255)
    email_ownercar = models.EmailField(max_length=255)
    password_ownercar = models.CharField(max_length=255)
    address_ownercar = models.CharField(max_length=100, null=True)
    phone_ownercar = models.IntegerField(null=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_authenticated=models.BooleanField(default=False)
    verify_ownercar = models.BooleanField(default=False)
    token_ownercar = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        db_table = 'ownercar'