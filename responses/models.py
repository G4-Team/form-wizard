from django.contrib.auth import get_user_model
from django.db import models

from forms.models import Form, Pipeline


class Response(models.Model):
    owner = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
    )
    ip = models.GenericIPAddressField(null=True, blank=True)
    pipeline = models.ForeignKey(
        to=Pipeline,
        on_delete=models.CASCADE,
    )
    form = models.ForeignKey(
        to=Form,
        on_delete=models.CASCADE,
    )
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
