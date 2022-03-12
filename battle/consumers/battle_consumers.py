import json
from uuid import uuid4

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from battle.handlers.battle_handlers import handle_battle_create, \
    handle_battle_mover


class BattleCreator(WebsocketConsumer):
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
        response = handle_battle_create(request=text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.connect_name,
            {
                "type": "type.message",
                "text": response,
            },
        )

    def type_message(self, event):
        self.send(text_data=event["text"])


class BattleMover(WebsocketConsumer):
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
        result_battle_move = handle_battle_mover(
            request=text_data, the_websocket=self.connect_name
        )

        offeror_websocket = result_battle_move.pop("offeror_websocket", None)
        acceptor_websocket = result_battle_move.pop("acceptor_websocket", None)

        response = json.dumps(result_battle_move)

        another_connect_name_set = frozenset({
            offeror_websocket, acceptor_websocket
        }).difference(frozenset({self.connect_name}))

        if len(another_connect_name_set):
            another_connect_name = set(another_connect_name_set).pop()
        else:
            another_connect_name = None

        async_to_sync(self.channel_layer.group_send)(
            self.connect_name,
            {
                "type": "type.message",
                "text": response,
            },
        )

        if another_connect_name:
            async_to_sync(self.channel_layer.group_send)(
                another_connect_name,
                {
                    "type": "type.message",
                    "text": response,
                },
            )

    def type_message(self, event):
        self.send(text_data=event["text"])
