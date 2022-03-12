from django.db.models import (
    ForeignKey,
    PROTECT,
    IntegerChoices,
    SmallIntegerField, CharField,
)

from _utils.models import AbstractBaseModel
from battle.models.battle import Battle
from battle.models.user import User


class RoundChoices(IntegerChoices):
    PAPER = 1
    SCISSORS = 2
    STONE = 3


class Round(AbstractBaseModel):
    number = SmallIntegerField()
    battle = ForeignKey(Battle, on_delete=PROTECT)

    offeror_websocket = CharField(max_length=32)
    acceptor_websocket = CharField(max_length=32)

    offeror_choice = SmallIntegerField(
        choices=RoundChoices.choices, blank=True, null=True
    )
    acceptor_choice = SmallIntegerField(
        choices=RoundChoices.choices, blank=True, null=True
    )

    offeror_minus_point = SmallIntegerField(blank=True, null=True)
    acceptor_minus_point = SmallIntegerField(blank=True, null=True)

    winner = ForeignKey(User, blank=True, null=True, on_delete=PROTECT)

    class Meta:
        ordering = ["created"]
