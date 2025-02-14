import json
from django.contrib.auth.models import AnonymousUser
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from accounts.models import CustomUser
from .models import Chat


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get("user")
        if self.user and self.user.is_authenticated:
            raw_token = str(self.scope["url_route"]["kwargs"]["token"])
            self.room_id = raw_token.replace("-", "")
            await self.channel_layer.group_add(self.room_id, self.channel_name)

            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_id, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            username = text_data_json["username"]
            raw_token = str(text_data_json["token"])
            token = raw_token.replace("-", "")
            message_data = {
                "type": "chat_message",
                "message": text_data_json["message"],
                "username": text_data_json.get(
                    "username", username
                ),  # اضافه کردن نام کاربر
            }
            await self.save_message(text_data_json["message"], username)
            await self.channel_layer.group_send(token, message_data)

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {"message": event["message"], "username": event["username"]}
            )
        )

    @sync_to_async
    def save_message(self, message, username):
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise ValueError("The user does not exist")
        Chat.objects.create(user=user, message=message)
