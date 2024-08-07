from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import ResponseWriteSerializer


class AddResponseView(APIView):

    def post(self, request):
        serializer = ResponseWriteSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={"message": "Your response successfully submitted."},
        )
