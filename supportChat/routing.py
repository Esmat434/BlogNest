from django.urls import path
from .consumer import ChatConsumer

websocket_urlpatterns = [
    path(
        "ws/support/chat/<str:username>/<uuid:token>/",
        ChatConsumer.as_asgi(),
        name="chat_consumer",
    )
]
