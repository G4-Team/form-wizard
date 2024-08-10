from django.contrib.auth import get_user_model
from django.db import models

COMMON_REGEX_TYPES = {
    "english characters": "^[a-zA-Z ]*$",
    "persian characters": "^[‌ ء-ی]*$",
    "numbers": "^[0-9۰-۹٠-٩]*$",
    "email": "^[a-zA-Z0-9_.±]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$",
    "time": "^([۰-۱0-1٠-١]?[۰-۹0-9٠-٩]|20|21|22|23|۲۰|۲۱|۲۲|۲۳|٢٠|٢١|٢٢|٢٣):([۰-۵0-5٠-٥]?[۰-۹0-9٠-٩])(:([۰-۵0-5٠-٥]?[۰-۹0-9٠-٩]))?$",
    "ip": "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
}


class Field(models.Model):
    class TYPES(models.IntegerChoices):
        SHORT_TXT_INPUT = (
            1,
            "short input include a text",
        )
        LONG_TXT_INPUT = (
            2,
            "long input include a text",
        )
        CHOISES_INPUT = (
            3,
            "choose one or multiple choises",
        )
        NUM_INPUT = (
            4,
            "numeric input",
        )

    metadata = models.JSONField()
    title = models.CharField(max_length=250)
    slug = models.SlugField()
    description_text = models.CharField(max_length=250)
    type = models.PositiveSmallIntegerField(choices=TYPES)
    answer_required = models.BooleanField()
    error_message = models.CharField(max_length=500)
    owner = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
    )


class Form(models.Model):
    metadata = models.JSONField()
    title = models.CharField(max_length=250)
    fields = models.ManyToManyField(Field, related_name="forms", blank=True)
    owner = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
    )


class Pipeline(models.Model):
    metadata = models.JSONField()
    questions_responding_duration = models.PositiveBigIntegerField(
        help_text="Response duration time in minutes"
    )
    start_datetime = models.DateTimeField(null=True, blank=True)
    stop_datetime = models.DateTimeField(null=True, blank=True)
    hide_previous_button = models.BooleanField()
    hide_next_button = models.BooleanField()
    is_private = models.BooleanField()
    password = models.CharField(max_length=50, null=True, blank=True)
    owner = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
    )
