import re

from django.db.models import QuerySet
from django.urls import reverse
from django.utils import timezone
from rest_framework import serializers

from forms.models import Field, Form, Pipeline

from .models import PipelineSubmission, Response
from .utils import get_client_ip


class ResponseWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False)

    class Meta:
        model = Response
        exclude = [
            "created_at",
            "updated_at",
            "session_key",
            "owner",
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
        if self.context["request"].session.session_key is None:
            self.context["request"].session.create()
        session_key = self.context["request"].session.session_key

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
        if form.id not in pipeline.metadata["order"]:
            raise serializers.ValidationError(
                {"error": "This form not belong to this pipeline"}
            )
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
                        session_key=session_key,
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
            resp = data.get(str(field.id), None)
            if resp is not None:
                ResponseWriteSerializer.field_validation(
                    field=field,
                    response=resp,
                )
        ids = [id[0] for id in fields.values_list("id")]
        for id in list(data):
            if int(id) not in ids:
                data.pop(id)

        return attrs

    def create(self, validated_data):
        if self.context["request"].user.is_authenticated:
            pipeline: Pipeline = validated_data["pipeline"]
            form: Form = validated_data["form"]
            if Response.objects.filter(
                form__id=form.id,
                pipeline__id=pipeline.id,
                owner__id=self.context["request"].user.id,
            ).exists():
                response = Response.objects.only("id").get(
                    form__id=form.id,
                    pipeline__id=pipeline.id,
                    owner__id=self.context["request"].user.id,
                )
                raise serializers.ValidationError(
                    {
                        "message": f"You responsed to this form befor, if you want to change your response, use url below",
                        "url": f'{reverse("api:responses:update-response", kwargs={"response_id":response.id})}',
                    }
                )

            pipeline_submission, created = PipelineSubmission.objects.get_or_create(
                pipeline=pipeline, owner=self.context["request"].user
            )
            if created:
                responsed_forms_list: list = pipeline_submission.responses[
                    "responsed_forms"
                ]
                responsed_forms_list.append(form.id)
                pipeline_submission.responses["responsed_forms"] = responsed_forms_list
                pipeline_submission.save()
            else:
                now = timezone.make_aware(
                    timezone.datetime.now(), timezone.get_default_timezone()
                )
                duration = (now - pipeline_submission.created_at).total_seconds() / 60
                if pipeline.questions_responding_duration < duration:
                    raise serializers.ValidationError(
                        {"message": "Response time has expired."}
                    )
                responsed_forms_list: list = pipeline_submission.responses[
                    "responsed_forms"
                ]
                responsed_forms_list.append(form.id)
                pipeline_submission.responses["responsed_forms"] = responsed_forms_list
                pipeline_submission.save()
            if len(pipeline.metadata["order"]) == len(
                pipeline_submission.responses["responsed_forms"]
            ):
                pipeline_submission.is_completed = True
                pipeline_submission.save()
            validated_data["owner"] = self.context["request"].user
        else:
            pipeline: Pipeline = validated_data["pipeline"]
            form: Form = validated_data["form"]
            if Response.objects.filter(
                form__id=form.id,
                pipeline__id=pipeline.id,
                session_key=self.context["request"].session.session_key,
            ).exists():
                response = Response.objects.only("id").get(
                    form__id=form.id,
                    pipeline__id=pipeline.id,
                    session_key=self.context["request"].session.session_key,
                )
                raise serializers.ValidationError(
                    {
                        "message": f"You responsed to this form befor, if you want to change your response, use url below",
                        "url": f'{reverse("api:responses:update-response", kwargs={"response_id":response.id})}',
                    }
                )

            pipeline_submission, created = PipelineSubmission.objects.get_or_create(
                pipeline=pipeline,
                session_key=self.context["request"].session.session_key,
            )
            if created:
                responsed_forms_list: list = pipeline_submission.responses[
                    "responsed_forms"
                ]
                responsed_forms_list.append(form.id)
                pipeline_submission.responses["responsed_forms"] = responsed_forms_list
                pipeline_submission.save()
            else:
                now = timezone.make_aware(
                    timezone.datetime.now(), timezone.get_default_timezone()
                )
                duration = (now - pipeline_submission.created_at).total_seconds() / 60
                if pipeline.questions_responding_duration < duration:
                    raise serializers.ValidationError(
                        {"message": "Response time has expired."}
                    )
                responsed_forms_list: list = pipeline_submission.responses[
                    "responsed_forms"
                ]
                responsed_forms_list.append(form.id)
                pipeline_submission.responses["responsed_forms"] = responsed_forms_list
                pipeline_submission.save()
            if len(pipeline.metadata["order"]) == len(
                pipeline_submission.responses["responsed_forms"]
            ):
                pipeline_submission.is_completed = True
                pipeline_submission.save()
            validated_data["session_key"] = self.context["request"].session.session_key

        return super().create(validated_data)

    @staticmethod
    def field_validation(field: Field, response):
        match field.type:
            case Field.TYPES.CHOISES_INPUT:
                minimum = field.metadata["min_selectable_choices"]
                maximum = field.metadata["max_selectable_choices"]
                if not isinstance(response, list):
                    raise serializers.ValidationError(
                        {
                            "data": {field.slug: "The answer should be a list."},
                        }
                    )
                if len(response) < minimum or len(response) > maximum:
                    raise serializers.ValidationError(
                        {
                            "data": {
                                field.slug: f"The number of answers should be more than {minimum} and less than {maximum}."
                            },
                        }
                    )
                for e in response:
                    if str(e) not in field.metadata["choices"].keys():
                        raise serializers.ValidationError(
                            {
                                "data": {field.slug: f"{e} is not a valid choice."},
                            }
                        )
            case Field.TYPES.NUM_INPUT:
                if not isinstance(response, (int, float)):
                    raise serializers.ValidationError(
                        {
                            "data": {
                                field.slug: "The answer should be a number(float or int)."
                            },
                        }
                    )
                number_max_value = field.metadata["number_max_value"]
                if response > number_max_value:
                    raise serializers.ValidationError(
                        {
                            "data": {
                                field.slug: f"The answer should less than {number_max_value}."
                            },
                        }
                    )
                number_min_value = field.metadata["number_min_value"]
                if response < number_min_value:
                    raise serializers.ValidationError(
                        {
                            "data": {
                                field.slug: f"The answer should greater than {number_min_value}."
                            },
                        }
                    )
            case Field.TYPES.LONG_TXT_INPUT:
                if not isinstance(response, str):
                    raise serializers.ValidationError(
                        {
                            "data": {field.slug: "The answer should be a string."},
                        }
                    )
                answer_max_length = field.metadata["answer_max_length"]
                if len(response) > answer_max_length:
                    raise serializers.ValidationError(
                        {
                            "data": {
                                field.slug: f"The answer should less than {answer_max_length} char."
                            },
                        }
                    )
                answer_min_length = field.metadata["answer_min_length"]
                if len(response) < answer_min_length:
                    raise serializers.ValidationError(
                        {
                            "data": {
                                field.slug: f"The answer should more than {answer_min_length} char."
                            },
                        }
                    )
            case Field.TYPES.SHORT_TXT_INPUT:
                if not isinstance(response, str):
                    raise serializers.ValidationError(
                        {
                            "data": {field.slug: "The answer should be a string."},
                        }
                    )
                answer_max_length = field.metadata["answer_max_length"]
                if len(response) > answer_max_length:
                    raise serializers.ValidationError(
                        {
                            "data": {
                                field.slug: f"The answer should less than {answer_max_length} char."
                            },
                        }
                    )
                answer_min_length = field.metadata["answer_min_length"]
                if len(response) < answer_min_length:
                    raise serializers.ValidationError(
                        {
                            "data": {
                                field.slug: f"The answer should more than {answer_min_length} char."
                            },
                        }
                    )
                regex_value = field.metadata["regex_value"]
                if not re.match(regex_value, response):
                    raise serializers.ValidationError(
                        {
                            "data": {field.slug: field.error_message},
                        }
                    )


class ResponseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = [
            "data",
        ]

    def validate(self, attrs):
        if self.context["request"].session.session_key is None:
            self.context["request"].session.create()
        if "data" not in attrs:
            raise serializers.ValidationError({"data": "This field is required."})
        return super().validate(attrs)

    def update(self, instance, validated_data):
        pipeline: Pipeline = instance.pipeline
        if self.context["request"].user.is_authenticated:
            if (
                instance.owner != self.context["request"].user
                and instance.session_key != self.context["request"].session.session_key
            ):
                error = serializers.ValidationError(
                    {
                        "permission-denied": "You can't change this response! because you are not owner."
                    }
                )
                error.status_code = 403
                raise error
        else:
            if instance.session_key != self.context["request"].session.session_key:
                error = serializers.ValidationError(
                    {
                        "permission-denied": "You can't change this response! because you are not owner."
                    }
                )
                error.status_code = 403
                raise error

        if pipeline.hide_previous_button:
            raise serializers.ValidationError(
                {
                    "update-error": "This pipeline set as an unchangeble pipeline and you can't change your response!"
                }
            )
        fields: QuerySet[Field] = instance.form.fields.all()
        update_validated_data = validated_data["data"]
        for field in fields:
            if field.answer_required:
                if str(field.id) not in update_validated_data.keys():
                    raise serializers.ValidationError(
                        {
                            "data": {field.slug: "This field is required."},
                        }
                    )
            resp = update_validated_data.get(str(field.id), None)
            if resp is not None:
                ResponseWriteSerializer.field_validation(
                    field=field,
                    response=resp,
                )

        return super().update(instance, validated_data)


class ReadResponseSerializer(serializers.BaseSerializer):
    def to_representation(self, instance: Response):
        rep = {
            "data": instance.data,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
        }
        if instance.owner is not None:
            rep["owner"] = instance.owner.email
        return rep


class PipelineSubmissionSerializer(serializers.ModelSerializer):
    responses = serializers.SerializerMethodField()

    class Meta:
        model = PipelineSubmission
        fields = "__all__"

    def get_responses(self, obj: PipelineSubmission):
        resp = {}

        for id in obj.responses["responsed_forms"]:
            response = Response.objects.get(pipeline__id=obj.pipeline.id, form__id=id)
            resp[f"form-{id}"] = ReadResponseSerializer(instance=response).data

        return resp
