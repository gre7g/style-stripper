import logging
from typing import List, Tuple, Union, Optional
import wx

from style_stripper.data.constants import CONSTANTS
from style_stripper.data.enums import *

try:
    from style_stripper.model.main_app import StyleStripperApp
except ImportError:
    StyleStripperApp = None

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


class OptionsPanel(wx.Panel):
    app: StyleStripperApp

    def __init__(self, parent):
        super(OptionsPanel, self).__init__(parent)
        big_font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName="Times New Roman")

        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1a = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(sizer1a, 0, wx.EXPAND, 0)
        sizer1b = wx.BoxSizer(wx.VERTICAL)
        sizer1a.Add(sizer1b, 1, wx.EXPAND, 0)
        box = wx.StaticBox(self, label=_("Spaces"))
        sizer1b.Add(box, 0, wx.EXPAND, 0)
        sizer2 = wx.BoxSizer(wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.VERTICAL)
        sizer2.Add(sizer3, 1, wx.EXPAND | wx.ALL, 10)
        box.SetSizer(sizer2)
        self.double = wx.CheckBox(box, label=_("Purge double"))
        sizer3a = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(sizer3a, 0, wx.TOP, 15)
        sizer3a.Add(self.double, 0, 0, 0)
        self.leading = wx.CheckBox(box, label=_("Purge leading"))
        sizer3a.Add(self.leading, 0, wx.LEFT, 20)
        self.trailing = wx.CheckBox(box, label=_("Purge trailing"))
        sizer3a.Add(self.trailing, 0, wx.LEFT, 20)

        sizer12 = wx.BoxSizer(wx.VERTICAL)
        sizer1b.Add(sizer12, 0, wx.EXPAND | wx.LEFT, 10)
        self.italic = wx.CheckBox(self, label=_("Adjust italic to include punctuation"))
        sizer12.Add(self.italic, 0, wx.TOP, 16)

        self.quotes = wx.CheckBox(self, label=_("Convert quotes to curly"))
        sizer12.Add(self.quotes, 0, wx.TOP, 16)

        box = wx.StaticBox(self, label=_("Scene breaks"))
        sizer1b.Add(box, 0, wx.EXPAND | wx.TOP, 16)
        sizer4 = wx.BoxSizer(wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.VERTICAL)
        sizer4.Add(sizer5, 1, wx.EXPAND | wx.ALL, 10)
        box.SetSizer(sizer4)
        self.blank = wx.CheckBox(box, label=_("Look for blank lines if no other breaks found"))
        sizer5.Add(self.blank, 0, wx.TOP, 15)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(sizer6, 0, wx.EXPAND | wx.TOP, 10)
        self.replace_divider = wx.CheckBox(box, label=_("Replace with:"))
        sizer6.Add(self.replace_divider, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.divider = wx.TextCtrl(box, value="# # #")
        sizer6.Add(self.divider, 1, wx.LEFT, 0)

        sizer1c = wx.BoxSizer(wx.VERTICAL)
        sizer1a.Add(sizer1c, 1, wx.EXPAND | wx.LEFT, 20)
        box = wx.StaticBox(self, label=_("Ellipses"))
        sizer1c.Add(box, 0, wx.EXPAND, 0)
        sizer7 = wx.BoxSizer(wx.VERTICAL)
        sizer8 = wx.BoxSizer(wx.VERTICAL)
        box.SetSizer(sizer7)
        sizer7.Add(sizer8, 1, wx.EXPAND | wx.ALL, 10)
        self.replace_ellipses = wx.CheckBox(box, label=_("Replace with:"))
        sizer8.Add(self.replace_ellipses, 0, wx.TOP, 15)
        sizer9 = wx.FlexGridSizer(2, 10, 2)
        sizer8.Add(sizer9, 0, wx.TOP, 5)
        self.ellipses1 = wx.RadioButton(box)
        sizer9.Add(self.ellipses1, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.ellipses1_text = wx.StaticText(box, label="before...after")
        self.ellipses1_text.SetFont(big_font)
        sizer9.Add(self.ellipses1_text, 0, 0, 0)
        self.ellipses2 = wx.RadioButton(box)
        sizer9.Add(self.ellipses2, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.ellipses2_text = wx.StaticText(box, label="before…after")
        self.ellipses2_text.SetFont(big_font)
        sizer9.Add(self.ellipses2_text, 0, 0, 0)
        self.ellipses3 = wx.RadioButton(box)
        sizer9.Add(self.ellipses3, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.ellipses3_text = wx.StaticText(box, label="before\u200a.\u200a.\u200a.\u200aafter")
        self.ellipses3_text.SetFont(big_font)
        sizer9.Add(self.ellipses3_text, 0, 0, 0)
        self.ellipses4 = wx.RadioButton(box)
        sizer9.Add(self.ellipses4, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.ellipses4_text = wx.StaticText(box, label="before\u2009.\u2009.\u2009.\u2009after")
        self.ellipses4_text.SetFont(big_font)
        sizer9.Add(self.ellipses4_text, 0, 0, 0)

        # box = wx.StaticBox(self, label=_("Headings"))
        # sizer1.Add(box, 0, wx.EXPAND | wx.TOP, 10)
        # sizer10 = wx.BoxSizer(wx.VERTICAL)
        # sizer11 = wx.BoxSizer(wx.VERTICAL)
        # box.SetSizer(sizer10)
        # sizer10.Add(sizer11, 1, wx.EXPAND | wx.ALL, 10)
        # self.template_headings = wx.StaticText(box, label=_("Selected template supports both parts and chapters"))
        # sizer11.Add(self.template_headings, 0, wx.TOP, 10)
        # self.part_chapter = wx.CheckBox(box, label=_("Style parts and chapters"))
        # sizer11.Add(self.replace_ellipses, 0, wx.TOP, 15)

        self.SetSizer(sizer1)

    def refresh_contents(self):
        pass
