from rest_framework import serializers

from forms.models import Field, Form, Pipeline


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = "__all__"
        read_only_fields = [
            "owner",
        ]

    def validate_type(self, value):
        if value < 1 or value > 4:
            raise serializers.ValidationError("Type must be an integer from 1 to 4")
        return value

    def validate(self, data):
        field_type = data.get("type")
        metadata = data.get("metadata")

        match field_type:
            case Field.TYPES.SHORT_TXT_INPUT:
                if (
                    "placeholder" not in metadata
                    or not isinstance(metadata["placeholder"], str)
                    or not metadata["placeholder"]
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "placeholder": 'Metadata must contain a [str] placeholder like "only persian"'
                            }
                        }
                    )
                if (
                    "answer_max_length" not in metadata
                    or not isinstance(metadata["answer_max_length"], int)
                    or metadata["answer_max_length"] < 1
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "answer_min_length": "Metadata must contain a [int] answer_max_length more than 0"
                            }
                        }
                    )
                if (
                    "answer_min_length" not in metadata
                    or not isinstance(metadata["answer_min_length"], int)
                    or metadata["answer_min_length"] < 0
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "answer_min_length": "Metadata must contain a non negative [int] answer_min_length"
                            }
                        }
                    )
                if metadata["answer_max_length"] < metadata["answer_min_length"]:
                    raise serializers.ValidationError(
                        {
                            "metadata": "value of answer_max_length can not be less than answer_min_length"
                        }
                    )
                if (
                    "regex_value" not in metadata
                    or not isinstance(metadata["regex_value"], str)
                    or not metadata["regex_value"]
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "regex_value": "Metadata must contain a [str] regex validation"
                            }
                        }
                    )
                keys_to_keep = {
                    "placeholder",
                    "answer_max_length",
                    "answer_min_length",
                    "regex_value",
                }
                filtered_dict = {k: metadata[k] for k in keys_to_keep if k in metadata}
                data["metadata"] = filtered_dict
            case Field.TYPES.LONG_TXT_INPUT:
                if (
                    "answer_max_length" not in metadata
                    or not isinstance(metadata["answer_max_length"], int)
                    or metadata["answer_max_length"] < 1
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "answer_min_length": "Metadata must contain a [int] answer_max_length more than 0"
                            }
                        }
                    )
                if (
                    "answer_min_length" not in metadata
                    or not isinstance(metadata["answer_min_length"], int)
                    or metadata["answer_min_length"] < 0
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "answer_min_length": "Metadata must contain a non negative [int] answer_min_length"
                            }
                        }
                    )
                if metadata["answer_max_length"] < metadata["answer_min_length"]:
                    raise serializers.ValidationError(
                        {
                            "metadata": "value of answer_max_length can not be less than answer_min_length"
                        }
                    )
                keys_to_keep = {
                    "answer_max_length",
                    "answer_min_length",
                }
                filtered_dict = {k: metadata[k] for k in keys_to_keep if k in metadata}
                data["metadata"] = filtered_dict
            case Field.TYPES.NUM_INPUT:
                if "number_max_value" not in metadata or not isinstance(
                    metadata["number_max_value"], (int, float)
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "number_max_value": "Metadata must contain a valid [int, float] number_max_value"
                            }
                        }
                    )
                if "number_min_value" not in metadata or not isinstance(
                    metadata["number_min_value"], (int, float)
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "number_min_value": "Metadata must contain a valid [int, float] number_min_value"
                            }
                        }
                    )
                if metadata["number_max_value"] < metadata["number_min_value"]:
                    raise serializers.ValidationError(
                        {
                            "metadata": "value of number_max_value can not be less than number_min_value"
                        }
                    )
                keys_to_keep = {
                    "number_max_value",
                    "number_min_value",
                }
                filtered_dict = {k: metadata[k] for k in keys_to_keep if k in metadata}
                data["metadata"] = filtered_dict
            case Field.TYPES.CHOISES_INPUT:
                if "min_selectable_choices" not in metadata or not isinstance(
                    metadata["min_selectable_choices"], int
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "min_selectable_choices": "Metadata must contain a [int] value as min_selectable_choices"
                            }
                        }
                    )
                if "max_selectable_choices" not in metadata or not isinstance(
                    metadata["max_selectable_choices"], int
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "max_selectable_choices": "Metadata must contain a [int] value as max_selectable_choices"
                            }
                        }
                    )
                if (
                    metadata["max_selectable_choices"]
                    < metadata["min_selectable_choices"]
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": "value of max_selectable_choices can not be less than min_selectable_choices"
                        }
                    )
                if (
                    "choices" not in metadata
                    or not isinstance(metadata["choices"], dict)
                    or len(metadata["choices"]) == 0
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "choices": 'Choices must be defined in metadata as "choices":{"1": "f1"}'
                            }
                        }
                    )
                keys_to_keep = {
                    "min_selectable_choices",
                    "max_selectable_choices",
                    "choices",
                }
                filtered_dict = {k: metadata[k] for k in keys_to_keep if k in metadata}
                data["metadata"] = filtered_dict
        return super().validate(data)

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class UpdateFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = "__all__"
        read_only_fields = [
            "owner",
        ]

    def update(self, instance: Field, validated_data):
        field_type = validated_data.get("type", instance.type)
        metadata = validated_data.get("metadata", instance.metadata)
        match field_type:
            case Field.TYPES.SHORT_TXT_INPUT:
                if (
                    "placeholder" not in metadata
                    or not isinstance(metadata["placeholder"], str)
                    or not metadata["placeholder"]
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "placeholder": 'Metadata must contain a [str] placeholder like "only persian"'
                            }
                        }
                    )
                if (
                    "answer_max_length" not in metadata
                    or not isinstance(metadata["answer_max_length"], int)
                    or metadata["answer_max_length"] < 1
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "answer_min_length": "Metadata must contain a [int] answer_max_length more than 0"
                            }
                        }
                    )
                if (
                    "answer_min_length" not in metadata
                    or not isinstance(metadata["answer_min_length"], int)
                    or metadata["answer_min_length"] < 0
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "answer_min_length": "Metadata must contain a non negative [int] answer_min_length"
                            }
                        }
                    )
                if metadata["answer_max_length"] < metadata["answer_min_length"]:
                    raise serializers.ValidationError(
                        {
                            "metadata": "value of answer_max_length can not be less than answer_min_length"
                        }
                    )
                if (
                    "regex_value" not in metadata
                    or not isinstance(metadata["regex_value"], str)
                    or not metadata["regex_value"]
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "regex_value": "Metadata must contain a [str] regex validation"
                            }
                        }
                    )
                keys_to_keep = {
                    "placeholder",
                    "answer_max_length",
                    "answer_min_length",
                    "regex_value",
                }
                filtered_dict = {k: metadata[k] for k in keys_to_keep if k in metadata}
                validated_data["metadata"] = filtered_dict
            case Field.TYPES.LONG_TXT_INPUT:
                if (
                    "answer_max_length" not in metadata
                    or not isinstance(metadata["answer_max_length"], int)
                    or metadata["answer_max_length"] < 1
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "answer_min_length": "Metadata must contain a [int] answer_max_length more than 0"
                            }
                        }
                    )
                if (
                    "answer_min_length" not in metadata
                    or not isinstance(metadata["answer_min_length"], int)
                    or metadata["answer_min_length"] < 0
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "answer_min_length": "Metadata must contain a non negative [int] answer_min_length"
                            }
                        }
                    )
                if metadata["answer_max_length"] < metadata["answer_min_length"]:
                    raise serializers.ValidationError(
                        {
                            "metadata": "value of answer_max_length can not be less than answer_min_length"
                        }
                    )
                keys_to_keep = {
                    "answer_max_length",
                    "answer_min_length",
                }
                filtered_dict = {k: metadata[k] for k in keys_to_keep if k in metadata}
                validated_data["metadata"] = filtered_dict
            case Field.TYPES.NUM_INPUT:
                if "number_max_value" not in metadata or not isinstance(
                    metadata["number_max_value"], (int, float)
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "number_max_value": "Metadata must contain a valid [int, float] number_max_value"
                            }
                        }
                    )
                if "number_min_value" not in metadata or not isinstance(
                    metadata["number_min_value"], (int, float)
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "number_min_value": "Metadata must contain a valid [int, float] number_min_value"
                            }
                        }
                    )
                if metadata["number_max_value"] < metadata["number_min_value"]:
                    raise serializers.ValidationError(
                        {
                            "metadata": "value of number_max_value can not be less than number_min_value"
                        }
                    )
                keys_to_keep = {
                    "number_max_value",
                    "number_min_value",
                }
                filtered_dict = {k: metadata[k] for k in keys_to_keep if k in metadata}
                validated_data["metadata"] = filtered_dict
            case Field.TYPES.CHOISES_INPUT:
                if "min_selectable_choices" not in metadata or not isinstance(
                    metadata["min_selectable_choices"], int
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "min_selectable_choices": "Metadata must contain a [int] value as min_selectable_choices"
                            }
                        }
                    )
                if "max_selectable_choices" not in metadata or not isinstance(
                    metadata["max_selectable_choices"], int
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "max_selectable_choices": "Metadata must contain a [int] value as max_selectable_choices"
                            }
                        }
                    )
                if (
                    metadata["max_selectable_choices"]
                    < metadata["min_selectable_choices"]
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": "value of max_selectable_choices can not be less than min_selectable_choices"
                        }
                    )
                if (
                    "choices" not in metadata
                    or not isinstance(metadata["choices"], dict)
                    or len(metadata["choices"]) == 0
                ):
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "choices": 'Choices must be defined in metadata as "choices":{"1": "f1"}'
                            }
                        }
                    )
                keys_to_keep = {
                    "min_selectable_choices",
                    "max_selectable_choices",
                    "choices",
                }
                filtered_dict = {k: metadata[k] for k in keys_to_keep if k in metadata}
                validated_data["metadata"] = filtered_dict

        return super().update(instance, validated_data)


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = "__all__"
        read_only_fields = [
            "owner",
        ]

    def validate(self, attrs):
        if "order" not in attrs["metadata"] or not isinstance(
            attrs["metadata"]["order"], list
        ):
            raise serializers.ValidationError(
                {
                    "metadata": {
                        "order": "Order must be defined in metadata [as a list]."
                    }
                }
            )
        if "fields" not in attrs:
            raise serializers.ValidationError({"fields": "This field is required."})
        if len(attrs["metadata"]["order"]) != len(attrs["fields"]):
            raise serializers.ValidationError(
                "Order must have the same number of fields"
            )

        for field_id in attrs["fields"]:
            if field_id not in attrs["metadata"]["order"]:
                raise serializers.ValidationError(
                    f"The {field_id} field is not defined in metadata order"
                )
        keys_to_keep = {
            "order",
        }
        filtered_dict = {
            k: attrs["metadata"][k] for k in keys_to_keep if k in attrs["metadata"]
        }
        attrs["metadata"] = filtered_dict
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class UpdateFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = "__all__"
        read_only_fields = [
            "owner",
        ]

    def update(self, instance: Form, validated_data):
        metadata = validated_data.get("metadata", instance.metadata)
        fields = validated_data.get("fields", instance.fields.all())
        if "order" not in metadata or not isinstance(metadata["order"], list):
            raise serializers.ValidationError(
                {
                    "metadata": {
                        "order": "Order must be defined in metadata [as a list]."
                    }
                }
            )

        if len(metadata["order"]) != len(fields):
            raise serializers.ValidationError(
                "Order must have the same number of fields"
            )

        for field in fields:
            id = field.id if isinstance(field, Field) else field
            if id not in metadata["order"]:
                raise serializers.ValidationError(
                    f"The {id} field is not defined in metadata order"
                )
        keys_to_keep = {
            "order",
        }
        validated_data["metadata"] = {
            k: metadata[k] for k in keys_to_keep if k in metadata
        }
        return super().update(instance, validated_data)


