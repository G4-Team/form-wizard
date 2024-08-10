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


def get_default_responses():
    return {
        "responsed_forms": [],
    }


class PipelineSubmission(models.Model):
    pipeline = models.ForeignKey(to=Pipeline, on_delete=models.CASCADE)
    responses = models.JSONField(default=get_default_responses)
    owner = models.ForeignKey(
        to=get_user_model(), on_delete=models.SET_NULL, null=True, blank=True
    )
    ip = models.GenericIPAddressField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
