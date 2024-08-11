import json

from channels.generic.websocket import (
    AsyncJsonWebsocketConsumer,
    AsyncWebsocketConsumer,
)


class FormReportConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]

        if user.is_authenticated:
            self.room_name = user.phone
            self.room_group_name = f"report_{self.room_name}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

            await self.accept()
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
