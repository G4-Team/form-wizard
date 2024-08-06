from rest_framework import serializers

from forms.models import Field, Form, Pipeline, Response


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = '__all__'


class PipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipeline
        fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = '__all__'
