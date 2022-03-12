from django.db.models import (
    ForeignKey,
    PROTECT,
)

from _utils.models import AbstractBaseModel
from battle.models.offer import Offer
from battle.models.user import User


class Accept(AbstractBaseModel):
    user = ForeignKey(User, on_delete=PROTECT)
    offer = ForeignKey(Offer, on_delete=PROTECT)

    class Meta:
        ordering = ["created"]
