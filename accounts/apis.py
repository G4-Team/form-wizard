from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProfileSerializer, RegisterUserSerializer


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
