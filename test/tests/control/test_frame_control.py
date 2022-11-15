from mock_wx import wxTestCase, note_func

import logging
import os
import sys
from unittest.mock import call, patch
import wx

from style_stripper.data.enums import PanelType
from style_stripper.control import frame_control

# Constants:
LOG = logging.getLogger(__name__)


class TestFrameControl(wxTestCase):
    def setUp(self) -> None:
        self.app = wx.App()
        self.window = frame_control.FrameControl(self.app)

    @note_func("on_close")
    def test_on_close(self):
        """Should ask about saving before allowing the frame to close"""
        control = self.window
        mock = self.app._the_mock
        frame = self.app.frame

        LOG.info("Book modified, okay to close without saving")
        self.app.book.is_modified.return_value = True
        wx.MessageDialog._patch(".ShowModal.return_value = %d" % wx.ID_OK)
        event = mock.event
        control.on_close(event)
        expect = [
            call.on_close(event),
            call.App.book.is_modified(),
            call.MessageDialog(
                frame,
                "Changes not saved! Do you want to exit without saving?",
                "Permanent Action",
                -2147483372,
            ),
            call.MessageDialog.ShowModal(),
            call.event.Skip(),
            call.App.settings_controls.save_settings_on_exit(event),
            call.MessageDialog.Destroy(),
        ]

        LOG.info("Closing cancelled")
        wx.MessageDialog._patch(".ShowModal.return_value = %d" % wx.ID_CANCEL)
        control.on_close(event)
        expect += [
            call.on_close(event),
            call.App.book.is_modified(),
            call.MessageDialog(
                frame,
                "Changes not saved! Do you want to exit without saving?",
                "Permanent Action",
                -2147483372,
            ),
            call.MessageDialog.ShowModal(),
            call.MessageDialog.Destroy(),
        ]

        LOG.info("Book unmodified")
        self.app.book.is_modified.return_value = False
        control.on_close(event)
        expect += [
            call.on_close(event),
            call.App.book.is_modified(),
            call.App.settings_controls.save_settings_on_exit(event),
        ]

        mock.assert_has_calls(expect)

    @note_func("on_browse")
    def test_on_browse(self):
        """Should browse and load a book"""
        control = self.window
        mock = self.app._the_mock
        frame = self.app.frame

        LOG.info("Book selected")
        wx.FileDialog._patch(".ShowModal.return_value = %d" % wx.ID_OK)
        wx.FileDialog._patch('.GetPath.return_value = "/path/to/file"')
        control.on_browse(None)
        expect = [
            call.on_browse(None),
            call.FileDialog(
                frame, "Open?", wildcard="Word files (*.docx)|*.docx", style=1
            ),
            call.FileDialog.ShowModal(),
            call.FileDialog.GetPath(),
            call.App.book.load("/path/to/file"),
            call.App.book_loaded(),
            call.FileDialog.Destroy(),
        ]

        LOG.info("Cancelled")
        wx.FileDialog._patch(".ShowModal.return_value = %d" % wx.ID_CANCEL)
        control.on_browse(None)
        expect += [
            call.on_browse(None),
            call.FileDialog(
                frame, "Open?", wildcard="Word files (*.docx)|*.docx", style=1
            ),
            call.FileDialog.ShowModal(),
            call.FileDialog.Destroy(),
        ]

        mock.assert_has_calls(expect)

    @note_func("get_current_panel_num")
    @note_func("on_next")
    @note_func("on_prev")
    def test_next_prev(self):
        """Should navigate panels"""
        control = self.window
        mock = self.app._the_mock
        self.app.book.current_panel = PanelType.OPTIONS

        LOG.info("Next")
        control.on_next(None)
        mock.current_panel(self.app.book.current_panel)
        expect = [
            call.on_next(None),
            call.get_current_panel_num(),
            call.get_current_panel_num_return_value(3),
            call.App.refresh_contents(),
            call.current_panel(PanelType.REVIEW),
        ]

        LOG.info("Prev")
        control.on_prev(None)
        mock.current_panel(self.app.book.current_panel)
        expect += [
            call.on_prev(None),
            call.get_current_panel_num(),
            call.get_current_panel_num_return_value(4),
            call.App.refresh_contents(),
            call.current_panel(PanelType.OPTIONS),
        ]

        mock.assert_has_calls(expect)

    @note_func("on_author")
    def test_on_author(self):
        """Should update author"""
        control = self.window
        mock = self.app._the_mock
        self.app.book.author = "Author Name"
        event = wx.CommandEvent()

        LOG.info("Modified")
        event.GetString.return_value = "Jimbo"
        control.on_author(event)
        expect = [
            call.on_author(event),
            call.CommandEvent.GetString(),
            call.App.book.modified(),
            call.CommandEvent.Skip(),
        ]

        LOG.info("Not modified")
        control.on_author(event)
        expect += [
            call.on_author(event),
            call.CommandEvent.GetString(),
            call.CommandEvent.Skip(),
        ]

        mock.assert_has_calls(expect)

    @note_func("on_title")
    def test_on_title(self):
        """Should update title"""
        control = self.window
        mock = self.app._the_mock
        self.app.book.title = "Book Title"
        event = wx.CommandEvent()

        LOG.info("Modified")
        event.GetString.return_value = "Jimbo's Adventures"
        control.on_title(event)
        expect = [
            call.on_title(event),
            call.CommandEvent.GetString(),
            call.App.book.modified(),
            call.CommandEvent.Skip(),
        ]

        LOG.info("Not modified")
        control.on_title(event)
        expect += [
            call.on_title(event),
            call.CommandEvent.GetString(),
            call.CommandEvent.Skip(),
        ]

        mock.assert_has_calls(expect)

    @note_func("on_dimensions")
    @note_func("on_variant")
    @note_func("on_option")
    @note_func("on_reload_and_prev")
    @note_func("on_apply_and_next")
    def test_simple(self):
        """Should test some simple handlers"""
        control = self.window
        mock = self.app._the_mock
        control.on_prev = mock.on_prev
        control.on_next = mock.on_next
        event = wx.CommandEvent()

        LOG.info("Dimensions changed")
        control.on_dimensions(event)
        expect = [
            call.on_dimensions(event),
            call.App.new_dimensions(),
            call.App.refresh_contents(),
            call.CommandEvent.Skip(),
        ]

        LOG.info("Variant changed")
        control.on_variant(event)
        expect += [
            call.on_variant(event),
            call.App.refresh_contents(),
            call.CommandEvent.Skip(),
        ]

        LOG.info("Option changed")
        control.on_option(event)
        expect += [
            call.on_option(event),
            call.App.grab_contents(),
            call.CommandEvent.Skip(),
        ]

        LOG.info("Reload and prev")
        control.on_reload_and_prev(event)
        expect += [
            call.on_reload_and_prev(event),
            call.App.book.reload(),
            call.on_prev(event),
        ]

        LOG.info("Changes applied")
        control.on_apply_and_next(event)
        expect += [call.on_apply_and_next(event), call.on_next(event), call.App.apply()]

        mock.assert_has_calls(expect)

    @patch("sys.platform")
    @patch("os.startfile")
    @note_func("on_export")
    def test_on_export(self, startfile, platform):
        """Should export file"""
        control = self.window
        mock = self.app._the_mock
        frame = self.app.frame
        wx.FileDialog._patch('.GetPath.return_value = "/path/to/file"')
        os.startfile = mock.startfile
        event = wx.CommandEvent()

        LOG.info("Export on Windows")
        wx.FileDialog._patch(".ShowModal.return_value = %d" % wx.ID_OK)
        sys.platform = "win32"
        control.on_export(event)
        expect = [
            call.on_export(event),
            call.FileDialog(
                frame, "Export as?", wildcard="DocX files (*.docx)|*.docx", style=6
            ),
            call.FileDialog.ShowModal(),
            call.FileDialog.GetPath(),
            call.App.book.export("/path/to/file"),
            call.startfile("/path/to/file"),
            call.FileDialog.Destroy(),
        ]

        LOG.info("Export on Linux")
        sys.platform = "linux"
        control.on_export(event)
        expect += [
            call.on_export(event),
            call.FileDialog(
                frame, "Export as?", wildcard="DocX files (*.docx)|*.docx", style=6
            ),
            call.FileDialog.ShowModal(),
            call.FileDialog.GetPath(),
            call.App.book.export("/path/to/file"),
            call.FileDialog.Destroy(),
        ]

        LOG.info("Cancelled")
        wx.FileDialog._patch(".ShowModal.return_value = %d" % wx.ID_OK)
        control.on_export(event)
        expect += [
            call.on_export(event),
            call.FileDialog(
                frame, "Export as?", wildcard="DocX files (*.docx)|*.docx", style=6
            ),
            call.FileDialog.ShowModal(),
            call.FileDialog.GetPath(),
            call.App.book.export("/path/to/file"),
            call.FileDialog.Destroy(),
        ]

        mock.assert_has_calls(expect)
