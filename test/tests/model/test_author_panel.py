from mock_wx import wxTestCase, note_func

from datetime import datetime
import logging
from unittest.mock import call, patch
import wx

from style_stripper.model import author_panel
from style_stripper.model import content_panel

# Constants:
LOG = logging.getLogger(__name__)


class TestAuthorPanel(wxTestCase):
    def setUp(self) -> None:
        self.app = wx.App()
        self.window = author_panel.AuthorPanel()
        self.window._the_mock = self.app._the_mock
        self.app.book.source_path = "/path/to/source.docx"
        self.app.book.author = "Author Name"
        self.app.book.title = "Book Title"
        wx.DateTime._patch('.FormatDate.return_value = "11/7/2022"')
        wx.DateTime._patch('.FormatTime.return_value = "3:21:00pm"')

    @patch("style_stripper.model.content_panel.ContentPanel.is_current_panel")
    @note_func("refresh_contents")
    def test_refresh_contents(self, is_current_panel):
        """Should update the panel contents"""
        panel = self.window
        mock = panel._the_mock
        content_panel.ContentPanel.is_current_panel = mock.is_current_panel

        LOG.info("Not current panel, no content, not modified")
        mock.is_current_panel.return_value = False
        self.app.book.word_count = None
        self.app.book.last_modified = None
        panel.refresh_contents()
        expect = [
            call.refresh_contents(),
            call.is_current_panel(),
            call.AuthorPanel.Show(False),
            call.file_path_ctrl.SetLabel("/path/to/source.docx"),
            call.author_ctrl.SetValue("Author Name"),
            call.title_ctrl.SetValue("Book Title"),
            call.word_count_ctrl.SetLabel(""),
            call.modified_ctrl.SetLabel(""),
        ]

        LOG.info("Current panel, content, modified")
        mock.is_current_panel.return_value = True
        self.app.book.word_count = 123456
        self.app.book.last_modified = datetime(2022, 11, 7, 15, 21)
        panel.refresh_contents()
        expect += [
            call.refresh_contents(),
            call.is_current_panel(),
            call.AuthorPanel.Show(True),
            call.file_path_ctrl.SetLabel("/path/to/source.docx"),
            call.author_ctrl.SetValue("Author Name"),
            call.title_ctrl.SetValue("Book Title"),
            call.word_count_ctrl.SetLabel("123456"),
            call.DateTime(7, 10, 2022, 15, 21, 0),
            call.DateTime.FormatDate(),
            call.DateTime.FormatTime(),
            call.modified_ctrl.SetLabel("11/7/2022 3:21:00pm"),
        ]
        mock.assert_has_calls(expect)

    @note_func("book_loaded")
    def test_book_loaded(self):
        """Should enable the Next button when the book is ready"""
        panel = self.window
        mock = panel._the_mock

        panel.book_loaded(True)
        mock.assert_has_calls([call.book_loaded(True), call.next.Enable(True)])
