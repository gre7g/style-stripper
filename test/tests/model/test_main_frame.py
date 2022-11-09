from mock_wx import wxTestCase, note_func

from datetime import datetime
import logging
from unittest.mock import call, patch
import wx

from style_stripper.model import main_frame

# Constants:
LOG = logging.getLogger(__name__)


class TestMainFrame(wxTestCase):
    def setUp(self) -> None:
        self.app = wx.App()
        self.window = main_frame.MainFrame()
        self.window._the_mock = self.app._the_mock

    @note_func("show_title")
    def test_show_title(self):
        """Should update the frame's title"""
        frame = self.window
        mock = frame._the_mock

        LOG.info("Previously saved")
        self.app.book.is_modified.return_value = False
        self.app.file_path = "/path/to/file"
        frame.show_title()
        expect = [
            call.show_title(),
            call.App.book.is_modified(),
            call.MainFrame.SetTitle("Style Stripper - file"),
        ]

        LOG.info("Modified")
        self.app.book.is_modified.return_value = True
        frame.show_title()
        expect += [
            call.show_title(),
            call.App.book.is_modified(),
            call.MainFrame.SetTitle("Style Stripper - file*"),
        ]

        LOG.info("Never previously saved")
        self.app.file_path = None
        self.app.book.is_modified.return_value = False
        frame.show_title()
        expect += [
            call.show_title(),
            call.App.book.is_modified(),
            call.MainFrame.SetTitle("Style Stripper"),
        ]

        LOG.info("Modified")
        self.app.book.is_modified.return_value = True
        frame.show_title()
        expect += [
            call.show_title(),
            call.App.book.is_modified(),
            call.MainFrame.SetTitle("Style Stripper*"),
        ]

        mock.assert_has_calls(expect)

    @note_func("refresh_file_history")
    def test_refresh_file_history(self):
        """Should refresh the current file in the file history"""
        frame = self.window
        mock = frame._the_mock

        self.app.file_path = "/path/to/file"
        frame.refresh_file_history()
        mock.assert_has_calls(
            [
                call.refresh_file_history(),
                call.MainFrame.file_history.AddFileToHistory("/path/to/file"),
                call.FileConfig("StyleStripper"),
                call.MainFrame.file_history.Save(mock.FileConfig.return_value),
            ]
        )
