import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application
from django.urls import path


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_config.settings")
django.setup()


from battle.consumers.ntf_consumers import NTFCreator
from battle.consumers.user_consumers import UserCreator
from battle.consumers.offer_consumers import OfferCreator, OfferList
from battle.consumers.accept_consumers import AcceptCreator, AcceptList
from battle.consumers.battle_consumers import BattleCreator, BattleMover


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter(
            (
                # path("game", GameConsumer.as_asgi()),
                path("ntf_create", NTFCreator.as_asgi()),
                path("user_create", UserCreator.as_asgi()),
                path("battles_create", OfferCreator.as_asgi()),
                path("battles_list", OfferList.as_asgi()),
                path("battles/accept", AcceptCreator.as_asgi()),
                path("accept_list/<int:offer_pk>", AcceptList.as_asgi()),
                path("battles_start", BattleCreator.as_asgi()),
                path("battles_move", BattleMover.as_asgi()),

                # path("battle/<int:id>", BattlesConsumer.as_asgi()),
            )
        ),
    }
)
