from rest_framework import serializers

from responses.models import PipelineSubmission, Response

# class PipelineReportSerializer(serializers.ModelSerializer):


class ResponseReportSerializer(serializers.ModelSerializer):
    responsed_forms = serializers.SerializerMethodField()
    responses = serializers.SerializerMethodField()

    class Meta:
        model = PipelineSubmission
        exclude = ("pipeline",)
        depth = 2

    def get_responsed_forms(self, obj: PipelineSubmission):
        return obj.responses["responsed_forms"]

    def get_responses(self, obj: PipelineSubmission):
        RESPONSES = {}

        for form_id in obj.responses["responsed_forms"]:
            response = Response.objects.get(
                form__id=form_id,
                pipeline__id=obj.pipeline.id,
                pipeline_submission__id=obj.id,
            )
            RESPONSES[form_id] = response.data
        return RESPONSES
