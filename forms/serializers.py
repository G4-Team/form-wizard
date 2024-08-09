from rest_framework import serializers

from forms.models import Field, Form, Pipeline


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = "__all__"


    def validate_type(self, value):
        if value < 1 or value > 9:
            raise serializers.ValidationError('Type must be an integer from 1 to 9')
        return value
    def validate(self, data):
        type = data.get('type')
        metadata = data.get('metadata')

        match type:
            case Field.TYPES.TXT_INPUT_FR:
                if 'placeholder' not in metadata or not metadata['placeholder']:
                    raise serializers.ValidationError('Metadata must contain a placeholder like "only persian"')
                if 'answer_max_length' not in metadata or metadata['answer_max_length'] < 1:
                    raise serializers.ValidationError('Metadata must contain a answer_max_length more than 0')
                if 'answer_min_length' not in metadata or metadata['answer_min_length'] < 0:
                    raise serializers.ValidationError('Metadata must contain a non negative answer_min_length')
                if metadata['answer_max_length'] < metadata['answer_min_length']:
                    raise serializers.ValidationError('value of answer_max_length can not be less than answer_min_length')
            case Field.TYPES.TXT_INPUT_ENG:
                if 'placeholder' not in metadata or not metadata['placeholder']:
                    raise serializers.ValidationError('Metadata must contain a placeholder like "only english"')
                if 'answer_max_length' not in metadata or metadata['answer_max_length'] < 1:
                    raise serializers.ValidationError('Metadata must contain a answer_max_length more than 0')
                if 'answer_min_length' not in metadata or metadata['answer_min_length'] < 0:
                    raise serializers.ValidationError('Metadata must contain a non negative answer_min_length')
                if metadata['answer_max_length'] < metadata['answer_min_length']:
                    raise serializers.ValidationError('value of answer_max_length can not be less than answer_min_length')
            case Field.TYPES.TXT_INPUT_NUMBERS:
                if 'placeholder' not in metadata or not metadata['placeholder']:
                    raise serializers.ValidationError('Metadata must contain a placeholder like "only numbers"')
                if 'number_max_value' not in metadata or type(metadata['number_max_value']) not in [int, float]:
                    raise serializers.ValidationError('Metadata must contain a valid number_max_value')
                if 'number_min_value' not in metadata or type(metadata['number_min_value']) not in [int, float]:
                    raise serializers.ValidationError('Metadata must contain a valid number_min_value')
                if metadata['number_max_value'] < metadata['number_min_value']:
                    raise serializers.ValidationError('value of number_max_value can not be less than number_min_value')
            case Field.TYPES.TXT_INPUT_EMAIL:
                if 'placeholder' not in metadata or not metadata['placeholder']:
                    raise serializers.ValidationError('Metadata must contain a placeholder like "test@gmail.com"')
            case Field.TYPES.TXT_INPUT_TIME:
                if 'placeholder' not in metadata or not metadata['placeholder']:
                    raise serializers.ValidationError('Metadata must contain a placeholder like "12:34:56"')
            case Field.TYPES.TXT_INPUT_IP:
                if 'placeholder' not in metadata or not metadata['placeholder']:
                    raise serializers.ValidationError('Metadata must contain a placeholder like "192.168.1.1"')
            case Field.TYPES.LONG_TXT_INPUT:
                if 'answer_max_length' not in metadata or metadata['answer_max_length'] < 1 or type(metadata['answer_max_length']) is not int:
                    raise serializers.ValidationError('Metadata must contain a positive integer as answer_max_length')
            case Field.TYPES.NUM_INPUT:
                if 'number_max_value' not in metadata or type(metadata['number_max_value']) not in [int, float]:
                    raise serializers.ValidationError('Metadata must contain a valid number_max_value')
                if 'number_min_value' not in metadata or type(metadata['number_min_value']) not in [int, float]:
                    raise serializers.ValidationError('Metadata must contain a valid number_min_value')
                if metadata['number_max_value'] < metadata['number_min_value']:
                    raise serializers.ValidationError('value of number_max_value can not be less than number_min_value')
            case Field.TYPES.CHOISES_INPUT:
                if 'min_selectable_choices' not in metadata:
                    raise serializers.ValidationError('Metadata must contain a value as min_selectable_choices')
                if 'max_selectable_choices' not in metadata:
                    raise serializers.ValidationError('Metadata must contain a value as max_selectable_choices')
                if metadata['max_selectable_choices'] < metadata['min_selectable_choices']:
                    raise serializers.ValidationError('value of max_selectable_choices can not be less than min_selectable_choices')
                if 'choices' not in metadata:
                    raise serializers.ValidationError('Choices must be defined in metadata as "choices":{"1": "f1"}')

    def create(self, validated_data):
        field = Field.objects.create(**validated_data)
        match field['type']:
            case Field.TYPES.TXT_INPUT_FR:
                field['metadata']['regex_value'] = '^[ء-ی]*$'
            case Field.TYPES.TXT_INPUT_ENG:
                field['metadata']['regex_value'] = '^[a-zA-z]*$'
            case Field.TYPES.TXT_INPUT_NUMBERS:
                field['metadata']['regex_value'] = '^[0-9۰-۹٠-٩]*$'
            case Field.TYPES.TXT_INPUT_EMAIL:
                field['metadata']['regex_value'] = '^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$'
            case Field.TYPES.TXT_INPUT_TIME:
                field['metadata']['regex_value'] = \
                    '^([۰-۱0-1٠-١]?[۰-۹0-9٠-٩]|20|21|22|23|۲۰|۲۱|۲۲|۲۳|٢٠|٢١|٢٢|٢٣):([۰-۵0-5٠-٥]?[۰-۹0-9٠-٩])(:([۰-۵0-5٠-٥]?[۰-۹0-9٠-٩]))?$'
            case Field.TYPES.TXT_INPUT_IP:
                field['metadata']['regex_value'] = \
                    '^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return field


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
