from rest_framework import serializers

from forms.models import Field, Form, Pipeline


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = "__all__"


    def validate_type(self, value):
        if type(value) is not int:
            raise serializers.ValidationError('Type must be an integer from 1 to 9')
    def validate(self, data):
        pass


class FormSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True, read_only=True)

    class Meta:
        model = Form
        fields = "__all__"

    def create(self, validated_data):
        form = Form.objects.create(**validated_data)
        field_id = self.initial_data['fields']
        field_instance = [Field.objects.get(pk=int(field_id))]
        form.fields.set(field_instance)
        return form

    def update(self, instance, validated_data):
        instance = super(FormSerializer, self).update(instance, validated_data)
        field = self.initial_data.get('fields', None)
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

    def create(self, validated_data):
        pipeline = Pipeline.objects.create(**validated_data)
        form_id = self.initial_data['forms']
        form_instance = [Form.objects.get(pk=int(form_id))]
        pipeline.forms.set(form_instance)
        return pipeline

    def update(self, instance, validated_data):
        instance = super(PipelineSerializer, self).update(instance, validated_data)
        form = self.initial_data.get('forms', None)
        if form:
            form_id = form['id']
            forms = Form.objects.get(pk=form_id)
            if self.initial_data['remove']:
                instance.forms.remove(forms)
            else:
                instance.forms.add(forms)
        return instance
