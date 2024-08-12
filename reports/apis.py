from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from responses.models import PipelineSubmission

from .serializers import ResponseReportSerializer


class PeriodicReportApi(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResponseReportSerializer
    lookup_url_kwarg = "pipeline_id"
    lookup_field = "pk"

    def get_queryset(self):
        now = timezone.make_aware(
            timezone.datetime.now(), timezone.get_default_timezone()
        )
        period = self.request.query_params.get("period")
        if period is not None:
            if period == "monthly":
                time_query = now - timezone.timedelta(days=30)
            elif period == "weekly":
                time_query = now - timezone.timedelta(days=7)
            elif period == "daily":
                time_query = now - timezone.timedelta(days=1)
            else:
                raise ValidationError(
                    {
                        "period": "You entered an incorrect time period. It should be one of the following: [monthly, weekly, daily]."
                    }
                )
        else:
            time_query = now - timezone.timedelta(days=30)
        return PipelineSubmission.objects.filter(
            pipeline__owner__id=self.request.user.id, updated_at__gte=time_query
        )
