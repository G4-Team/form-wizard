from rest_framework import serializers

from forms.models import Field, Form, Pipeline


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = "__all__"


class FormSerializer(serializers.ModelSerializer):
    fields = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Form
        fields = "__all__"

    def create(self, validated_data):
        fields = self.initial_data['fields'].split(',')
        field_instances = []
        for field in fields:
            field_instances.append(Field.objects.get(pk=int(field)))
        form = Form.objects.create(**validated_data)
        form.fields.set(field_instances)
        return form

    def update(self, instance, validated_data):
        fields_data = validated_data.pop('fields')
        instance = super(FormSerializer, self).update(instance, validated_data)

        for fields_data in fields_data:
            fields_qs = Field.objects.filter(pk=fields_data['id'])

            if fields_qs.exists():
                fields = fields_qs.first()
            else:
                fields = Field.objects.create(**fields_data)

            instance.fields.add(fields)

        return instance


class PipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipeline
        fields = "__all__"
