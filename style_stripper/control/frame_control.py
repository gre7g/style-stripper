import logging
import wx

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
                self.app.frame.book_loaded()
        finally:
            dialog.Destroy()

    def on_next(self, event: wx.CommandEvent):
        self.app.book.current_page += 1
        self.app.frame.refresh_contents()

    def on_prev(self, event: wx.CommandEvent):
        self.app.book.current_page -= 1
        self.app.frame.refresh_contents()

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
        self.app.frame.new_dimensions()
        self.app.frame.refresh_contents()
        event.Skip()

    def on_variant(self, event: wx.ScrollEvent):
        self.app.frame.refresh_contents()
        event.Skip()

    def on_option(self, event: wx.CommandEvent):
        self.app.frame.grab_contents()
        event.Skip()

    def on_reload(self, event: wx.CommandEvent):
        self.app.book.reload()
        self.on_prev(event)

    def on_apply(self, event: wx.CommandEvent):
        self.on_next(event)
        self.app.frame.apply()

    def on_export(self, event: wx.CommandEvent):
        dialog = wx.FileDialog(self.app.frame, _("Export as?"), wildcard=_("DocX files (*.docx)|*.docx"),
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        try:
            if dialog.ShowModal() == wx.ID_OK:
                self.app.book.export(dialog.GetPath())
        finally:
            dialog.Destroy()
