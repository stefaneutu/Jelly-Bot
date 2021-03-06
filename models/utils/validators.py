import urllib.request
from typing import Any

from JellyBot.systemconfig import AutoReply
from extutils import safe_cast

from extutils.line_sticker import LineStickerManager
from flags import AutoReplyContentType

__all__ = ["AutoReplyValidator"]


class AutoReplyValidator:
    # noinspection PyArgumentList
    @staticmethod
    def is_valid_content(type_: AutoReplyContentType, content: Any, *, online_check=True) -> bool:
        if not isinstance(type_, AutoReplyContentType):
            type_ = AutoReplyContentType(type_)

        if type_ == AutoReplyContentType.TEXT:
            return 0 < len(content.strip()) <= AutoReply.MaxContentLength

        if type_ == AutoReplyContentType.IMAGE:
            return _BaseValidator.is_content_image(content, online_check)

        if type_ == AutoReplyContentType.LINE_STICKER:
            return _BaseValidator.is_content_sticker(content, online_check)

        return True


class _BaseValidator:
    # noinspection PyBroadException
    @staticmethod
    def is_content_image(content: Any, online_check) -> bool:
        if online_check:
            try:
                # Add headers to prevent discord CDN failure
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) "
                                  "AppleWebKit/537.11 (KHTML, like Gecko) "
                                  "Chrome/23.0.1271.95 Safari/537.11"}

                req = urllib.request.Request(content, headers=headers)
                with urllib.request.urlopen(req) as response:
                    if response.info().get_content_maintype() != "image":
                        return False
                    else:
                        return True
            except Exception:
                return False
        else:
            try:
                return content.startswith("http") and (content[len(content) - 4:] in (".png", ".jpg"))
            except Exception:
                return False

    @staticmethod
    def is_content_sticker(content: Any, online_check) -> bool:
        if online_check:
            return LineStickerManager.is_sticker_exists(content)
        else:
            return safe_cast(content, int) is not None
