from datetime import timedelta, datetime
from typing import Optional

from django.utils import timezone

from JellyBot import systemconfig
from models import Model, ModelDefaultValueExt
from models.field import TextField, ExecodeField, DateTimeField, DictionaryField, ObjectIDField


class ExecodeEntryModel(Model):
    EXECODE_LENGTH = 10

    CreatorOid = ObjectIDField("cr", default=ModelDefaultValueExt.Required, stores_uid=True)
    Execode = TextField("tk", default=ModelDefaultValueExt.Required,
                        regex=fr"\w{{{EXECODE_LENGTH}}}", must_have_content=True)
    ActionType = ExecodeField("a", default=ModelDefaultValueExt.Required)
    Timestamp = DateTimeField("t", default=ModelDefaultValueExt.Required)
    Data = DictionaryField("d", allow_none=True)

    @property
    def expire_time(self) -> Optional[datetime]:
        return timezone.localtime(self.timestamp) + timedelta(seconds=systemconfig.Database.ExecodeExpirySeconds)