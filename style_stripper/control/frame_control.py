from dataclasses import dataclass
import logging
import os
import sys
import wx

from style_stripper.data.enums import PanelType

try:
    from style_stripper.model.main_app import StyleStripperApp
except ImportError:
    StyleStripperApp = None

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


@dataclass
class FrameControl:
    app: StyleStripperApp

    def on_close(self, event: wx.CloseEvent):
        if self.app.book.is_modified():
            dialog = wx.MessageDialog(
                self.app.frame,
                _("Changes not saved! Do you want to exit without saving?"),
                _("Permanent Action"),
                wx.OK | wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_WARNING,
            )
            try:
                if dialog.ShowModal() == wx.ID_OK:
                    event.Skip()
                    self.app.settings_controls.save_settings_on_exit(event)
            finally:
                dialog.Destroy()
        else:
            self.app.settings_controls.save_settings_on_exit(event)

    def on_browse(self, _event: wx.CommandEvent):
        dialog = wx.FileDialog(
            self.app.frame,
            _("Open?"),
            wildcard=_("Word files (*.docx)|*.docx"),
            style=wx.FD_OPEN,
        )
        try:
            if dialog.ShowModal() == wx.ID_OK:
                self.app.book.load(dialog.GetPath())
                self.app.book_loaded()
        finally:
            dialog.Destroy()

    def get_current_panel_num(self) -> int:
        return self.app.book.current_panel.value  # noqa (value is int by design)

    def on_next(self, _event: wx.CommandEvent):
        self.app.book.current_panel = PanelType(self.get_current_panel_num() + 1)
        self.app.refresh_contents()

    def on_prev(self, _event: wx.CommandEvent):
        self.app.book.current_panel = PanelType(self.get_current_panel_num() - 1)
        self.app.refresh_contents()

    def on_author(self, event: wx.CommandEvent):
        author = event.GetString()
        if self.app.book.author != author:
            self.app.book.author = author
            self.app.book.modified()
        event.Skip()

    def on_title(self, event: wx.CommandEvent):
        title = event.GetString()
        if self.app.book.title != title:
            self.app.book.title = title
            self.app.book.modified()
        event.Skip()

    def on_dimensions(self, event: wx.CommandEvent):
        self.app.new_dimensions()
        self.app.refresh_contents()
        event.Skip()

    def on_variant(self, event: wx.ScrollEvent):
        self.app.refresh_contents()
        event.Skip()

    def on_option(self, event: wx.CommandEvent):
        self.app.grab_contents()
        event.Skip()

    def on_reload_and_prev(self, event: wx.CommandEvent):
        self.app.book.reload()
        self.on_prev(event)

    def on_apply_and_next(self, event: wx.CommandEvent):
        self.on_next(event)
        self.app.apply()

    def on_export(self, _event: wx.CommandEvent):
        dialog = wx.FileDialog(
            self.app.frame,
            _("Export as?"),
            wildcard=_("DocX files (*.docx)|*.docx"),
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        )
        try:
            if dialog.ShowModal() == wx.ID_OK:
                path = dialog.GetPath()
                self.app.book.export(path)
                if sys.platform == "win32":
                    os.startfile(path)
        finally:
            dialog.Destroy()
