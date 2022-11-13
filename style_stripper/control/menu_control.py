from dataclasses import dataclass
import pickle
import logging
import wx

from style_stripper.data.book import Book
from style_stripper.data.enums import PanelType

try:
    from style_stripper.model.main_app import StyleStripperApp
except ImportError:
    StyleStripperApp = None

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


@dataclass
class MenuControl:
    app: StyleStripperApp

    def on_new(self, _event: wx.MenuEvent):
        if self.app.book.is_modified():
            dialog = wx.MessageDialog(
                self.app.frame,
                _("Changes not saved! Do you want to start a new file without saving?"),
                _("Permanent Action"),
                wx.OK | wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_WARNING,
            )
            try:
                if dialog.ShowModal() != wx.ID_OK:
                    return
            finally:
                dialog.Destroy()

        self.app.book = Book(self.app.settings.latest_config)
        self.app.file_path = None
        self.app.refresh_contents()

    def on_save(self, event: wx.MenuEvent):
        if self.app.file_path:
            try:
                with open(self.app.file_path, "wb") as file_obj:
                    pickle.dump(self.app.book, file_obj)
            except Exception as message:
                dialog = wx.MessageDialog(
                    self.app.frame,
                    _("Error: %s") % message,
                    _("Save Error"),
                    wx.OK | wx.ICON_WARNING,
                )
                try:
                    dialog.ShowModal()
                finally:
                    dialog.Destroy()
            else:
                self.app.book.not_modified()
        else:
            self.on_save_as(event)

    def on_save_as(self, event: wx.MenuEvent):
        dialog = wx.FileDialog(
            self.app.frame,
            _("Save as?"),
            wildcard=_("SPK files (*.book)|*.book"),
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        )
        try:
            if dialog.ShowModal() == wx.ID_OK:
                self.app.file_path = dialog.GetPath()
                self.on_save(event)
                self.app.frame.refresh_file_history()
        finally:
            dialog.Destroy()

    def on_open(self, _event: wx.MenuEvent):
        if self.app.book.is_modified():
            dialog = wx.MessageDialog(
                self.app.frame,
                _("Changes not saved! Do you want to open a new file without saving?"),
                _("Permanent Action"),
                wx.OK | wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_WARNING,
            )
            try:
                if dialog.ShowModal() != wx.ID_OK:
                    return
            finally:
                dialog.Destroy()

        dialog = wx.FileDialog(
            self.app.frame,
            _("Open?"),
            wildcard=_("SPK files (*.book)|*.book"),
            style=wx.FD_OPEN,
        )
        try:
            if dialog.ShowModal() == wx.ID_OK:
                self.load(dialog.GetPath())
        finally:
            dialog.Destroy()

    def load(self, path: str):
        self.app.file_path = path
        with open(path, "rb") as file_obj:
            self.app.book = pickle.load(file_obj).init()
        if self.app.book.is_loaded():
            self.app.book_loaded()
        if self.app.book.current_panel in [PanelType.REVIEW, PanelType.DONE]:
            LOG.info("Rewind the process to the options panel")
            self.app.book.current_panel = PanelType.OPTIONS
        self.app.refresh_contents()
        self.app.book.not_modified()
        self.app.frame.refresh_file_history()

        if self.app.book.current_panel == PanelType.OPTIONS:
            self.app.book.reload()
            self.app.apply()

    def on_file_history(self, event: wx.MenuEvent):
        self.load(
            self.app.frame.file_history.GetHistoryFile(event.GetId() - wx.ID_FILE1)
        )

    def on_quit(self, _event: wx.MenuEvent):
        self.app.frame.Close()
