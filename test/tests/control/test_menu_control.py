from mock_wx import wxTestCase, note_func

import logging
from unittest.mock import call, patch, mock_open
import wx

from style_stripper.control import menu_control
from style_stripper.data.enums import PanelType

# Constants:
LOG = logging.getLogger(__name__)


class TestMenuControl(wxTestCase):
    def setUp(self) -> None:
        self.app = wx.App()
        self.window = menu_control.MenuControl(self.app)

    @note_func("on_new")
    def test_on_new(self):
        """Should reset to a new book"""
        control = self.window
        mock = self.app._the_mock
        frame = self.app.frame

        LOG.info("Book modified, cancelled")
        self.app.book.is_modified.return_value = True
        wx.MessageDialog._patch(".ShowModal.return_value = %d" % wx.ID_CANCEL)
        control.on_new(None)
        expect = [
            call.on_new(None),
            call.App.book.is_modified(),
            call.MessageDialog(
                frame,
                "Changes not saved! Do you want to start a new file without saving?",
                "Permanent Action",
                -2147483372,
            ),
            call.MessageDialog.ShowModal(),
            call.MessageDialog.Destroy(),
        ]

        LOG.info("Okay to discard")
        wx.FileDialog._patch(".ShowModal.return_value = %d" % wx.ID_OK)
        control.on_new(None)
        expect += [
            call.on_new(None),
            call.App.book.is_modified(),
            call.MessageDialog(
                frame,
                "Changes not saved! Do you want to start a new file without saving?",
                "Permanent Action",
                -2147483372,
            ),
            call.MessageDialog.ShowModal(),
            call.MessageDialog.Destroy(),
        ]

        LOG.info("Not modified")
        self.app.book.is_modified.return_value = True
        control.on_new(None)
        expect += [
            call.on_new(None),
            call.App.book.is_modified(),
            call.MessageDialog(
                frame,
                "Changes not saved! Do you want to start a new file without saving?",
                "Permanent Action",
                -2147483372,
            ),
            call.MessageDialog.ShowModal(),
            call.MessageDialog.Destroy(),
        ]

        mock.assert_has_calls(expect)

    @patch("style_stripper.control.menu_control.pickle")
    @note_func("on_save")
    def test_on_save(self, pickle):
        """Should save configuration"""
        control = self.window
        mock = self.app._the_mock
        frame = self.app.frame
        control.on_save_as = mock.on_save_as
        menu_control.pickle = mock.pickle

        LOG.info("Known filename, failed to save")
        self.app.file_path = "/path/to/file"
        with patch("style_stripper.control.menu_control.open"):
            menu_control.open = mock.open
            mock.open.side_effect = OSError("Save failed")
            control.on_save(None)
        expect = [
            call.on_save(None),
            call.open("/path/to/file", "wb"),
            call.MessageDialog(frame, "Error: Save failed", "Save Error", 260),
            call.MessageDialog.ShowModal(),
            call.MessageDialog.Destroy(),
        ]

        LOG.info("Saved okay")
        with patch("style_stripper.control.menu_control.open", mock_open(mock.open)):
            control.on_save(None)
        expect += [
            call.on_save(None),
            call.open("/path/to/file", "wb"),
            call.open().__enter__(),
            call.pickle.dump(self.app.book, mock.open.return_value),
            call.open().__exit__(None, None, None),
            call.App.book.not_modified(),
        ]

        LOG.info("Filename not set")
        self.app.file_path = None
        control.on_save(None)
        expect += [call.on_save(None), call.on_save_as(None)]

        mock.assert_has_calls(expect)

    @note_func("on_save_as")
    def test_on_save_as(self):
        """Should save configuration under a new name"""
        control = self.window
        mock = self.app._the_mock
        frame = self.app.frame
        control.on_save = mock.on_save
        wx.FileDialog._patch('.GetPath.return_value = "/path/to/file"')

        LOG.info("Filename given")
        wx.FileDialog._patch(".ShowModal.return_value = %d" % wx.ID_OK)
        control.on_save_as(None)
        mock.file_path(self.app.file_path)
        expect = [
            call.on_save_as(None),
            call.FileDialog(
                frame, "Save as?", wildcard="SPK files (*.book)|*.book", style=6
            ),
            call.FileDialog.ShowModal(),
            call.FileDialog.GetPath(),
            call.on_save(None),
            call.App.frame.refresh_file_history(),
            call.FileDialog.Destroy(),
            call.file_path("/path/to/file"),
        ]

        LOG.info("Cancelled")
        wx.FileDialog._patch(".ShowModal.return_value = %d" % wx.ID_CANCEL)
        control.on_save_as(None)
        expect += [
            call.on_save_as(None),
            call.FileDialog(
                frame, "Save as?", wildcard="SPK files (*.book)|*.book", style=6
            ),
            call.FileDialog.ShowModal(),
            call.FileDialog.Destroy(),
        ]

        mock.assert_has_calls(expect)

    @note_func("on_open")
    def test_on_open(self):
        """Should open a file"""
        control = self.window
        mock = self.app._the_mock
        frame = self.app.frame
        control.load = mock.load
        wx.FileDialog._patch('.GetPath.return_value = "/path/to/file"')

        LOG.info("Unsaved file, cancelled")
        self.app.book.is_modified.return_value = True
        wx.MessageDialog._patch(".ShowModal.return_value = %d" % wx.ID_CANCEL)
        control.on_open(None)
        expect = [
            call.App.book.is_modified(),
            call.MessageDialog(
                frame,
                "Changes not saved! Do you want to open a new file without saving?",
                "Permanent Action",
                -2147483372,
            ),
            call.MessageDialog.ShowModal(),
            call.MessageDialog.Destroy(),
        ]

        LOG.info("Okay to discard, file named")
        wx.MessageDialog._patch(".ShowModal.return_value = %d" % wx.ID_OK)
        wx.FileDialog._patch(".ShowModal.return_value = %d" % wx.ID_OK)
        control.on_open(None)
        expect += [
            call.on_open(None),
            call.App.book.is_modified(),
            call.MessageDialog(
                frame,
                "Changes not saved! Do you want to open a new file without saving?",
                "Permanent Action",
                -2147483372,
            ),
            call.MessageDialog.ShowModal(),
            call.MessageDialog.Destroy(),
            call.FileDialog(
                frame, "Open?", wildcard="SPK files (*.book)|*.book", style=1
            ),
            call.FileDialog.ShowModal(),
            call.FileDialog.GetPath(),
            call.load("/path/to/file"),
            call.FileDialog.Destroy(),
        ]

        LOG.info("Cancelled")
        wx.FileDialog._patch(".ShowModal.return_value = %d" % wx.ID_CANCEL)
        control.on_open(None)
        expect += [
            call.on_open(None),
            call.App.book.is_modified(),
            call.MessageDialog(
                frame,
                "Changes not saved! Do you want to open a new file without saving?",
                "Permanent Action",
                -2147483372,
            ),
            call.MessageDialog.ShowModal(),
            call.MessageDialog.Destroy(),
            call.FileDialog(
                frame, "Open?", wildcard="SPK files (*.book)|*.book", style=1
            ),
            call.FileDialog.ShowModal(),
            call.FileDialog.Destroy(),
        ]

        LOG.info("No file to discard")
        self.app.book.is_modified.return_value = False
        control.on_open(None)
        expect += [
            call.on_open(None),
            call.App.book.is_modified(),
            call.FileDialog(
                frame, "Open?", wildcard="SPK files (*.book)|*.book", style=1
            ),
            call.FileDialog.ShowModal(),
            call.FileDialog.Destroy(),
        ]

        mock.assert_has_calls(expect)

    @patch("style_stripper.control.menu_control.pickle")
    @note_func("load")
    def test_load(self, pickle):
        """Should open a file"""
        control = self.window
        mock = self.app._the_mock
        menu_control.pickle = mock.pickle
        mock.pickle.load.return_value = mock.book
        mock.book.init.return_value = self.app.book  # totally cheating

        LOG.info("Book doesn't contain a docx yet and not on options panel")
        self.app.book.is_loaded.return_value = False
        self.app.book.current_panel = PanelType.AUTHOR
        with patch("style_stripper.control.menu_control.open", mock_open(mock.open)):
            control.load("/path/to/file")
        expect = [
            call.load("/path/to/file"),
            call.open("/path/to/file", "rb"),
            call.open().__enter__(),
            call.pickle.load(mock.open.return_value),
            call.book.init(),
            call.open().__exit__(None, None, None),
            call.App.book.is_loaded(),
            call.App.refresh_contents(),
            call.App.book.not_modified(),
            call.App.frame.refresh_file_history(),
        ]

        LOG.info("Loaded a document while on the options panel")
        self.app.book.is_loaded.return_value = True
        self.app.book.current_panel = PanelType.OPTIONS
        with patch("style_stripper.control.menu_control.open", mock_open(mock.open)):
            control.load("/path/to/file")
        mock.app_book(self.app.book)
        expect += [
            call.load("/path/to/file"),
            call.open("/path/to/file", "rb"),
            call.open().__enter__(),
            call.pickle.load(mock.open.return_value),
            call.book.init(),
            call.open().__exit__(None, None, None),
            call.App.book.is_loaded(),
            call.App.book_loaded(),
            call.App.refresh_contents(),
            call.App.book.not_modified(),
            call.App.frame.refresh_file_history(),
            call.App.book.reload(),
            call.App.apply(),
            call.app_book(self.app.book),
        ]

        mock.assert_has_calls(expect)

    @note_func("on_file_history")
    def test_on_file_history(self):
        """Should open a recent file"""
        control = self.window
        mock = self.app._the_mock
        event = wx.MenuEvent()
        event.GetId.return_value = 5055
        control.load = mock.load
        self.app.frame.file_history.GetHistoryFile.return_value = "/path/to/file"

        control.on_file_history(event)
        mock.assert_has_calls(
            [
                call.on_file_history(event),
                call.MenuEvent.GetId(),
                call.App.frame.file_history.GetHistoryFile(4),
                call.load("/path/to/file"),
            ]
        )

    @note_func("on_quit")
    def test_on_quit(self):
        """Should close the frame"""
        control = self.window
        mock = self.app._the_mock

        control.on_quit(None)
        mock.assert_has_calls([call.on_quit(None), call.App.frame.Close()])
