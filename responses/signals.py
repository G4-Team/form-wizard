from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import ModelSignal, post_delete, post_save
from django.dispatch import receiver

from reports.utils import create_new_report

from .models import Response


@receiver(signal=post_save, sender=Response)
def web_socket_report_when_save_response(
    sender: ModelSignal,
    instance: Response,
    created: bool,
    **kwargs,
):
    channel_layer = get_channel_layer()
    phone = instance.pipeline.owner.phone
    if created:
        async_to_sync(channel_layer.group_send)(
            f"report_{phone}_{instance.pipeline.id}",
            {
                "type": "form_response",
                "message": "A new response submitted",
            },
        )
        async_to_sync(channel_layer.group_send)(
            f"report_{phone}_{instance.pipeline.id}",
            {
                "type": "form_response",
                "message": create_new_report(instance.pipeline),
            },
        )
    else:
        async_to_sync(channel_layer.group_send)(
            f"report_{phone}_{instance.pipeline.id}",
            {
                "type": "form_response",
                "message": "A response updated",
            },
        )
        async_to_sync(channel_layer.group_send)(
            f"report_{phone}_{instance.pipeline.id}",
            {
                "type": "form_response",
                "message": create_new_report(instance.pipeline),
            },
        )


@receiver(signal=post_delete, sender=Response)
def web_socket_report_when_delete_response(
    sender: ModelSignal,
    instance: Response,
    **kwargs,
):
    channel_layer = get_channel_layer()
    phone = instance.pipeline.owner.phone
    async_to_sync(channel_layer.group_send)(
        f"report_{phone}_{instance.pipeline.id}",
        {
            "type": "form_response",
            "message": "A response deleted",
        },
    )
    async_to_sync(channel_layer.group_send)(
        f"report_{phone}_{instance.pipeline.id}",
        {
            "type": "form_response",
            "message": create_new_report(instance.pipeline),
        },
    )
