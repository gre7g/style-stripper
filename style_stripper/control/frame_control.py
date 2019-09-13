import logging
import wx

# Constants:
LOG = logging.getLogger(__name__)


class FrameControl(object):
    def __init__(self, app):
        self.app = app
        self._deselect_protect = None

    def on_close(self, event):
        if self.app.book.is_modified():
            dialog = wx.MessageDialog(self.app.frame, "Changes not saved! Do you want to exit without saving?",
                                      "Permanent Action", wx.OK | wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_WARNING)
            try:
                if dialog.ShowModal() == wx.ID_OK:
                    event.Skip()
                    self.app.settings_controls.save_settings_on_exit(event)
            finally:
                dialog.Destroy()
        else:
            self.app.settings_controls.save_settings_on_exit(event)

    def on_browse(self, event):
        LOG.debug("browse")

    def on_next(self, event):
        LOG.debug("next")
