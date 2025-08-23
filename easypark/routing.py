from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/parking-status/", consumers.ParkingStatusConsumer.as_asgi()),
]
