import locale
import logging
from typing import Optional
import wx

from style_stripper.control.frame_control import FrameControl
from style_stripper.control.menu_control import MenuControl
from style_stripper.control.settings_control import SettingsControl, Settings
from style_stripper.data.book import Book
from style_stripper.data.constants import CONSTANTS
from style_stripper.data.template import Templates, Template
from style_stripper.model.main_frame import MainFrame

# Constants:
LOG = logging.getLogger(__name__)


class StyleStripperApp(wx.App):
    file_path: Optional[str]
    initialized: bool
    frame_controls: FrameControl
    menu_controls: MenuControl
    settings_controls: SettingsControl
    frame: MainFrame
    book: Book
    settings: Settings
    templates: Optional[Templates]
    template: Optional[Template]

    def __init__(self, *args, **kwargs):
        self.file_path = None
        self.initialized = False

        # Controls
        self.frame_controls = FrameControl(self)
        self.menu_controls = MenuControl(self)
        self.settings_controls = SettingsControl(self)
        self.templates = self.template = None

        super(StyleStripperApp, self).__init__(*args, **kwargs)

    def init(self):
        self.frame = MainFrame(None, title=CONSTANTS.UI.APP_NAME)
        self.settings_controls.load_settings()
        self.frame.init()

        self.book = Book(self.settings.latest_config)
        self.initialized = True
        locale.setlocale(locale.LC_ALL, "")
        self.frame.refresh_contents()

    def __getattribute__(self, item: str):
        """Get a wrapper for all panels within the application"""
        # Note: Some functions are applied to all panels. For example app.grab_contents() will call a grab_contents()
        # member function on each of the frame's panels. If the function returns a value, the active panel is the one
        # returned.
        def wrap(*args, **kwargs):
            return_value = None
            for panel_type, panel in self.frame.panels.items():
                func = getattr(panel, item)
                value = func(*args, **kwargs)
                if panel.is_current_panel():
                    return_value = value
            return return_value

        return wrap
