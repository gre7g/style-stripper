import logging
from typing import List, Tuple, Union, Optional
import wx

from style_stripper.data.constants import CONSTANTS
from style_stripper.data.enums import *
from style_stripper.model.utility import add_stretcher

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
        self.app = wx.GetApp()
        big_font = wx.Font(
            20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName="Times New Roman"
        )

        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(sizer2, 0, wx.EXPAND, 0)
        sizer3 = wx.BoxSizer(wx.VERTICAL)
        sizer2.Add(sizer3, 1, wx.EXPAND, 0)
        box = wx.StaticBox(self, label=_("Spaces"))
        sizer3.Add(box, 0, wx.EXPAND, 0)
        sizer4 = wx.BoxSizer(wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.VERTICAL)
        sizer4.Add(sizer5, 1, wx.EXPAND | wx.ALL, 10)
        box.SetSizer(sizer4)
        self.double = wx.CheckBox(box, label=_("Purge double"))
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(sizer6, 0, wx.TOP, 15)
        sizer6.Add(self.double, 0, 0, 0)
        self.leading = wx.CheckBox(box, label=_("Purge leading"))
        sizer6.Add(self.leading, 0, wx.LEFT, 20)
        self.trailing = wx.CheckBox(box, label=_("Purge trailing"))
        sizer6.Add(self.trailing, 0, wx.LEFT, 20)

        sizer7 = wx.BoxSizer(wx.VERTICAL)
        sizer3.Add(sizer7, 0, wx.EXPAND | wx.LEFT, 10)
        self.italic = wx.CheckBox(self, label=_("Adjust italic to include punctuation"))
        sizer7.Add(self.italic, 0, wx.TOP, 16)

        self.quotes = wx.CheckBox(self, label=_("Convert quotes to curly"))
        sizer7.Add(self.quotes, 0, wx.TOP, 16)

        box = wx.StaticBox(self, label=_("Scene breaks"))
        sizer3.Add(box, 0, wx.EXPAND | wx.TOP, 16)
        sizer8 = wx.BoxSizer(wx.VERTICAL)
        sizer9 = wx.BoxSizer(wx.VERTICAL)
        sizer8.Add(sizer9, 1, wx.EXPAND | wx.ALL, 10)
        box.SetSizer(sizer8)
        self.blank = wx.CheckBox(box, label=_("Look for blank lines if no other breaks found"))
        sizer9.Add(self.blank, 0, wx.TOP, 15)
        sizer10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer9.Add(sizer10, 0, wx.EXPAND | wx.TOP, 10)
        self.replace_divider = wx.CheckBox(box, label=_("Replace with:"))
        sizer10.Add(self.replace_divider, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.divider = wx.TextCtrl(box, value="# # #")
        sizer10.Add(self.divider, 1, 0, 0)

        sizer11 = wx.BoxSizer(wx.VERTICAL)
        sizer2.Add(sizer11, 1, wx.EXPAND | wx.LEFT, 20)
        box = wx.StaticBox(self, label=_("Ellipses"))
        sizer11.Add(box, 0, wx.EXPAND, 0)
        sizer12 = wx.BoxSizer(wx.VERTICAL)
        sizer13 = wx.BoxSizer(wx.VERTICAL)
        box.SetSizer(sizer12)
        sizer12.Add(sizer13, 1, wx.EXPAND | wx.ALL, 10)
        self.replace_ellipses = wx.CheckBox(box, label=_("Replace with:"))
        sizer13.Add(self.replace_ellipses, 0, wx.TOP, 15)
        sizer14 = wx.FlexGridSizer(2, 10, 2)
        sizer13.Add(sizer14, 0, wx.TOP, 5)
        self.ellipses1 = wx.RadioButton(box)
        sizer14.Add(self.ellipses1, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.ellipses1_text = wx.StaticText(box, label="before...after")
        self.ellipses1_text.SetFont(big_font)
        sizer14.Add(self.ellipses1_text, 0, 0, 0)
        self.ellipses2 = wx.RadioButton(box)
        sizer14.Add(self.ellipses2, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.ellipses2_text = wx.StaticText(box, label="before…after")
        self.ellipses2_text.SetFont(big_font)
        sizer14.Add(self.ellipses2_text, 0, 0, 0)
        self.ellipses3 = wx.RadioButton(box)
        sizer14.Add(self.ellipses3, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.ellipses3_text = wx.StaticText(box, label="before\u200a.\u200a.\u200a.\u200aafter")
        self.ellipses3_text.SetFont(big_font)
        sizer14.Add(self.ellipses3_text, 0, 0, 0)
        self.ellipses4 = wx.RadioButton(box)
        sizer14.Add(self.ellipses4, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.ellipses4_text = wx.StaticText(box, label="before\u2009.\u2009.\u2009.\u2009after")
        self.ellipses4_text.SetFont(big_font)
        sizer14.Add(self.ellipses4_text, 0, 0, 0)

        sizer15 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(sizer15, 0, wx.EXPAND | wx.TOP, 10)
        box = wx.StaticBox(self, label=_("Headings"))
        sizer15.Add(box, 1, 0, 0)
        sizer16 = wx.BoxSizer(wx.VERTICAL)
        sizer17 = wx.BoxSizer(wx.VERTICAL)
        box.SetSizer(sizer16)
        sizer16.Add(sizer17, 1, wx.EXPAND | wx.ALL, 10)
        self.template_headings = wx.StaticText(box, label=_("Selected template supports both parts and chapters"))
        sizer17.Add(self.template_headings, 0, wx.TOP, 15)
        self.part_chapter = wx.CheckBox(box, label=_("Style parts and chapters"))
        sizer17.Add(self.part_chapter, 0, wx.TOP, 7)
        self.style_end = wx.CheckBox(box, label=_('Style "The End"'))
        sizer17.Add(self.style_end, 0, wx.TOP, 10)
        sizer18 = wx.BoxSizer(wx.HORIZONTAL)
        sizer17.Add(sizer18, 0, wx.EXPAND | wx.TOP, 7)
        self.add_end = wx.CheckBox(box, label=_("Add if missing:"))
        sizer18.Add(self.add_end, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.end = wx.TextCtrl(box, value="The End")
        sizer18.Add(self.end, 1, 0, 0)
        sizer19 = wx.BoxSizer(wx.HORIZONTAL)
        sizer17.Add(sizer19, 0, wx.EXPAND | wx.TOP, 10)
        self.breaks_text = wx.StaticText(box, label=_("Page breaks:"))
        sizer19.Add(self.breaks_text, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.breaks = wx.Choice(
            box,
            choices=[
                "Continuous (no breaks before part/chapter text)",
                "Next page (keep headers/footers on first page of part/chapter)",
                "Next page (no headers/footers on first page of part/chapter)",
                "Odd page (no headers/footers on first page of part/chapter)",
                "Even page (no headers/footers on first page of part/chapter)",
            ],
        )
        sizer19.Add(self.breaks, 1, wx.LEFT, 5)
        self.indent = wx.CheckBox(box, label=_("Indent first paragraph of scenes"))
        sizer17.Add(self.indent, 0, wx.TOP, 8)

        box = wx.StaticBox(self, label=_("Dashes and Hyphens"))
        sizer15.Add(box, 1, wx.LEFT, 20)
        sizer20 = wx.BoxSizer(wx.VERTICAL)
        sizer21 = wx.BoxSizer(wx.VERTICAL)
        box.SetSizer(sizer20)
        sizer20.Add(sizer21, 1, wx.EXPAND | wx.ALL, 10)
        self.replace_dashes = wx.CheckBox(box, label=_("Replace dashes"))
        sizer21.Add(self.replace_dashes, 0, wx.TOP, 15)
        self.replace_hyphens = wx.CheckBox(box, label=_("Replace double-hyphens (--)"))
        sizer21.Add(self.replace_hyphens, 0, wx.TOP, 12)
        self.hyphen_at_end = wx.CheckBox(box, label=_('Fix hyphen at end of quotes (before-")'))
        sizer21.Add(self.hyphen_at_end, 0, wx.TOP, 12)
        sizer22 = wx.FlexGridSizer(2, 5, 2)
        sizer21.Add(sizer22, 0, wx.TOP, 10)
        self.en_dash = wx.RadioButton(box)
        sizer22.Add(self.en_dash, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.en_dash_text = wx.StaticText(box, label="before – after")
        self.en_dash_text.SetFont(big_font)
        sizer22.Add(self.en_dash_text, 0, 0, 0)
        self.em_dash = wx.RadioButton(box)
        sizer22.Add(self.em_dash, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.em_dash_text = wx.StaticText(box, label="before—after")
        self.em_dash_text.SetFont(big_font)
        sizer22.Add(self.em_dash_text, 0, 0, 0)

        add_stretcher(sizer1)
        sizer23 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(sizer23, 0, wx.EXPAND | wx.TOP, 10)
        button = wx.Button(self, label=_("Prev"))
        button.Bind(wx.EVT_BUTTON, self.app.frame_controls.on_prev)
        sizer23.Add(button, 0, 0, 0)
        add_stretcher(sizer23)
        button = wx.Button(self, label=_("Next"))
        button.Bind(wx.EVT_BUTTON, self.app.frame_controls.on_next)
        sizer23.Add(button, 0, 0, 0)

        self.SetSizer(sizer1)

    def refresh_contents(self):
        pass
