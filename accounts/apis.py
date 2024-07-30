from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class RegisterUser(APIView):
    def post(self, request):
        return Response(data={"hello": request.user.first_name})
