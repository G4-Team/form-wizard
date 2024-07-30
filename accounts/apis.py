from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterUserSerializer


class RegisterUser(APIView):

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
