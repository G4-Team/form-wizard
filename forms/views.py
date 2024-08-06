from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from forms.models import Field
from forms.serializers import FieldSerializer
from permissions import IsOwnerOrReadOnly


class FieldListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        fields = Field.objects.filter(owner=user)
        serializer = FieldSerializer(instance=fields, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FieldCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = FieldSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FieldUpdateView(APIView):
    permission_classes = (IsOwnerOrReadOnly, )

    def put(self, request, pk):
        field = Field.objects.get(pk=pk)
        self.check_object_permissions(request, field)
        serializer = FieldSerializer(instance=field, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FieldDeleteView(APIView):
    permission_classes = (IsOwnerOrReadOnly, )

    def delete(self, request, pk):
        field = Field.objects.get(pk=pk)
        self.check_object_permissions(request, field)
        field.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
