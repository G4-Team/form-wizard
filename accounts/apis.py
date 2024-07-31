from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    OtpPhoneSerializer,
    OtpValidatSerializer,
    ProfileSerializer,
    RegisterUserSerializer,
)
from .utils import get_or_create_verfication_code, send_code


class RegisterUserApi(APIView):

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = {
            "message": f"hello {serializer.validated_data['first_name']} {serializer.validated_data['last_name']}, you registerd sucessfully :)"
        }
        return Response(
            data=response_data,
            status=status.HTTP_201_CREATED,
        )


class ProfileApi(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        serializer = ProfileSerializer(instance=request.user)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = RegisterUserSerializer(
            instance=request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = {"message": "your profile updated sucessfully."}
        return Response(
            data=response_data,
            status=status.HTTP_202_ACCEPTED,
        )


class SendOtpCodeApi(APIView):
    def post(self, request):
        serializer = OtpPhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = get_or_create_verfication_code(phone=serializer.validated_data["phone"])
        send_code(code=code.code, phone=serializer.validated_data["phone"])
        return Response(
            data={
                "message": "we sent a code. please enter the code within the next three minutes."
            },
            status=status.HTTP_201_CREATED,
        )


class ValidateOtpCodeApi(APIView):
    User = get_user_model()

    def post(self, request):
        serializer = OtpValidatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.User.objects.get(phone=serializer.validated_data["phone"])
        refresh = RefreshToken.for_user(user)

        response_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return Response(
            data=response_data,
            status=status.HTTP_200_OK,
        )
