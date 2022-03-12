from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import (
    Model,
    DateTimeField,
    BooleanField,
    ForeignKey,
    SET_NULL,
)


class AbstractBaseModel(Model):

    author = ForeignKey(User, blank=True, null=True, on_delete=SET_NULL)
    created = DateTimeField(default=datetime.utcnow, editable=False)
    updated = DateTimeField(default=datetime.utcnow)
    is_active = BooleanField(default=True)
    is_archived = BooleanField(default=False)

    def __repr__(self):
        return str(self.pk)

    class Meta:
        abstract = True
