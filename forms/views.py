from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from forms.models import Field, Form
from forms.serializers import FieldSerializer, FormSerializer
from permissions import IsOwnerOrReadOnly


class AllFieldListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        fields = Field.objects.all()
        serializer = FieldSerializer(instance=fields, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FieldListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        fields = Field.objects.filter(owner=user)
        serializer = FieldSerializer(instance=fields, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FieldDataView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)
    def get(self, request, pk):
        field = Field.objects.get(pk=pk)
        serializer = FieldSerializer(instance=field)
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
    permission_classes = (IsOwnerOrReadOnly,)

    def put(self, request, pk):
        field = Field.objects.get(pk=pk)
        self.check_object_permissions(request, field)
        serializer = FieldSerializer(instance=field, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FieldDeleteView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def delete(self, request, pk):
        field = Field.objects.get(pk=pk)
        self.check_object_permissions(request, field)
        field.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AllFormListView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        form = Form.objects.all()
        serializer = FormSerializer(instance=form, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FormListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        forms = Form.objects.filter(owner=user)
        serializer = FormSerializer(instance=forms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FormDataView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)
    def get(self, request, pk):
        form = Form.objects.get(pk=pk)
        serializer = FormSerializer(instance=form)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FormCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = FormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormAddField(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def put(self, request, form_pk, field_pk):
        field = Field.objects.get(pk=field_pk)
        form = Form.objects.get(pk=form_pk)
        self.check_object_permissions(request, field)
        self.check_object_permissions(request, form)
        field_serializer = FieldSerializer(instance=field)
        if field_serializer.is_valid():
            form_serializer = FormSerializer(instance=form, data=field_serializer.data, partial=True)
            if form_serializer.is_valid() and field_serializer.is_valid():
                form_serializer.save()
                return Response(form_serializer.data, status=status.HTTP_201_CREATED)
            return Response(form_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(field_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormViewSet(viewsets.ModelViewSet):
    serializer_class = FormSerializer
    queryset = Form.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        serializer = self.serializer_class(
            self.queryset.filter(owner=request.user), many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        pass

    def retrieve(self, request, pk):
        pass

    def update(self, request, pk):
        pass

    def partial_update(self, request, pk):
        pass

    def destroy(self, request, pk):
        pass
