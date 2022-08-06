import json
import datetime

from django.core.exceptions import ObjectDoesNotExist

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from comments_and_chats.models import Message, PrivatChat, Comment
from media_storage.models import Media
from accounts.models import ProfileData


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self):
        self.room_group_name = 'chat_%s' % self.room_name
        self.room_name = self.scope['url_route']['kwargs']['room_name']

    async def connect(self):

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        type_chat = text_data_json['type_chat']
        created = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'username': str(self.scope["user"]),
                'userID': str(self.scope["user"].pk),
                'created': created,
                'message': message
            }
        )
        if type_chat == 'chat':
            await self.create_message(message)
        else:
            await self.create_comment(message)

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def profile_photo(self):
        try:
            profile = ProfileData.objects.get(owner__pk=self.scope["user"].pk).avatar
        except ObjectDoesNotExist:
            profile = 'none'
        return profile

    @database_sync_to_async
    def create_message(self, message):
        try:
            chat = PrivatChat.objects.get(id=int(self.room_name))
            Message.objects.create(chat=chat, author=self.scope["user"], content=message)
        except ObjectDoesNotExist:
            print('chat not found')

    @database_sync_to_async
    def create_comment(self, message):
        try:
            chat = Media.objects.get(id=int(self.room_name))
            Comment.objects.create(media=chat, author=self.scope["user"], content=message)
        except ObjectDoesNotExist:
            print('chat not found')
