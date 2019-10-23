from JellyBot.api.static import param, result
from JellyBot.api.responses.mixin import (
    SerializeErrorMixin, SerializeResultOnSuccessMixin, RequireSenderMixin, SerializeResultExtraMixin
)
from mongodb.factory import TokenActionManager

from ._base import BaseApiResponse


class TokenActionCompleteApiResponse(SerializeErrorMixin, SerializeResultExtraMixin, BaseApiResponse):
    def __init__(self, param_dict, sender_oid):
        super().__init__(param_dict, sender_oid)

        self._token = param_dict.get(param.TokenAction.TOKEN)
        self._param_dict.update(**param_dict)
        self._param_dict[param.TokenAction.USER_OID] = sender_oid

    def pass_condition(self) -> bool:
        return self._token and self._result.success

    def _handle_token_(self):
        if not self._token:
            self._err[result.TokenActionResponse.TOKEN] = self._token

    def pre_process(self):
        self._handle_token_()
        self._result = TokenActionManager.complete_action(self._token, self.param_dict)

    def process_pass(self):
        pass

    def serialize_success(self) -> dict:
        return dict()


class TokenActionListApiResponse(
        RequireSenderMixin, SerializeErrorMixin, SerializeResultOnSuccessMixin, BaseApiResponse):
    def __init__(self, param_dict, sender_oid):
        super().__init__(param_dict, sender_oid)

    def process_pass(self):
        self._result = list(TokenActionManager.get_queued_actions(self._sender_oid))

    def pre_process(self):
        super().pre_process()