# class FormSerializer(serializers.ModelSerializer):
#     fields = FieldSerializer(many=True, read_only=True)

#     class Meta:
#         model = Form
#         fields = "__all__"
#         read_only_fields = [
#             "owner",
#         ]

#     def validate(self, data):
#         metadata = data["metadata"]
#         if not self.instance:  # creation mode
#             if "order" not in metadata or not isinstance(metadata["order"], list):
#                 raise serializers.ValidationError(
#                     {
#                         "metadata": {
#                             "order": "Order must be defined in metadata [as a list]."
#                         }
#                     }
#                 )
#             elif len(metadata["order"]) != len(self.initial_data["fields"]):
#                 raise serializers.ValidationError(
#                     "Order must have the same number of fields"
#                 )
#             else:
#                 fields_id = self.initial_data["fields"]
#                 for field_id in fields_id:
#                     if field_id not in metadata["order"]:
#                         raise serializers.ValidationError(
#                             f"The {field_id} field is not defined in metadata order"
#                         )
#         elif "fields" in self.initial_data:  # updating fields
#             if "fields_update_mode" not in metadata or metadata[
#                 "fields_update_mode"
#             ] not in ["add", "remove"]:
#                 raise serializers.ValidationError(
#                     'Metadata must contain field_update_mode as "add"/"remove"'
#                 )
#             elif metadata["fields_update_mode"] == "add":
#                 if "order" not in metadata:
#                     raise serializers.ValidationError(
#                         "Order must be defined in metadata"
#                     )
#                 elif len(metadata["order"]) != len(self.initial_data["fields"]) + len(
#                     self.instance.metadata["order"]
#                 ):
#                     raise serializers.ValidationError(
#                         "number of adding fields does not match with the number of fields given in order"
#                     )
#                 else:
#                     fields_id = self.initial_data["fields"]
#                     for field_id in fields_id:
#                         if field_id not in metadata["order"]:
#                             raise serializers.ValidationError(
#                                 f"The {field_id} field is not defined in metadata order"
#                             )
#                         else:
#                             field = Field.objects.get(id=field_id)
#                             if field in self.instance.fields:
#                                 raise serializers.ValidationError(
#                                     "This field is already in use"
#                                 )
#             else:  # metadata['fields_update_mode'] == 'remove'
#                 if "order" in metadata:
#                     if len(metadata["order"]) != len(
#                         self.instance.metadata["order"]
#                     ) - len(self.initial_data["fields"]):
#                         raise serializers.ValidationError(
#                             "number of removing fields does not match with the number of fields given in order"
#                         )
#                     else:
#                         for field_id in metadata["order"]:
#                             if field_id not in self.instance.metadata["order"]:
#                                 raise serializers.ValidationError(
#                                     "The given order does not match with the remaining fields"
#                                 )
#                 else:
#                     for field_id in self.initial_data["fields"]:
#                         if field_id not in self.instance.metadata["order"]:
#                             raise serializers.ValidationError(
#                                 f"The given field {field_id} does not exist in fields"
#                             )
#         return data

