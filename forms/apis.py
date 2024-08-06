from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Form, Pipline
from .permissions import IsOwner
from .serializer import FormSerializer


class FormApiViewset(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = FormSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Form.objects.filter(owner__id=self.request.user.id)
