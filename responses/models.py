from django.contrib.auth import get_user_model
from django.db import models

from forms.models import Pipline


class Response(models.Model):
    owner = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
    )
    pipline = models.ForeignKey(
        to=Pipline,
        on_delete=models.CASCADE,
    )
    data = models.JSONField()
