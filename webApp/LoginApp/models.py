from django.db import models
from django.contrib.auth.models import Group,Permission
from django.contrib.auth.models import  AbstractUser
from django.utils.translation import gettext as _
import uuid


class CustomerUser(AbstractUser):
    address_user =models.CharField(max_length=100, null=True)
    phone_user =models.IntegerField(null=True)
    verify_user = models.BooleanField(default=False)
    token_user= models.CharField(max_length=255, null=True, blank=True)
    user_groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, verbose_name=_('user permissions'), blank=True, related_name='custom_user_set')
    class Meta:
        db_table = 'customeruser'