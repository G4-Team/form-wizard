from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from forms.models import Field, Form, Pipeline
from forms.serializers import (
    FieldSerializer,
    FormSerializer,
    PipelineSerializer,
    UpdateFieldSerializer,
)
from permissions import IsOwnerOrReadOnly

from .models import COMMON_REGEX_TYPES


# Field API Views
class CommonRegexApi(APIView):
    def get(self, request):
        return Response(data=COMMON_REGEX_TYPES)


class FieldListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FieldSerializer

    def get_queryset(self):
        if self.request.user.is_admin:
            return Field.objects.all()
        return Field.objects.filter(owner__id=self.request.user.id)


class FieldDataView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, field_id):
        field = Field.objects.get(pk=field_id)
        serializer = FieldSerializer(instance=field)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FieldCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = FieldSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FieldUpdateView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def put(self, request, field_id):
        field = Field.objects.get(pk=field_id)
        self.check_object_permissions(request, field)
        serializer = UpdateFieldSerializer(
            instance=field, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class FieldDeleteView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def delete(self, request, field_id):
        field = Field.objects.get(pk=field_id)
        self.check_object_permissions(request, field)
        field.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Form API Views


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

    def get(self, request, form_id):
        form = Form.objects.get(pk=form_id)
        serializer = FormSerializer(instance=form)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FormCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = FormSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormUpdateView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def put(self, request, form_id):
        form = Form.objects.get(pk=form_id)
        self.check_object_permissions(request, form)
        serializer = FormSerializer(instance=form, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormDeleteView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def delete(self, request, form_id):
        form = Form.objects.get(pk=form_id)
        self.check_object_permissions(request, form)
        form.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Pipeline API Views


class AllPipelineListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        pipeline = Pipeline.objects.all()
        serializer = PipelineSerializer(instance=pipeline, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PipelineListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        pipelines = Pipeline.objects.filter(owner=user)
        serializer = PipelineSerializer(instance=pipelines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PipelineDataView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, pipeline_id):
        pipeline = Pipeline.objects.get(pk=pipeline_id)
        serializer = PipelineSerializer(instance=pipeline)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PipelineCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PipelineSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PipelineUpdateView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def put(self, request, pipeline_id):
        pipeline = Pipeline.objects.get(pk=pipeline_id)
        self.check_object_permissions(request, pipeline)
        serializer = PipelineSerializer(
            instance=pipeline, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PipelineDeleteView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def delete(self, request, pipeline_id):
        pipeline = Pipeline.objects.get(pk=pipeline_id)
        pipeline.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
