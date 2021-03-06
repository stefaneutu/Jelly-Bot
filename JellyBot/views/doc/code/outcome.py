from django.views import View
from django.utils.translation import gettext_lazy as _

from JellyBot.views.render import render_flag_table
from mongodb.factory.results import WriteOutcome, GetOutcome, OperationOutcome, UpdateOutcome


class InsertOutcomeCodeView(View):
    # noinspection PyUnusedLocal, PyMethodMayBeStatic, PyTypeChecker
    def get(self, request, *args, **kwargs):
        return render_flag_table(
            request, _("Insert Outcome Code"), _("Insert Outcome"), WriteOutcome, {"td_color": True})


class GetOutcomeCodeView(View):
    # noinspection PyUnusedLocal, PyMethodMayBeStatic, PyTypeChecker
    def get(self, request, *args, **kwargs):
        return render_flag_table(
            request, _("Get Outcome Code"), _("Get Outcome"), GetOutcome, {"td_color": True})


class OperationOutcomeCodeView(View):
    # noinspection PyUnusedLocal, PyMethodMayBeStatic, PyTypeChecker
    def get(self, request, *args, **kwargs):
        return render_flag_table(
            request, _("Operation Outcome Code"), _("Operation Outcome"), OperationOutcome, {"td_color": True})


class UpdateOutcomeCodeView(View):
    # noinspection PyUnusedLocal, PyMethodMayBeStatic, PyTypeChecker
    def get(self, request, *args, **kwargs):
        return render_flag_table(
            request, _("Update Outcome Code"), _("Update Outcome"), UpdateOutcome, {"td_color": True})
