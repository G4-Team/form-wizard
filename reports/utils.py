from django.core.mail import send_mail
from django.db.models import Avg, Max, Min
from django.db.models.fields.json import KT

from forms.models import Field, Form, Pipeline
from responses.models import PipelineSubmission, Response


def create_new_report(pipeline: Pipeline) -> dict:
    output = {}

    TOTAL_RESPONSES = PipelineSubmission.objects.filter(
        pipeline__id=pipeline.id
    ).count()
    pipeline_submission = PipelineSubmission.objects.filter(
        pipeline__id=pipeline.id, is_completed=True
    )
    COMPLETE_RESPONSES = PipelineSubmission.objects.filter(
        pipeline__id=pipeline.id, is_completed=True
    ).count()
    VISITED = pipeline.number_of_views

    output["total_responses"] = TOTAL_RESPONSES
    output["complete_responses"] = COMPLETE_RESPONSES
    output["number_of_visit"] = VISITED

    RESPNSES = {}

    for form_id in pipeline.metadata["order"]:
        form = Form.objects.get(pk=form_id)
        RESPNSES[form.title] = {}

        for field in form.fields.all():
            if field.type == Field.TYPES.NUM_INPUT:
                annotation = {}
                annotation[f"field_{field.id}"] = KT(f"data__{field.slug}")
                RESPNSES[form.title][field.slug] = {}
                agg = (
                    Response.objects.annotate(**annotation)
                    .filter(
                        pipeline__id=pipeline.id,
                        form__id=form.id,
                        pipeline_submission__is_completed=True,
                    )
                    .aggregate(
                        avg=Avg(f"field_{field.id}"),
                        max=Max(f"field_{field.id}"),
                        min=Min(f"field_{field.id}"),
                    )
                )
                RESPNSES[form.title][field.slug]["average"] = agg["avg"]
                RESPNSES[form.title][field.slug]["maximum_value"] = agg["max"]
                RESPNSES[form.title][field.slug]["minimum_value"] = agg["min"]
            elif field.type == Field.TYPES.CHOISES_INPUT:
                RESPNSES[form.title][field.slug] = {}
                annotation = {}
                annotation[f"field_{field.id}"] = KT(f"data__{field.slug}")
                perc = {}
                for id, value in field.metadata["choices"].items():
                    filter = {f"field_{field.id}__icontains": int(id)}
                    perc[value] = (
                        Response.objects.annotate(**annotation)
                        .filter(
                            pipeline__id=pipeline.id,
                            form__id=form.id,
                            pipeline_submission__is_completed=True,
                            **filter,
                        )
                        .count()
                    )

                for key, value in perc.items():
                    if COMPLETE_RESPONSES != 0:
                        RESPNSES[form.title][field.slug][
                            key
                        ] = f"{value*100/COMPLETE_RESPONSES}%"
                    else:
                        RESPNSES[form.title][field.slug][key] = "0%"

    output["responses"] = RESPNSES

    return output


async def acreate_new_report(pipeline: Pipeline) -> dict:
    output = {}

    TOTAL_RESPONSES = await PipelineSubmission.objects.filter(
        pipeline__id=pipeline.id
    ).acount()
    COMPLETE_RESPONSES = await PipelineSubmission.objects.filter(
        pipeline__id=pipeline.id, is_completed=True
    ).acount()
    VISITED = pipeline.number_of_views

    output["total_responses"] = TOTAL_RESPONSES
    output["complete_responses"] = COMPLETE_RESPONSES
    output["number_of_visit"] = VISITED

    RESPNSES = {}

    for form_id in pipeline.metadata["order"]:
        form = await Form.objects.aget(pk=form_id)
        RESPNSES[form.title] = {}

        async for field in form.fields.all():
            if field.type == Field.TYPES.NUM_INPUT:
                annotation = {}
                annotation[f"field_{field.id}"] = KT(f"data__{field.slug}")
                RESPNSES[form.title][field.slug] = {}
                agg = await (
                    await Response.objects.annotate(**annotation)
                    .filter(
                        pipeline__id=pipeline.id,
                        form__id=form.id,
                        pipeline_submission__is_completed=True,
                    )
                    .aaggregate(
                        avg=Avg(f"field_{field.id}"),
                        max=Max(f"field_{field.id}"),
                        min=Min(f"field_{field.id}"),
                    )
                )
                RESPNSES[form.title][field.slug]["average"] = agg["avg"]
                RESPNSES[form.title][field.slug]["maximum_value"] = agg["max"]
                RESPNSES[form.title][field.slug]["minimum_value"] = agg["min"]
            elif field.type == Field.TYPES.CHOISES_INPUT:
                RESPNSES[form.title][field.slug] = {}
                annotation = {}
                annotation[f"field_{field.id}"] = KT(f"data__{field.slug}")
                perc = {}
                for id, value in field.metadata["choices"].items():
                    filter = {f"field_{field.id}__icontains": int(id)}
                    perc[value] = (
                        await Response.objects.annotate(**annotation)
                        .filter(
                            pipeline__id=pipeline.id,
                            form__id=form.id,
                            pipeline_submission__is_completed=True,
                            **filter,
                        )
                        .acount()
                    )

                for key, value in perc.items():
                    if COMPLETE_RESPONSES != 0:
                        RESPNSES[form.title][field.slug][
                            key
                        ] = f"{value*100/COMPLETE_RESPONSES}%"
                    else:
                        RESPNSES[form.title][field.slug][key] = "0%"

    output["responses"] = RESPNSES

    return output


def send_email(subject: str, message: str, receiver: str):
    subject = subject
    message = message
    sender = "dctrxspprt@gmail.com"
    receiver = receiver
    send_mail(
        subject,
        message,
        sender,
        receiver,
        fail_silently=False,
    )
