from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from forms.models import Field, Form, Pipeline
from forms.serializers import FieldSerializer, FormSerializer, PipelineSerializer
from permissions import IsOwnerOrReadOnly


#Field API Views

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

    def get(self, request, field_id):
        field = Field.objects.get(pk=field_id)
        serializer = FieldSerializer(instance=field)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FieldCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = FieldSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FieldUpdateView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def put(self, request, field_id):
        field = Field.objects.get(pk=field_id)
        self.check_object_permissions(request, field)
        serializer = FieldSerializer(instance=field, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FieldDeleteView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def delete(self, request, field_id):
        field = Field.objects.get(pk=field_id)
        self.check_object_permissions(request, field)
        field.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Form API Views

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
        serializer = FormSerializer(data=request.data, context={'request': request})
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


#Pipeline API Views

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
        serializer = PipelineSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PipelineUpdateView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)

    def put(self, request, pipeline_id):
        pipeline = Pipeline.objects.get(pk=pipeline_id)
        self.check_object_permissions(request, pipeline)
        serializer = PipelineSerializer(instance=pipeline, data=request.data, partial=True)
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
