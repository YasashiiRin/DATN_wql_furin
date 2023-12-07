
from datetime import timedelta
from LoginApp.models import Customer
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from django.conf import settings
import json
from datetime import datetime
from django.utils import timezone
from CarownerApp.models import CustomSession
class CustomerBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Thực hiện xác thực như bình thường
        user = super().authenticate(request, username=username, password=password, **kwargs)
        if user:
            # Kiểm tra xem user có phải là CarOwner hay không
            if hasattr(user, 'carowner'):
                session_data = {
                    'user_id': user.id,
                    'user_type': 'carowner',
                }
                session_data_str = json.dumps(session_data)
                session_key = f'carowner_{user.id}_session_key'
                expire_seconds = 3000
                custom_session, created = CustomSession.objects.get_or_create(session_key=session_key)
                custom_session.session_data = session_data_str
                custom_session.expire_date = timezone.now() + timedelta(seconds=expire_seconds)
                custom_session.save()
                request.session[settings.CAROWNER_SESSION_COOKIE_NAM] = session_key
                print("khởi chạy session của carowner..........")
        return user

    def custom_login(request, user, user_type):
        session_data = {
            'user_id': user.id,
            'user_type': user_type,
        }
        session_data_str = json.dumps(session_data)
        session_key = f'{user_type}_{user.id}_session_key'
        if user_type == 'customer':
            expire_seconds = 3000
            custom_session, created = CustomSession.objects.get_or_create(session_key=session_key)
            custom_session.session_data = session_data_str
            custom_session.expire_date = timezone.now() + timedelta(seconds=expire_seconds)
            custom_session.save()
            request.session[settings.CUSTOMER_SESSION_COOKIE_NAME] = session_key
        elif user_type == 'driver':
            expire_seconds = 3000
            custom_session, created = CustomSession.objects.get_or_create(session_key=session_key)
            custom_session.session_data = session_data_str
            custom_session.expire_date = timezone.now() + timedelta(seconds=expire_seconds)
            custom_session.save()
            request.session[settings.DRIVER_SESSION_COOKIE_NAME] = session_key
        else:
            raise ValueError("Invalid user_type")
        request.session.save()

        # if user_type == 'customer':
        #     request.session[settings.CUSTOMER_SESSION_COOKIE_NAME] = {
        #         'id_customer': user.id,
        #     }
        # if user_type == 'driver':
        #     request.session[settings.DRIVER_SESSION_COOKIE_NAME] = {
        #         'id_driver': user.id,
        # }
        # request.session.save()
        # print("check id :", user.id)
        # return user
