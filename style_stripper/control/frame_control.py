import logging
import wx

from style_stripper.data.enums import *

try:
    from style_stripper.model.main_app import StyleStripperApp
except ImportError:
    StyleStripperApp = None

# Constants:
_ = wx.GetTranslation
LOG = logging.getLogger(__name__)


class FrameControl(object):
    def __init__(self, app: StyleStripperApp):
        self.app: StyleStripperApp = app
        self._deselect_protect = None

    def on_close(self, event: wx.Event):
        if self.app.book.is_modified():
            dialog = wx.MessageDialog(self.app.frame, _("Changes not saved! Do you want to exit without saving?"),
                                      _("Permanent Action"), wx.OK | wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_WARNING)
            try:
                if dialog.ShowModal() == wx.ID_OK:
                    event.Skip()
                    self.app.settings_controls.save_settings_on_exit(event)
            finally:
                dialog.Destroy()
        else:
            self.app.settings_controls.save_settings_on_exit(event)

    def on_browse(self, event: wx.CommandEvent):
        dialog = wx.FileDialog(self.app.frame, _("Open?"), wildcard=_("Word files (*.docx)|*.docx"), style=wx.FD_OPEN)
        try:
            if dialog.ShowModal() == wx.ID_OK:
                self.app.book.load(dialog.GetPath())
        finally:
            dialog.Destroy()

    def on_next(self, event: wx.CommandEvent):
        LOG.debug("next")

    def on_author(self, event: wx.CommandEvent):
        self.app.book.config[SOURCE][AUTHOR] = event.GetString()
        self.app.book.modified()
        event.Skip()

    def on_title(self, event: wx.CommandEvent):
        self.app.book.config[SOURCE][TITLE] = event.GetString()
        self.app.book.modified()
        event.Skip()