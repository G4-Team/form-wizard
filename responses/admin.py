from django.contrib import admin

from .models import PipelineSubmission, Response

admin.site.register(Response)
admin.site.register(PipelineSubmission)
