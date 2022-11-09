from mock_wx import wxTestCase, note_func

import locale
import logging
from unittest.mock import call, patch

from style_stripper.model import main_app

# Constants:
LOG = logging.getLogger(__name__)


class TestMainApp(wxTestCase):
    def setUp(self) -> None:
        self.app = main_app.StyleStripperApp()
        self.window = self.app

    @patch("style_stripper.model.main_app.MainFrame")
    @patch("style_stripper.model.main_app.locale")
    @patch("style_stripper.model.main_app.Book")
    @note_func("init")
    def test_init(self, Book, _locale, MainFrame):
        """Should initialize the application"""
        app = self.app
        mock = app._the_mock
        main_app.MainFrame = mock.MainFrame
        main_app.locale = mock.locale
        main_app.locale.LC_ALL = locale.LC_ALL
        main_app.Book = mock.Book
        app.settings_controls = mock.settings_controls
        app.refresh_contents = mock.refresh_contents
        self.app.settings = mock.settings

        app.init()
        mock.initialized(self.app.initialized)
        mock.assert_has_calls(
            [
                call.init(),
                call.MainFrame(None, title="Style Stripper", name="frame"),
                call.settings_controls.load_settings(),
                call.Book(mock.settings.latest_config),
                call.MainFrame().init(),
                call.locale.setlocale(0, ""),
                call.refresh_contents(),
                call.initialized(True),
            ]
        )