#     def create(self, validated_data):
#         form = Form.objects.create(**validated_data)
#         fields_id = self.initial_data["fields"]
#         field_instances = []
#         for field_id in fields_id:
#             field_instances.append(Field.objects.get(pk=field_id))
#         form.fields.set(field_instances)
#         return form

#     def update(self, instance, validated_data):
#         metadata = validated_data.pop("metadata")
#         instance = super(FormSerializer, self).update(instance, validated_data)
#         fields_id = self.initial_data.get("fields", None)
#         if fields_id:
#             mode = metadata.pop("fields_update_mode")
#             if mode == "remove":
#                 for field_id in fields_id:
#                     field = Field.objects.get(pk=field_id)
#                     instance.fields.remove(field)
#                     instance.metadata["order"].remove(field_id)
#             elif mode == "add":
#                 for field_id in fields_id:
#                     field = Field.objects.get(pk=field_id)
#                     instance.fields.add(field)
#                 instance.metadata["order"] = metadata["order"]
#         instance.save()
#         return instance


class PipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipeline
        fields = "__all__"
        read_only_fields = [
            "owner",
        ]

    def validate(self, attrs):
        if "is_private" in attrs and attrs["is_private"] is True:
            if "password" not in attrs:
                raise serializers.ValidationError(
                    {"password": "This field is required"}
                )
        return super().validate(attrs)

    def validate_metadata(self, metadata):
        if "order" not in metadata or not isinstance(metadata["order"], list):
            raise serializers.ValidationError(
                {
                    "metadata": {
                        "order": "Order must be defined in metadata [as a list]."
                    }
                }
            )
        for id in metadata["order"]:
            if not Form.objects.filter(
                id=id, owner__id=self.context["request"].user.id
            ).exists():
                raise serializers.ValidationError(
                    {"metadata": {"order": f"we can't find a form with this id: {id}"}}
                )
        keys_to_keep = {
            "order",
        }
        filtered_dict = {k: metadata[k] for k in keys_to_keep if k in metadata}
        return filtered_dict

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance: Pipeline, validated_data):
        metadata = validated_data.get("metadata", instance.metadata)
        if "order" not in metadata or not isinstance(metadata["order"], list):
            raise serializers.ValidationError(
                {
                    "metadata": {
                        "order": "Order must be defined in metadata [as a list]."
                    }
                }
            )
        for id in metadata["order"]:
            if not Form.objects.filter(
                id=id, owner__id=self.context["request"].user.id
            ).exists():
                raise serializers.ValidationError(
                    {"metadata": {"order": f"we can't find a form with this id: {id}"}}
                )
        keys_to_keep = {
            "order",
        }
        validated_data["metadata"] = {
            k: metadata[k] for k in keys_to_keep if k in metadata
        }
        return super().update(instance, validated_data)
