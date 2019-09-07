from JellyBotAPI.api.static import param
from JellyBotAPI.api.responses import (
    PermissionQueryResponse
)
from JellyBotAPI.components.mixin import CsrfExemptMixin, CheckParameterMixin, APIStatisticsCollectMixin
from JellyBotAPI.components.views import APIJsonResponseView
from flags import APICommand


class PermissionQueryView(CsrfExemptMixin, APIStatisticsCollectMixin, CheckParameterMixin, APIJsonResponseView):
    get_response_class = PermissionQueryResponse

    def get_api_action(self):
        return APICommand.DATA_PERMISSION

    def mandatory_keys(self) -> set:
        return {param.Manage.Channel.CHANNEL_OID}