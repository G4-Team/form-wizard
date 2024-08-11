from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from forms.models import Field, Form, Pipeline, Category
from forms.serializers import (
    FieldSerializer,
    FormSerializer,
    PipelineSerializer,
    UpdateFieldSerializer,
    UpdateFormSerializer, CategorySerializer,
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


class FieldDataView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FieldSerializer
    lookup_url_kwarg = "field_id"
    lookup_field = "pk"

    def get_queryset(self):
        return Field.objects.filter(owner__id=self.request.user.id)


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
        field = get_object_or_404(Field, pk=field_id)
        self.check_object_permissions(request, field)
        serializer = UpdateFieldSerializer(
            instance=field, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class FieldDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = "field_id"
    lookup_field = "pk"

    def get_queryset(self):
        return Field.objects.filter(owner__id=self.request.user.id)


# Form API Views
class FormListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FormSerializer

    def get_queryset(self):
        if self.request.user.is_admin:
            return Form.objects.all()
        return Form.objects.filter(owner__id=self.request.user.id)


class FormDataView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FormSerializer
    lookup_url_kwarg = "form_id"
    lookup_field = "pk"

    def get_queryset(self):
        return Form.objects.filter(owner__id=self.request.user.id)


class FormCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = FormSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FormUpdateView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def put(self, request, form_id):
        form = get_object_or_404(Form, pk=form_id)
        self.check_object_permissions(request, form)
        serializer = UpdateFormSerializer(
            instance=form,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FormDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = "form_id"
    lookup_field = "pk"

    def get_queryset(self):
        return Form.objects.filter(owner__id=self.request.user.id)


# Pipeline API Views
class PipelineListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PipelineSerializer

    def get_queryset(self):
        if self.request.user.is_admin:
            return Pipeline.objects.all()
        return Pipeline.objects.filter(owner__id=self.request.user.id)


class PipelineDataView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PipelineSerializer
    lookup_url_kwarg = "pipeline_id"
    lookup_field = "pk"

    def get_queryset(self):
        return Pipeline.objects.filter(owner__id=self.request.user.id)


class PipelineCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PipelineSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PipelineUpdateView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def put(self, request, pipeline_id):
        pipeline = get_object_or_404(Pipeline, pk=pipeline_id)
        self.check_object_permissions(request, pipeline)
        serializer = PipelineSerializer(
            instance=pipeline,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PipelineDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = "pipeline_id"
    lookup_field = "pk"

    def get_queryset(self):
        return Pipeline.objects.filter(owner__id=self.request.user.id)


class PipelineShareView(APIView):
    def get(self, request, pipeline_id):
        pipeline = Pipeline.objects.get(pk=pipeline_id)
        if pipeline.hide_next_button: #pipeline is ordered
            forms_id = pipeline.metadata['order']
            last_answered_form_id = None
            for form_id in forms_id: #find last_answered_form_id by user
                form = Form.objects.get(pk=form_id)
                user_response = form.responses.filter(session_key=request.session.session_key).exists()
                if user_response:
                    last_answered_form_id = form_id
            if last_answered_form_id == forms_id[-1]:  #case user has completed survey
                return Response('you have already answered', status=status.HTTP_400_BAD_REQUEST)
            elif last_answered_form_id is None: #case user has not answered yet
                form = Form.objects.get(pk=forms_id[0])
                serializer = FormSerializer(instance=form, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            else: #case still there is still forms for user to answer
                index = forms_id.index(last_answered_form_id)
                form = Form.objects.get(pk=forms_id[index+1])
                serializer = FormSerializer(instance=form, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
        else: #case the pipeline is not ordered
            serializer = PipelineSerializer(instance=pipeline)
            return Response(serializer.data, status=status.HTTP_200_OK)


# Category API Views
class CategoryCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CategorySerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryUpdateView(APIView):
    permission_classes = (IsOwnerOrReadOnly, )

    def put(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        self.check_object_permissions(request, category)
        serializer = CategorySerializer(
            instance=category,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer

    def get_queryset(self):
        if self.request.user.is_admin:
            return Category.objects.all()
        return Category.objects.filter(owner__id=self.request.user.id)


class CategoryDataView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    lookup_url_kwarg = 'category_id'
    lookup_field = 'pk'

    def get_queryset(self):
        return Category.objects.filter(owner__id=self.request.user.id)


class CategoryDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = 'category_id'
    lookup_field = 'pk'

    def get_queryset(self):
        return Category.objects.filter(owner__id=self.request.user.id)
