from mock_wx import wxTestCase, note_func

import logging
from unittest.mock import call
import wx

from style_stripper.model import done_panel

# Constants:
LOG = logging.getLogger(__name__)


class TestDonePanel(wxTestCase):
    def setUp(self) -> None:
        self.app = wx.App()
        self.window = done_panel.DonePanel()
        self.window._the_mock = self.app._the_mock

    @note_func("apply")
    def test_apply(self):
        """Should apply all the checkboxes"""
        panel = self.window
        mock = panel._the_mock
        self.app.frame.review_panel.questionable = [
            mock.question1,
            mock.question2,
            mock.question3,
        ]

        panel.apply()
        mock.assert_has_calls(
            [
                call.apply(),
                call.question1.apply(),
                call.question2.apply(),
                call.question3.apply(),
            ]
        )
