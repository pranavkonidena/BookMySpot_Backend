from django.urls import path
from . import consumers

websocket_urlpaterns = [
    path('uws/', consumers.ChatConsumer.as_asgi()),
]