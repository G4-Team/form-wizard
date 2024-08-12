from rest_framework import serializers

from forms.models import Category, Field, Form, Pipeline
from responses.models import PipelineSubmission

from .utils import get_random_string


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
                if len(metadata["choices"]) < metadata["max_selectable_choices"]:
                    raise serializers.ValidationError(
                        {
                            "metadata": {
                                "choices": "number of choices must greater than equal max_selectable_choices"
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

        for field in attrs["fields"]:
            if field.id not in attrs["metadata"]["order"]:
                raise serializers.ValidationError(
                    f"The {field.id} field is not defined in metadata order"
                )
            if field.owner.id != self.context["request"].user.id:
                raise serializers.ValidationError(
                    {"fields": f"we can't find a field with this id: {field.id}"}
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
            if not Field.objects.filter(
                id=id, owner__id=self.context["request"].user.id
            ).exists():
                raise serializers.ValidationError(
                    {"fields": f"we can't find a field with this id: {id}"}
                )
        keys_to_keep = {
            "order",
        }
        validated_data["metadata"] = {
            k: metadata[k] for k in keys_to_keep if k in metadata
        }
        return super().update(instance, validated_data)


class PipelineSerializer(serializers.ModelSerializer):
    share_link = serializers.SerializerMethodField()

    class Meta:
        model = Pipeline
        fields = "__all__"
        read_only_fields = [
            "owner",
            "slug",
            "share_link",
        ]

    def get_share_link(self, obj: Pipeline):
        return obj.get_absolute_url()

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
        random_slug = get_random_string(length=20)
        while Pipeline.objects.filter(slug=random_slug).exists():
            random_slug = get_random_string(length=20)
        validated_data["slug"] = random_slug
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


class PipelineShowSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    forms = serializers.SerializerMethodField()

    class Meta:
        model = Pipeline
        exclude = ("password",)
        read_only_fields = (
            "id",
            "title",
            "slug",
            "description_text",
            "metadata",
            "questions_responding_duration",
            "start_datetime",
            "stop_datetime",
            "hide_previous_button",
            "hide_next_button",
            "is_private",
            "owner",
            "number_of_views",
            "categories",
        )
        depth = 2

    def get_owner(self, obj: Pipeline):
        return obj.owner.email

    def get_forms(self, obj: Pipeline):
        form_ids = None
        OUTPUT = {}
        if obj.hide_next_button:
            if self.context["request"].user.is_authenticated:
                submission = PipelineSubmission.objects.filter(
                    pipeline__id=obj.id, owner__id=self.context["request"].user.id
                )
                if submission.exists():
                    form_ids = submission[0].responses["responsed_forms"]
                    last_index = obj.metadata["order"].index(form_ids[-1])
                    if len(obj.metadata["order"]) > last_index + 1:
                        form_ids.append(obj.metadata["order"][last_index + 1])
                else:
                    form_ids = obj.metadata["order"][:1]
            else:
                if self.context["request"].session.session_key is None:
                    self.context["request"].session.create()
                session_key = self.context["request"].session.session_key
                submission = PipelineSubmission.objects.filter(
                    pipeline__id=obj.id, session_key=session_key
                )
                if submission.exists():
                    form_ids = submission[0].responses["responsed_forms"]
                    last_index = obj.metadata["order"].index(form_ids[-1])
                    if len(obj.metadata["order"]) > last_index + 1:
                        form_ids.append(obj.metadata["order"][last_index + 1])
                else:
                    form_ids = obj.metadata["order"][:1]
        else:
            form_ids = obj.metadata["order"]

        for form_id in form_ids:
            form: Form = Form.objects.get(pk=form_id)
            OUTPUT[str(form.id)] = {}
            OUTPUT[str(form.id)]["metadata"] = form.metadata
            OUTPUT[str(form.id)]["title"] = form.title

            OUTPUT[str(form.id)]["fields"] = {}
            for field in form.fields.all():
                OUTPUT[str(form.id)]["fields"][str(field.id)] = {}
                OUTPUT[str(form.id)]["fields"][str(field.id)]["title"] = field.title
                OUTPUT[str(form.id)]["fields"][str(field.id)]["slug"] = field.slug
                OUTPUT[str(form.id)]["fields"][str(field.id)][
                    "metadata"
                ] = field.metadata
                OUTPUT[str(form.id)]["fields"][str(field.id)][
                    "description_text"
                ] = field.description_text
                OUTPUT[str(form.id)]["fields"][str(field.id)]["type"] = field.type
                OUTPUT[str(form.id)]["fields"][str(field.id)][
                    "answer_required"
                ] = field.answer_required
                OUTPUT[str(form.id)]["fields"][str(field.id)][
                    "error_message"
                ] = field.error_message
        return OUTPUT


class CategorySerializer(serializers.ModelField):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = [
            "owner",
        ]

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)
