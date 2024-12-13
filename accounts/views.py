from django.conf import settings
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User

from .serializers import (
    LoginSerializer,
    JWTSerializer,
)

from yeva.utils import log, telegram_webapp_validate


class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    user = None
    # access_token = None
    refresh_token = None

    def process_login(self):
        django_login(self.request, self.user)

    def login(self):
        # self.user = self.serializer.validated_data['user']
        self.refresh_token = RefreshToken.for_user(self.user)
        # self.access_token = self.refresh_token.access_token

        # if settings.SESSION_LOGIN:
        #     self.process_login()

    def get_response(self):
        serializer_class = JWTSerializer
        data = {
            'user': self.user,
            'access': str(self.refresh_token.access_token),
            'refresh': str(self.refresh_token)
        }
        serializer = serializer_class(
            instance=data,
            context=self.get_serializer_context(),
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        self.request = request
        # self.serializer = self.get_serializer(data=self.request.data)
        # self.serializer.is_valid(raise_exception=True)

        # self.login()
        # return self.get_response()
        validated_data = telegram_webapp_validate(request.body.decode('utf-8'), settings.TELEGRAM_BOT_TOKEN)

        log(validated_data)

        # create or get the user from database
        tg_user = validated_data.get('user')
        try:
            user = User.objects.get(telegram_id=tg_user.get('id'))
        except User.DoesNotExist:
            user = User.objects.create(
                telegram_id  = tg_user.get('id'),
                first_name   = tg_user.get('first_name'),
                last_name    = tg_user.get('last_name'),
            )

        self.user = user

        self.login()

        return self.get_response()

        # user=%7B%22id%22%3A5189503550%2C%22first_name%22%3A%22-_-%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22nickphilomath%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2F7nkdVed-TsoL8UkWQW1WcVlFvfnFMBPB1IcLahlqiAf1xYVPA_M3Nmv1wrxpId2B.svg%22%7D&chat_instance=-7564035028080141132&chat_type=sender&auth_date=1732451238&signature=V_AShWLgbgNdZDvh0bV7TpG5s7xUg4nJadbghPuaPA24y-7oGsplNJqT8wmajaz_A3jH5DflNk4-Yv7-vivCCA&hash=6150a996542795f3342439fa292eff51db744125a95f46bf0d4612697f1bc549


class PromoteToDriverView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        user.is_driver = True
        user.save()

        return Response(status=status.HTTP_200_OK)
