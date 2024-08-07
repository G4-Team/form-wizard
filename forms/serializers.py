from rest_framework import serializers

from forms.models import Field, Form, Pipeline, Response


class FieldSerializer(serializers.ModelSerializer):
    # owner = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Field
        fields = '__all__'


class FormSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True, read_only=True)
    owner = serializers.StringRelatedField(read_only=True)

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
