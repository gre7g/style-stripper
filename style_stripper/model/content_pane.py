import wx

from style_stripper.data.enums import PanelType

try:
    from style_stripper.model.main_app import StyleStripperApp
except ImportError:
    StyleStripperApp = None


class ContentPanel(wx.Panel):
    app: StyleStripperApp
    PANEL_TYPE: PanelType

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.app = wx.GetApp()

    def is_current_panel(self) -> bool:
        return self.PANEL_TYPE == self.app.book.current_panel

    def refresh_contents(self):
        """Move contents from Book to UI"""
        self.Show(self.is_current_panel())
        self.app.frame.Layout()

    def apply(self):
        pass

    def grab_contents(self):
        """Move contents from UI to Book"""
        pass

    def new_dimensions(self):
        """Adapt to the current window size"""
        pass

    def book_loaded(self, is_loaded: bool = True):
        pass
