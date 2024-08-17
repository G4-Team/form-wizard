from celery import shared_task
from celery.utils.log import get_task_logger

from .models import Subscriber
from .serializers import ResponseReportSerializer
from .utils import send_email

logger = get_task_logger(__name__)


@shared_task
def send_reports_to_subscriber():
    for subscriber in Subscriber.objects.select_related("user", "pipeline").all():
        send_email(
            subject=f"Your monthly repost of {subscriber.pipeline.title}",
            message=str(ResponseReportSerializer(instance=subscriber.pipeline).data),
            receiver=subscriber.user.email,
        )
