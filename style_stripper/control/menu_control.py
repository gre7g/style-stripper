import pickle
import logging
import wx

from style_stripper.data.book import Book

try:
    from style_stripper.model.main_app import StyleStripperApp
except ImportError:
    StyleStripperApp = None

# Constants:
LOG = logging.getLogger(__name__)


class MenuControl(object):
    def __init__(self, app: StyleStripperApp):
        self.app = app

    def on_new(self, event: wx.MenuEvent):
        if self.app.book.is_modified():
            dialog = wx.MessageDialog(self.app.frame,
                                      "Changes not saved! Do you want to start a new file without saving?",
                                      "Permanent Action", wx.OK | wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_WARNING)
            try:
                if dialog.ShowModal() != wx.ID_OK:
                    return
            finally:
                dialog.Destroy()

        self.app.book = Book(self.app.settings.latest_config)
        self.app.frame.refresh_contents()

    def on_save(self, event: wx.MenuEvent):
        if self.app.settings.file_path:
            try:
                with open(self.app.settings.file_path, "wb") as file_obj:
                    pickle.dump(self.app.book, file_obj)
            except Exception as message:
                dialog = wx.MessageDialog(self.app.frame, "Error: %s" % message, "Save Error", wx.OK | wx.ICON_WARNING)
                try:
                    dialog.ShowModal()
                finally:
                    dialog.Destroy()
            else:
                self.app.book.not_modified()
        else:
            self.on_save_as(event)

    def on_save_as(self, event: wx.MenuEvent):
        dialog = wx.FileDialog(self.app.frame, "Save as?", wildcard="SPK files (*.book)|*.book",
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        try:
            if dialog.ShowModal() == wx.ID_OK:
                self.app.settings.file_path = dialog.GetPath()
                self.on_save(event)
        finally:
            dialog.Destroy()

    def on_open(self, event: wx.MenuEvent):
        if self.app.book.is_modified():
            dialog = wx.MessageDialog(self.app.frame,
                                      "Changes not saved! Do you want to open a new file without saving?",
                                      "Permanent Action", wx.OK | wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_WARNING)
            try:
                if dialog.ShowModal() != wx.ID_OK:
                    return
            finally:
                dialog.Destroy()

        dialog = wx.FileDialog(self.app.frame, "Open?", wildcard="SPK files (*.book)|*.book", style=wx.FD_OPEN)
        try:
            if dialog.ShowModal() == wx.ID_OK:
                self.load(dialog.GetPath())
        finally:
            dialog.Destroy()

    def load(self, path: str):
        self.app.settings.file_path = path
        with open(path, "rb") as file_obj:
            self.app.book = pickle.load(file_obj).init()
        self.app.frame.refresh_contents()
        self.app.book.not_modified()

    def on_quit(self, event: wx.MenuEvent):
        self.app.frame.Close()
