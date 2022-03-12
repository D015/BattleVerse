from django.db.models import (
    ForeignKey,
    PROTECT,
    PositiveSmallIntegerField,
)

from _utils.models import AbstractBaseModel
from battle.models import User
from battle.models.accept import Accept


class Battle(AbstractBaseModel):
    accept = ForeignKey(Accept, on_delete=PROTECT)
    offeror_point_start = PositiveSmallIntegerField()
    offeror_point_end = PositiveSmallIntegerField()
    acceptor_point_start = PositiveSmallIntegerField()
    acceptor_point_end = PositiveSmallIntegerField()

    winner = ForeignKey(User, blank=True, null=True, on_delete=PROTECT)

    class Meta:
        ordering = ["created"]
