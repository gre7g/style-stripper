import logging
import wx

from style_stripper.model.utility import add_stretcher

try:
    from style_stripper.model.main_app import StyleStripperApp
except ImportError:
    StyleStripperApp = None

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


class DonePanel(wx.Panel):
    app: StyleStripperApp

    def __init__(self, parent):
        super(DonePanel, self).__init__(parent)
        self.app = wx.GetApp()

        sizer1 = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, label=_('Processing complete! Click the "Export..." button below to save the .docx'))
        sizer1.Add(text, 0, 0, 0)
        button = wx.Button(self, label=_("Export..."))
        button.Bind(wx.EVT_BUTTON, self.app.frame_controls.on_export)
        sizer1.Add(button, 0, wx.TOP, 10)

        add_stretcher(sizer1)
        button = wx.Button(self, label=_("Back (reload document)"))
        button.Bind(wx.EVT_BUTTON, self.app.frame_controls.on_reload)
        sizer1.Add(button, 0, 0, 0)

        self.SetSizer(sizer1)

    def refresh_contents(self):
        pass

