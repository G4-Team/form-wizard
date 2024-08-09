from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Response as ResponseModel
from .serializer import ResponseUpdateSerializer, ResponseWriteSerializer


class AddResponseView(APIView):

    def post(self, request):
        serializer = ResponseWriteSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)


class UpdateResponseView(APIView):
    def patch(self, request, response_id):
        response = get_object_or_404(ResponseModel, id=response_id)
        serializer = ResponseUpdateSerializer(
            instance=response,
            data=request.data,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"hi": "hi"})
