from datetime import datetime
from uuid import uuid4

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from battle.handlers.ntf_handlers import handle_ntf_create


class NTFCreator(WebsocketConsumer):
    def connect(self):
        self.connect_name = uuid4().hex
        async_to_sync(self.channel_layer.group_add)(
            self.connect_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.connect_name, self.channel_name
        )

    def receive(self, text_data):
        response = handle_ntf_create(request=text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.connect_name,
            {
                "type": "type.message",
                "text": response,
            },
        )

    def type_message(self, event):
        self.send(text_data=event["text"])
