from rest_framework import serializers

from forms.models import Field, Form, Pipeline


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = "__all__"


class FormSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True, read_only=True)

    class Meta:
        model = Form
        fields = "__all__"

    def create(self, validated_data):
        field_id = self.initial_data['fields']
        field_instances = [Field.objects.get(pk=int(field_id))]
        form = Form.objects.create(**validated_data)
        form.fields.set(field_instances)
        return form

    def update(self, instance, validated_data):
        field = self.initial_data.get('fields', None)
        instance = super(FormSerializer, self).update(instance, validated_data)
        if field:
            field_id = field['id']
            fields = Field.objects.get(pk=field_id)
            if self.initial_data['remove']:
                instance.fields.remove(fields)
            else:
                instance.fields.add(fields)
        return instance


class PipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipeline
        fields = "__all__"
