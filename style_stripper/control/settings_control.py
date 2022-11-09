from base64 import b64encode, b64decode
import binascii
from dataclasses import dataclass, field
import logging
import pickle
from typing import Optional
import wx

from style_stripper.data.constants import CONSTANTS
from style_stripper.data.enums import PaginationType

try:
    from style_stripper.model.main_app import StyleStripperApp
except ImportError:
    StyleStripperApp = None

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


@dataclass
class SpacesConfig:
    purge_double: bool = True
    purge_leading: bool = True
    purge_trailing: bool = True


@dataclass
class ItalicConfig:
    adjust_to_include_punctuation: bool = True


@dataclass
class QuotesConfig:
    convert_to_curly: bool = True


@dataclass
class DividerConfig:
    blank_paragraph_if_no_other: bool = True
    replace_with_new: bool = True
    new: str = "# # #"


@dataclass
class EllipsesConfig:
    replace_with_new: bool = True
    new: str = "\u200a.\u200a.\u200a.\u200a"  # Alternative is \u2009


@dataclass
class HeadingsConfig:
    style_parts_and_chapter: bool = True
    style_the_end: bool = True
    add_the_end: bool = True
    the_end: str = _("The End")
    header_footer_after_break: bool = False
    break_before_heading: PaginationType = PaginationType.ODD_PAGE


@dataclass
class DashesConfig:
    convert_double: bool = True
    convert_to_en_dash: bool = False
    convert_to_em_dash: bool = True
    fix_at_end_of_quote: bool = True
    force_all_en_or_em: bool = True


@dataclass
class StylingConfig:
    indent_first_paragraph: bool = False


@dataclass
class ConfigSettings:
    spaces: SpacesConfig = field(default_factory=SpacesConfig)
    italic: ItalicConfig = field(default_factory=ItalicConfig)
    quotes: QuotesConfig = field(default_factory=QuotesConfig)
    divider: DividerConfig = field(default_factory=DividerConfig)
    ellipses: EllipsesConfig = field(default_factory=EllipsesConfig)
    headings: HeadingsConfig = field(default_factory=HeadingsConfig)
    dashes: DashesConfig = field(default_factory=DashesConfig)
    styling: StylingConfig = field(default_factory=StylingConfig)


@dataclass
class Settings:
    window_rect: Optional[wx.Rect] = None
    maximized: bool = False
    file_version: int = 1
    latest_config: ConfigSettings = field(default_factory=ConfigSettings)

    def init(self):
        return self


@dataclass
class SettingsControl:
    app: StyleStripperApp
    _save_maximized: bool = True

    def load_settings(self):
        try:
            pickle_data = b64decode(
                wx.FileConfig(CONSTANTS.UI.CATEGORY_NAME).Read(
                    CONSTANTS.UI.CONFIG_PARAM, ""
                )
            )
            self.app.settings = pickle.loads(pickle_data)
        except (
            TypeError,
            binascii.Error,
            ModuleNotFoundError,
            EOFError,
            AttributeError,
        ) as msg:
            LOG.exception(
                _("Unable to load old settings due to a %r. No biggie. Starting fresh.")
                % msg
            )
            self.app.settings = Settings()
        self.app.settings = self.app.settings.init()

    def save_settings_on_exit(self, event):
        self.app.book.not_modified()

        maximized = self.app.frame.IsMaximized()
        if self._save_maximized:
            self.app.settings.maximized = maximized
            self._save_maximized = False

        if maximized:
            self.app.frame.Maximize(False)
            wx.CallLater(100, self.save_settings_on_exit2, True)
        else:
            event.Skip()
            self.save_settings_on_exit2(False)

    def save_settings_on_exit2(self, close_frame):
        self.app.settings.window_rect = self.app.frame.GetRect()
        param_data = b64encode(pickle.dumps(self.app.settings))
        wx.FileConfig(CONSTANTS.UI.CATEGORY_NAME).Write(
            CONSTANTS.UI.CONFIG_PARAM, param_data
        )
        if close_frame:
            self.app.frame.Close()
