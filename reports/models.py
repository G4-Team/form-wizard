from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from forms.models import Pipeline


def set_default_expired_datetime():
    now = timezone.make_aware(timezone.datetime.now(), timezone.get_default_timezone())
    return now + timezone.timedelta(days=30)


class Subscriber(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    pipeline = models.ForeignKey(to=Pipeline, on_delete=models.CASCADE)
    expired_datetime = models.DateTimeField(default=set_default_expired_datetime)
