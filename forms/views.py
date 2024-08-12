from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from forms.models import Category, Field, Form, Pipeline
from forms.serializers import (
    CategorySerializer,
    FieldSerializer,
    FormSerializer,
    PipelineSerializer,
    PipelineShowSerializer,
    UpdateFieldSerializer,
    UpdateFormSerializer,
)
from permissions import IsOwnerOrReadOnly

from .models import COMMON_REGEX_TYPES


# Field API Views
class CommonRegexApi(APIView):
    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request):
        return Response(data=COMMON_REGEX_TYPES)


class FieldListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FieldSerializer

    def get_queryset(self):
        if self.request.user.is_admin:
            return Field.objects.all()
        return Field.objects.filter(owner__id=self.request.user.id)

    @method_decorator(vary_on_cookie)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class FieldDataView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FieldSerializer
    lookup_url_kwarg = "field_id"
    lookup_field = "pk"

    def get_queryset(self):
        return Field.objects.filter(owner__id=self.request.user.id)

    @method_decorator(vary_on_cookie)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


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
        category = self.request.query_params.get("category")
        if self.request.user.is_admin:
            if category is not None:
                return Form.objects.filter(categories__name=category)
            return Form.objects.all()
        if category is not None:
            return Form.objects.filter(
                owner__id=self.request.user.id, categories__name=category
            )
        return Form.objects.filter(owner__id=self.request.user.id)

    @method_decorator(vary_on_cookie)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class FormDataView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FormSerializer
    lookup_url_kwarg = "form_id"
    lookup_field = "pk"

    def get_queryset(self):
        return Form.objects.filter(owner__id=self.request.user.id)

    @method_decorator(vary_on_cookie)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


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
        category = self.request.query_params.get("category")
        if self.request.user.is_admin:
            if category is not None:
                return Pipeline.objects.filter(categories__name=category)
            return Pipeline.objects.all()
        if category is not None:
            return Pipeline.objects.filter(
                owner__id=self.request.user.id, categories__name=category
            )
        return Pipeline.objects.filter(owner__id=self.request.user.id)

    @method_decorator(vary_on_cookie)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class PipelineDataView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PipelineSerializer
    lookup_url_kwarg = "pipeline_id"
    lookup_field = "pk"

    def get_queryset(self):
        return Pipeline.objects.filter(owner__id=self.request.user.id)

    @method_decorator(vary_on_cookie)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


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


# class PipelineShareView(APIView):
#     def get(self, request, pipeline_id):
#         pipeline = Pipeline.objects.get(pk=pipeline_id)
#         if pipeline.hide_next_button:  # pipeline is ordered
#             forms_id = pipeline.metadata["order"]
#             last_answered_form_id = None
#             for form_id in forms_id:  # find last_answered_form_id by user
#                 form = Form.objects.get(pk=form_id)
#                 user_response = form.responses.filter(
#                     session_key=request.session.session_key
#                 ).exists()
#                 if user_response:
#                     last_answered_form_id = form_id
#             if last_answered_form_id == forms_id[-1]:  # case user has completed survey
#                 return Response(
#                     "you have already answered", status=status.HTTP_400_BAD_REQUEST
#                 )
#             elif last_answered_form_id is None:  # case user has not answered yet
#                 form = Form.objects.get(pk=forms_id[0])
#                 serializer = FormSerializer(instance=form, context={"request": request})
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             else:  # case still there is still forms for user to answer
#                 index = forms_id.index(last_answered_form_id)
#                 form = Form.objects.get(pk=forms_id[index + 1])
#                 serializer = FormSerializer(instance=form, context={"request": request})
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#         else:  # case the pipeline is not ordered
#             serializer = PipelineSerializer(instance=pipeline)
#             return Response(serializer.data, status=status.HTTP_200_OK)
class PipelineShareView(RetrieveAPIView):
    serializer_class = PipelineShowSerializer
    lookup_url_kwarg = "pipeline_slug"
    lookup_field = "slug"

    class InputSerializer(serializers.Serializer):
        password = serializers.CharField(required=True)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg
        filter_kwargs = {
            self.lookup_field: self.kwargs[lookup_url_kwarg],
        }
        obj: Pipeline = get_object_or_404(queryset, **filter_kwargs)
        if obj.is_private:
            serializer = self.InputSerializer(data=self.request.data)
            serializer.is_valid(raise_exception=True)
            if obj.password != serializer.validated_data["password"]:
                raise ValidationError({"password": "The password is incorrect."})

        self.check_object_permissions(self.request, obj)
        obj.number_of_views = F("number_of_views") + 1
        obj.save()
        return obj

    def get_queryset(self):
        return Pipeline.objects.all()

    def get(self, request, *args, **kwargs):

        return super().get(request, *args, **kwargs)


# Category API Views
class CategoryCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CategorySerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryUpdateView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

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

    @method_decorator(vary_on_cookie)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class CategoryDataView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    lookup_url_kwarg = "category_id"
    lookup_field = "pk"

    def get_queryset(self):
        return Category.objects.filter(owner__id=self.request.user.id)

    @method_decorator(vary_on_cookie)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class CategoryDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = "category_id"
    lookup_field = "pk"

    def get_queryset(self):
        return Category.objects.filter(owner__id=self.request.user.id)
