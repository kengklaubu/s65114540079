import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ParkingStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("parking_status", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("parking_status", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            "parking_status",
            {
                "type": "update_status",
                "message": data["message"],
            }
        )

    async def update_status(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()
async_to_sync(channel_layer.group_send)(
    "parking_status",
    {
        "type": "update_status",
        "message": "Parking spot updated!",
    }
)



