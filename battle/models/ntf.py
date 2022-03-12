from django.db.models import CharField

from _utils.models import AbstractBaseModel


class NTF(AbstractBaseModel):
    name = CharField(max_length=50)
    description = CharField(max_length=240)

    class Meta:
        ordering = ["created"]
