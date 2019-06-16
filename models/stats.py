from flags import APIAction as FlagAPIAction
from models.field import BooleanField, DictionaryField, APIActionTypeField, DateTimeField, TextField, ObjectIDField
from models import Model, ModelDefaultValueExtension


class APIStatisticModel(Model):
    Timestamp = "t"
    SenderOID = "s"
    APIAction = "a"
    Parameter = "p"
    PathParameter = "pp"
    Response = "r"
    Success = "s"
    PathInfo = "pi"
    PathInfoFull = "pf"

    default_vals = (
        (Timestamp, ModelDefaultValueExtension.Required),
        (SenderOID, ModelDefaultValueExtension.Optional),
        (APIAction, FlagAPIAction.UNKNOWN),
        (Parameter, None),
        (PathParameter, None),
        (Response, None),
        (Success, False),
        (PathInfo, ModelDefaultValueExtension.Required),
        (PathInfoFull, ModelDefaultValueExtension.Required)
    )

    def _init_fields_(self, **kwargs):
        self.timestamp = DateTimeField(APIStatisticModel.Timestamp, allow_none=False)
        self.sender_oid = ObjectIDField(APIStatisticModel.SenderOID, allow_none=False)
        self.api_action = APIActionTypeField(APIStatisticModel.APIAction, allow_none=False)
        self.parameter = DictionaryField(APIStatisticModel.Parameter, allow_none=True)
        self.path_parameter = DictionaryField(APIStatisticModel.PathParameter, allow_none=True)
        self.response = DictionaryField(APIStatisticModel.Response, allow_none=True)
        self.success = BooleanField(APIStatisticModel.Success, allow_none=True)
        self.path_info = TextField(APIStatisticModel.PathInfo, allow_none=False)
        self.path_info_full = TextField(APIStatisticModel.PathInfoFull, allow_none=False)
