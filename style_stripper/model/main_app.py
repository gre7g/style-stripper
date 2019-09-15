import logging
import os
import wx

from style_stripper.control.frame_control import FrameControl
from style_stripper.control.menu_control import MenuControl
from style_stripper.control.settings_control import SettingsControl
from style_stripper.data.book import Book
from style_stripper.model.main_frame import MainFrame

# Constants:
LOG = logging.getLogger(__name__)

TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docx_templates")


class StyleStripperApp(wx.App):
    def __init__(self, *args, **kwargs):
        # Basics
        self.frame = self.book = None
        self.settings = None

        # Controls
        self.frame_controls = FrameControl(self)
        self.menu_controls = MenuControl(self)
        self.settings_controls = SettingsControl(self)

        wx.App.__init__(self, *args, **kwargs)

    def init(self):
        self.frame = MainFrame(None, title="Style Stripper")
        self.settings_controls.load_settings()
        self.frame.init()

        self.book = Book(self.settings.latest_config)
