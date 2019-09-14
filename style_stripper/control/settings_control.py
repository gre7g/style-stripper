from base64 import b64encode, b64decode
import binascii
from docx.enum.section import WD_SECTION
import logging
import pickle
import wx

# Constants:
LOG = logging.getLogger(__name__)


class Settings(object):
    file_path = None
    window_rect = None
    maximized = False

    def __init__(self):
        self.file_version = 1
        self.latest_config = {
            "SOURCE": {
                "PATH": "",
                "AUTHOR": "",
                "TITLE": "",
                "WORD_COUNT": None,
                "LAST_MODIFIED": None
            },
            "SPACES": {
                "PURGE_DOUBLE_SPACES": True,
                "PURGE_LEADING_WHITESPACE": True,
                "PURGE_TRAILING_WHITESPACE": True
            },
            "ITALIC": {
                "ADJUST_TO_INCLUDE_PUNCTUATION": True
            },
            "QUOTES": {
                "CONVERT_TO_CURLY": True
            },
            "DIVIDER": {
                "BLANK_PARAGRAPH_IF_NO_OTHER": True,
                "REPLACE_WITH_NEW": True,
                "NEW": "# # #",
                "REMOVE_DIVIDERS_BEFORE_HEADINGS": True
            },
            "ELLIPSES": {
                "REPLACE_WITH_NEW": True,
                "NEW": "\u200a.\u200a.\u200a.\u200a"  # Alternative is \u2009
            },
            "HEADINGS": {
                "STYLE_PART": True,
                "STYLE_CHAPTER": True,
                "STYLE_THE_END": True,
                "FLATTEN_IF_NO_PARTS": True,
                "HEADER_FOOTER_AFTER_BREAK": False,
                "BREAK_BEFORE_HEADING": WD_SECTION.ODD_PAGE
            },
            "DASHES": {
                "CONVERT_DOUBLE_DASHES": True,
                "CONVERT_TO_EN_DASH": False,
                "CONVERT_TO_EM_DASH": True,
                "FIX_DASH_AT_END_OF_QUOTE": True,
                "FORCE_ALL_EN_OR_EM": True
            },
            "STYLING": {
                "INDENT_FIRST_PARAGRAPH": False,
                "CENTER_DIVIDER": True
            }
        }

    def init(self):
        return self


class SettingsControl(object):
    def __init__(self, app):
        self.app = app
        self._save_maximized = True

    def load_settings(self):
        try:
            self.app.settings = pickle.loads(b64decode(wx.FileConfig("StyleStripper").Read("configuration", "")))
        except (TypeError, binascii.Error):
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
        wx.FileConfig("StyleStripper").Write("configuration", b64encode(pickle.dumps(self.app.settings)))
        if close_frame:
            self.app.frame.Close()
