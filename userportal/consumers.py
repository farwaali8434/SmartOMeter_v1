# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from userportal.serializers import MessageSerializer
from .models import Chat, User, Message


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_id = f"chat_{self.scope['url_route']['kwargs']['ticket_id']}"

    def connect(self):
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.chat_id,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_id,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        payload = json.loads(text_data)
        payload['data']['sent_by'] = self.scope["user"]
        message = Message.objects.create(**payload['data'])
        payload = {
            'command': 'new_message',
            'message': MessageSerializer(message).data
        }
        self.send_chat_message(payload)

    def send_chat_message(self, payload):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.chat_id,
            {
                'type': 'chat_message',
                'payload': payload
            }
        )

    # Receive message from room group

    def chat_message(self, event):
        payload = event['payload']
        # Send message to WebSocket
        self.send(text_data=json.dumps(payload))
