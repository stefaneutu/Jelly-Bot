from models import OID_KEY, PendingRepairDataModel
from extutils.mongo import get_codec_options

from ._base import single_db_name, BaseCollection
from .factory import MONGO_CLIENT
from ..utils import BulkWriteDataHolder


DB_NAME = "pdrp"


class PendingRepairDataManager:
    def __init__(self):
        if single_db_name:
            self._db = MONGO_CLIENT.get_database(single_db_name)
        else:
            self._db = MONGO_CLIENT.get_database(DB_NAME)

    def new_bulk_holder(self, col_inst: BaseCollection) -> BulkWriteDataHolder:
        if single_db_name:
            col_full_name = f"{DB_NAME}.{col_inst.get_col_name()}"
        else:
            col_full_name = col_inst.full_name

        col = self._db.get_collection(col_full_name, codec_options=get_codec_options())
        col.create_index(f"{PendingRepairDataModel.Data.key}.{OID_KEY}", unique=True)

        return BulkWriteDataHolder(col)


_inst = PendingRepairDataManager()
