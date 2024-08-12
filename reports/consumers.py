import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import (
    AsyncJsonWebsocketConsumer,
    AsyncWebsocketConsumer,
)

from forms.models import Pipeline
from reports.utils import acreate_new_report


class FormReportConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        pipline_id = self.scope["url_route"]["kwargs"]["pipeline_id"]
        if user.is_authenticated:
            pipline = None
            try:
                pipline = await Pipeline.objects.select_related("owner").aget(
                    pk=pipline_id
                )
            except Pipeline.DoesNotExist:
                pass
            if pipline is None or pipline.owner.id != user.id:
                self.room_group_name = "perrmission_denied"
                await self.channel_layer.group_add(
                    self.room_group_name, self.channel_name
                )
                await self.accept()
                await self.send(
                    text_data=json.dumps({"permission-denied": "You are not Owner"})
                )
                await self.close()
            else:
                self.room_name = user.phone
                self.room_group_name = f"report_{self.room_name}_{pipline_id}"
                await self.channel_layer.group_add(
                    self.room_group_name, self.channel_name
                )
                await self.accept()
                response = await acreate_new_report(pipeline=pipline)
                await self.send(text_data=json.dumps(response))
        else:
            self.room_group_name = "perrmission_denied"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            await self.send(
                text_data=json.dumps(
                    {
                        "permission-denied": "Please provide valid authentication credentials."
                    }
                )
            )
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "form_response", "message": message}
        )

    async def form_response(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
