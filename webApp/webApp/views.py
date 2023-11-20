
import os
from django.http import HttpResponseRedirect
from django.shortcuts import render , redirect
from django.contrib.auth import logout
from CarownerApp.models import Driver,Schedules,Vehicle,Orders
from django.db.models import Prefetch

import shutil
from django.conf import settings

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

from LoginApp.models import Customer
from django.utils import timezone
from django.db.models import Q
from datetime import datetime
from CarownerApp.models import CustomSession
from django.contrib.sessions.models import Session
import numpy as np
from django.contrib.auth.views import LogoutView



def custom_logout(request, *args, **kwargs):
    print("Custom Logout: Custom logout action--------------------------------")
    return render(request, 'HomeApp/home.html')

class CustomLogoutView(LogoutView):
    def logout(self, request):
        print("..........................Custom logout")
        admin_sessions = Session.objects.filter(
            expire_date__gte=timezone.now(),
            session_data__contains='"{}"'.format(request.user.username),
        )
        admin_sessions.delete()
        response = super().logout(request)
        return response  