from django.utils.translation import activate, deactivate

from mongodb.factory import MessageRecordStatisticsManager, ProfileManager

from .models.pipe_in import (
    MessageEventObject, TextMessageEventObject, ImageMessageEventObject, LineStickerMessageEventObject
)
from .models.pipe_out import HandledMessageEventsHolder


def handle_message_main(e: MessageEventObject) -> HandledMessageEventsHolder:
    # Ensure User existence in channel
    ProfileManager.register_new_default(e.channel_model.id, e.user_model.id)

    # Translation activation
    activate(e.user_model.config.language)

    # Main handle process
    if isinstance(e, TextMessageEventObject):
        from .text.main import handle_text_event

        ret = HandledMessageEventsHolder(handle_text_event(e))
    elif isinstance(e, ImageMessageEventObject):
        from .img.main import handle_image_event

        ret = HandledMessageEventsHolder(handle_image_event(e))
    elif isinstance(e, LineStickerMessageEventObject):
        from .stk.main import handle_line_sticker_event

        ret = HandledMessageEventsHolder(handle_line_sticker_event(e))
    else:
        from .logger import logger

        logger.logger.info(f"Message handle object not handled. Raw: {e.raw}")
        ret = HandledMessageEventsHolder()

    # Translation deactivation
    deactivate()

    # Record message for stats
    MessageRecordStatisticsManager.record_message(
        e.channel_model.id, e.user_model.id, e.message_type, e.content, e.constructed_time)

    return ret
