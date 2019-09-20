import wx

from style_stripper.data.enums import *
from style_stripper.data.template_details import fetch_docx_details
from style_stripper.model.preview_panel import PreviewPanel
from style_stripper.model.utility import add_stretcher

try:
    from style_stripper.model.main_app import StyleStripperApp
except ImportError:
    StyleStripperApp = None

# Constants:
_ = wx.GetTranslation
DIMENSIONS = [
    '5" x 8"', '5.06" x 7.81"', '5.25" x 8"', '5.5" x 8.5"', '6" x 9"', '6.14" x 9.21"', '6.69" x 9.61"', '7" x 10"',
    '7.44" x 9.69"', '7.5" x 9.25"', '8" x 10"', '8.25" x 6"', '8.25" x 8.25"', '8.5" x 11"', '8.27" x 11.69"'
]


class TemplatePanel(wx.Panel):
    app: StyleStripperApp

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.app = wx.GetApp()

        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(sizer2, 0, wx.EXPAND)
        text = wx.StaticText(self, label=_("Dimensions:"))
        sizer2.Add(text, 0, wx.CENTER)
        self.dimensions = wx.Choice(self, choices=DIMENSIONS)
        self.dimensions.Bind(wx.EVT_CHOICE, self.app.frame_controls.on_dimensions)
        self.dimensions.SetSelection(0)
        sizer2.Add(self.dimensions, 0, wx.LEFT | wx.CENTER, 5)
        add_stretcher(sizer2)
        self.bleed = wx.StaticText(self, label=_("Bleed"))
        sizer2.Add(self.bleed, 0, wx.CENTER, 0)
        add_stretcher(sizer2)
        text = wx.StaticText(self, label=_("Variant:"))
        sizer2.Add(text, 0, wx.CENTER, 0)
        panel = wx.Panel(self, style=wx.BORDER_THEME)
        sizer2b = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer2b)
        self.variant = wx.ScrollBar(panel, style=wx.SB_HORIZONTAL)
        self.variant.SetScrollbar(0, 1, 10, 1)
        self.variant.Bind(wx.EVT_SCROLL, self.app.frame_controls.on_variant)
        sizer2b.Add(self.variant, 1, wx.EXPAND)
        sizer2.Add(panel, 1, wx.LEFT | wx.CENTER, 10)
        self.item = wx.StaticText(self, label=_("1 of 10"))
        sizer2.Add(self.item, 0, wx.LEFT | wx.CENTER, 5)

        self.preview = PreviewPanel(self)
        self.preview.set_template_dict(fetch_docx_details(r"..\docx_templates\5x8+bleed.docx"))
        self.preview.set_contents(OPEN_TO_PART, [SCOPE_ON_EVEN_HEADER, SCOPE_ON_EVEN_HEADER, SCOPE_ON_LEFT_MARGIN])
        sizer1.Add(self.preview, 1, wx.EXPAND | wx.TOP, 10)

        panel = wx.Panel(self, style=wx.BORDER_THEME)
        sizer2a = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer2a)
        page = wx.ScrollBar(panel, style=wx.SB_HORIZONTAL)
        page.SetScrollbar(0, 1, 5, 1)
        sizer2a.Add(page, 1, wx.EXPAND)
        sizer1.Add(panel, 0, wx.EXPAND | wx.TOP, 5)

        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(sizer3, 0, wx.EXPAND | wx.TOP, 10)
        button = wx.Button(self, label=_("Prev"))
        button.Bind(wx.EVT_BUTTON, self.app.frame_controls.on_prev)
        sizer3.Add(button, 0, 0, 0)
        add_stretcher(sizer3)
        text = wx.StaticText(self, label=_("Estimated pages with this template:"))
        sizer3.Add(text, 0, wx.CENTER, 0)
        text = wx.StaticText(self, label=_("395"))
        sizer3.Add(text, 0, wx.CENTER | wx.LEFT, 5)
        add_stretcher(sizer3)
        button = wx.Button(self, label=_("Next"))
        button.Bind(wx.EVT_BUTTON, self.app.frame_controls.on_next)
        sizer3.Add(button, 0, 0, 0)

        self.SetSizer(sizer1)

    def refresh_contents(self):
        book = self.app.book
        self.item.SetLabel("%d of 10" % (self.variant.GetThumbPosition() + 1))


if __name__ == "__main__":
    from pprint import pprint
    pprint(fetch_docx_details(r"..\docx_templates\5x8+bleed.docx"))

# doc.core_properties.comments
# Comment on template:
# 1,395
# 1 first variant of headers and footers
# 395p typ for 100k words
