from mock_wx import wxTestCase, note_func

import logging
from unittest.mock import call
import wx

from style_stripper.data.enums import PanelType
from style_stripper.model import author_panel

# Constants:
LOG = logging.getLogger(__name__)


class TestContentPanel(wxTestCase):
    def setUp(self) -> None:
        self.app = wx.App()
        self.window = author_panel.AuthorPanel()
        self.window._the_mock = self.app._the_mock

    @note_func("is_current_panel")
    def test_is_current_panel(self):
        """Should indicate whether this is the current panel"""
        panel = self.window
        mock = panel._the_mock

        LOG.info("Not current panel")
        self.app.book.current_panel = PanelType.REVIEW
        panel.is_current_panel()
        expect = [call.is_current_panel(), call.is_current_panel_return_value(False)]

        LOG.info("Current panel")
        self.app.book.current_panel = PanelType.AUTHOR
        panel.is_current_panel()
        expect += [call.is_current_panel(), call.is_current_panel_return_value(True)]

        mock.assert_has_calls(expect)
