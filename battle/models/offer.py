from django.db.models import CharField, ForeignKey, PROTECT

from _utils.models import AbstractBaseModel
from battle.models.user import User


class Offer(AbstractBaseModel):
    title = CharField(max_length=50)
    description = CharField(max_length=240)
    user = ForeignKey(User, on_delete=PROTECT)

    class Meta:
        ordering = ["created"]
