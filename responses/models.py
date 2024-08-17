from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.db import models

from forms.models import Form, Pipeline


class Response(models.Model):
    owner = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    pipeline = models.ForeignKey(
        to=Pipeline,
        on_delete=models.CASCADE,
        related_name="responses",
    )
    form = models.ForeignKey(
        to=Form,
        on_delete=models.CASCADE,
        related_name="responses",
    )
    pipeline_submission = models.ForeignKey(
        to="PipelineSubmission", on_delete=models.CASCADE
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
    session_key = models.CharField(max_length=40, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
