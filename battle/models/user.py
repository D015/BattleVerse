from django.db.models import (
    CharField,
    ForeignKey,
    PROTECT,
)

from _utils.models import AbstractBaseModel
from battle.models.ntf import NTF


class User(AbstractBaseModel):
    username = CharField(max_length=50)
    description = CharField(max_length=240)
    ntf = ForeignKey(NTF, on_delete=PROTECT)

    class Meta:
        ordering = ["created"]
