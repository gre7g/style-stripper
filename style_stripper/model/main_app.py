import logging
import os
import sys
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

TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docx_templates")


class StyleStripperApp(wx.App):
    file_path: Optional[str]
    initialized: bool
    base_dir: str  # abspath to style_stripper
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
        if sys.argv[0].endswith(".exe"):
            self.base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        else:
            self.base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

        # Controls
        self.frame_controls = FrameControl(self)
        self.menu_controls = MenuControl(self)
        self.settings_controls = SettingsControl(self)
        self.templates = self.template = None

        wx.App.__init__(self, *args, **kwargs)

    def init(self):
        self.frame = MainFrame(None, title=CONSTANTS.UI.APP_NAME)
        self.settings_controls.load_settings()
        self.frame.init()

        self.book = Book(self.settings.latest_config)
        self.initialized = True
        self.frame.refresh_contents()
