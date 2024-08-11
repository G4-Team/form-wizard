from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PipelineSubmission
from .models import Response as ResponseModel
from .serializer import (
    PipelineSubmissionSerializer,
    ResponseUpdateSerializer,
    ResponseWriteSerializer,
)


class AddResponseView(APIView):

    def post(self, request):
        serializer = ResponseWriteSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        channel_layer = get_channel_layer()
        phone = serializer.validated_data["pipeline"].owner.phone
        async_to_sync(channel_layer.group_send)(
            f"report_{phone}",
            {
                "type": "form_response",
                "message": f"New response submitted: {serializer.data}",
            },
        )
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
        return Response(data=serializer.data)


class ResponseRetriveApi(RetrieveAPIView):
    lookup_field = "pk"
    lookup_url_kwarg = "pipeline_sunbmission_id"
    serializer_class = PipelineSubmissionSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_admin:
                return PipelineSubmission.objects.all()
            return PipelineSubmission.objects.filter(owner__id=self.request.user.id)

        if self.request.session.session_key is None:
            self.request.session.creat()
        return PipelineSubmission.objects.filter(
            session_key=self.request.session.session_key
        )
