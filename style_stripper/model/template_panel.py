import wx

from style_stripper.data.constants import CONSTANTS
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
        self.variant = wx.ScrollBar(self)
        self.variant.SetScrollbar(0, 1, 10, 1)
        self.variant.Bind(wx.EVT_SCROLL, self.app.frame_controls.on_variant)
        sizer2.Add(self.variant, 1, wx.LEFT | wx.CENTER, 10)
        self.item = wx.StaticText(self, label=_("1 of 10"))
        sizer2.Add(self.item, 0, wx.LEFT | wx.CENTER, 5)

        add_stretcher(sizer1)

        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(sizer3, 0, wx.EXPAND, 0)
        add_stretcher(sizer3)
        button = wx.Button(self, label=_("Next"))
        button.Bind(wx.EVT_BUTTON, self.app.frame_controls.on_next)
        sizer3.Add(button, 0, 0, 0)

        self.SetSizer(sizer1)

    def refresh_contents(self):
        book = self.app.book
        self.item.SetLabel("%d of 10" % (self.variant.GetThumbPosition() + 1))


if __name__ == "__main__":
    from docx import Document
    d=Document(r"..\docx_templates\5x8+bleed.docx")
    style={style.name:style for style in d.styles}
    normal=style["Normal"]
    section=d.sections[0]
    details = {
        "different_first_page_header_footer": bool(section.different_first_page_header_footer),
        "page_height": section.page_height / CONSTANTS.MEASURING.EMUS_PER_INCH,
        "page_width": section.page_width / CONSTANTS.MEASURING.EMUS_PER_INCH,
        "top_margin": section.top_margin / CONSTANTS.MEASURING.EMUS_PER_INCH,
        "bottom_margin": section.bottom_margin / CONSTANTS.MEASURING.EMUS_PER_INCH,
        "left_margin": section.left_margin / CONSTANTS.MEASURING.EMUS_PER_INCH,
        "right_margin": section.right_margin / CONSTANTS.MEASURING.EMUS_PER_INCH,
        "header_distance": section.header_distance / CONSTANTS.MEASURING.EMUS_PER_INCH,
        "footer_distance": section.footer_distance / CONSTANTS.MEASURING.EMUS_PER_INCH,
        "gutter": section.gutter / CONSTANTS.MEASURING.EMUS_PER_INCH,
        "font": normal.font.name,
        "font_size": normal.font.size / CONSTANTS.MEASURING.EMUS_PER_POINT,
        "italic": bool(normal.font.italic),
        "bold": bool(normal.font.bold),
        "line_spacing": normal.paragraph_format.line_spacing / CONSTANTS.MEASURING.EMUS_PER_INCH,
        "first_line_indent": normal.paragraph_format.first_line_indent / CONSTANTS.MEASURING.EMUS_PER_INCH
    }
    from pprint import pprint
    pprint(details)

# doc.core_properties.comments
# Comment on template:
# 1,395
# 1 first variant of headers and footers
# 395p typ for 100k words
