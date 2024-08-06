from django.contrib.auth import get_user_model
from django.db import models

TYPES = {
    "EN_CHAR": {
        "regex_value": "^[a-zA-Z ]*$",
    },
    "FR_CHAR": {},
}


class Field(models.Model):
    class TYPES(models.IntegerChoices):
        TXT_INPUT_FR = (
            1,
            "short input include just persian chars",
        )
        TXT_INPUT_ENG = (
            2,
            "short input include just english chars",
        )
        TXT_INPUT_NUMBERS = (
            3,
            "short input include just numbers",
        )
        TXT_INPUT_EMAIL = (
            4,
            "short input include just a valid email",
        )
        TXT_INPUT_TIME = (
            5,
            "short input include just a valid time like 11:11:11",
        )
        TXT_INPUT_IP = (
            6,
            "short input include just a valid ip like 192.168.1.1",
        )
        LONG_TXT_INPUT = (
            7,
            "long input include a text",
        )
        CHOISES_INPUT = (
            8,
            "choose one or multiple choises",
        )
        NUM_INPUT = (
            9,
            "numeric input",
        )

    metadata = models.JSONField()
    title = models.CharField(max_length=250)
    slug = models.SlugField()
    description_text = models.CharField(max_length=250)
    type = models.PositiveSmallIntegerField(choices=TYPES)
    answer_required = models.BooleanField()
    error_message = models.CharField(max_length=500)
    form = models.ForeignKey(
        to="Form",
        on_delete=models.SET_NULL,
        null=True,
        related_name="fields",
    )


class Form(models.Model):
    metadata = models.JSONField()
    title = models.CharField(max_length=250)
    pipline = models.ForeignKey(
        to="Pipline",
        on_delete=models.SET_NULL,
        null=True,
    )


class Pipline(models.Model):
    metadata = models.JSONField()
    questions_responding_duration = models.PositiveBigIntegerField(
        help_text="Response duration time in minutes"
    )
    start_datetime = models.DateTimeField()
    stop_datetime = models.DateTimeField()
    hide_previous_button = models.BooleanField()
    hide_next_button = models.BooleanField()
    is_private = models.BooleanField()
    password = models.CharField(max_length=50, null=True)
    owner = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
    )
