import re

from django.db.models import QuerySet
from django.urls import reverse
from django.utils import timezone
from rest_framework import serializers

from forms.models import Field, Form, Pipeline

from .models import Response
from .utils import get_client_ip


class ResponseWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False)

    class Meta:
        model = Response
        exclude = [
            "created_at",
            "updated_at",
        ]

    def validate_pipeline(self, pipeline: Pipeline):
        now = timezone.make_aware(
            timezone.datetime.now(), timezone.get_default_timezone()
        )

        if pipeline.stop_datetime is not None and now > pipeline.stop_datetime:
            raise serializers.ValidationError("This pipeline has expired.")

        if pipeline.start_datetime is not None and now < pipeline.start_datetime:
            raise serializers.ValidationError(
                f"The pipeline has not started yet. It will start at {pipeline.start_datetime}."
            )
        return pipeline

    def validate(self, attrs):

        pipeline: Pipeline = attrs["pipeline"]
        if pipeline.is_private:
            if "password" not in attrs:
                raise serializers.ValidationError(
                    {
                        "password": "The pipeline is protected. so, This field is required"
                    }
                )

            password = attrs["password"]
            if password != pipeline.password:
                raise serializers.ValidationError(
                    {"password": "password is incorrect."}
                )

            attrs.pop("password")

        form: Form = attrs["form"]
        if pipeline.hide_next_button:
            index_form = pipeline.metadata["order"].index(form.id)

            if self.context["request"].user.is_authenticated:
                if index_form != 0:
                    previous_form_id = pipeline.metadata["order"][index_form - 1]
                    if not Response.objects.filter(
                        form__id=previous_form_id,
                        pipeline__id=pipeline.id,
                        owner__id=self.context["request"].user.id,
                    ).exists():
                        raise serializers.ValidationError(
                            f"You should first answer to previous form with id: {previous_form_id}"
                        )
            else:
                if index_form != 0:
                    previous_form_id = pipeline.metadata["order"][index_form - 1]
                    if not Response.objects.filter(
                        form__id=previous_form_id,
                        pipeline__id=pipeline.id,
                        ip=get_client_ip(self.context["request"]),
                    ).exists():
                        raise serializers.ValidationError(
                            f"You should first answer to previous form with id: {previous_form_id}"
                        )

        fields: QuerySet[Field] = form.fields.all()
        data = attrs["data"]

        for field in fields:
            if field.answer_required:
                if str(field.id) not in data.keys():
                    raise serializers.ValidationError(
                        {
                            "data": {field.slug: "This field is required."},
                        }
                    )

                if field.type == Field.TYPES.CHOISES_INPUT:
                    minimum = field.metadata["min_selectable_choices"]
                    maximum = field.metadata["max_selectable_choices"]
                    values = data[str(field.id)]
                    if not isinstance(values, list):
                        raise serializers.ValidationError(
                            {
                                "data": {field.slug: "The answer should be a list."},
                            }
                        )
                    if len(values) < minimum or len(values) > maximum:
                        raise serializers.ValidationError(
                            {
                                "data": {
                                    field.slug: f"The number of answers should be more than {minimum} and less than {maximum}."
                                },
                            }
                        )
                    for e in values:
                        if str(e) not in field.metadata["choices"].keys():
                            raise serializers.ValidationError(
                                {
                                    "data": {field.slug: f"{e} is not a valid choice."},
                                }
                            )
                else:
                    value = data[str(field.id)]
                    if not re.match(field.metadata["regex_value"], str(value)):
                        raise serializers.ValidationError(
                            {
                                "data": {field.slug: field.error_message},
                            }
                        )

        return attrs

    def create(self, validated_data):
        if self.context["request"].user.is_authenticated:
            validated_data["owner"] = self.context["request"].user
        else:
            validated_data["ip"] = get_client_ip(request=self.context["request"])

        return super().create(validated_data)
