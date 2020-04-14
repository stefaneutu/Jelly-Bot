from .email import TestFakeEmailServer
from .checker import TestArgTypeEnsure
from .flags import (
    TestFlagCodeEnum, TestFlagSingleCodeEnum, TestFlagDoubleCodeEnum, TestFlagPrefixedDoubleCodeEnum, TestFlagMisc
)
from .imgproc import TestImgurClient
from .linesticker import TestLineStickerUtils
from .boolext import TestBooleanExtension
from .color import TestColor, TestColorFactory
from .dt import TestDatetime, TestParseTimeRange
from .singleton import TestSingleton
from .utils import TestFunctions
from .locales import TestFunctions, TestLocaleInfo