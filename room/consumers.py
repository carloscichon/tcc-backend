import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Conexão aceita")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'room_%s' % self.room_name


        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print("Mensagem recebida do front")
        data = json.loads(text_data)
        message = data['message']
        room = data['room']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'room_message',
                'message': message,
                'room': room,
            }
        )

    async def room_message(self, event):
        print("Entrei no room_message")

        message = event['message']
        room = event['room']

        await self.send(text_data=json.dumps({
            'message': message,
            'room': room
        }))
