from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from registration_profile.models import RegistrationProfile
from registration_profile.serializers import RegistrationSerializer, RegistrationValidationSerializer

User = get_user_model()


class CreateRegistrationView(GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        send_mail(
            'Thank you for registering!',
            'Thank you for registering for Motion\n'
            f'Here is your code for registration:\n{instance.code}',
            'propulsionteamphp@gmail.com',
            [request.data['email']],
            fail_silently=False,
        )
        return Response(status.HTTP_200_OK)


class ValidateCreateRegistrationView(GenericAPIView):
    serializer_class = RegistrationValidationSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User(email=request.data['email'],
                    password=make_password(request.data['password']),
                    username=request.data['username'],
                    first_name=request.data['first_name'],
                    last_name=request.data['last_name'])
        user.save()
        return Response(status.HTTP_200_OK)
