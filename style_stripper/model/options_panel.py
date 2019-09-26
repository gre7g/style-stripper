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

        sizer1 = wx.BoxSizer(wx.VERTICAL)
        box = wx.StaticBox(self, label=_("Spaces"))
        sizer1.Add(box, 0, wx.EXPAND, 0)
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

        self.italic = wx.CheckBox(self, label=_("Adjust italic to include punctuation"))
        sizer1.Add(self.italic, 0, wx.TOP | wx.LEFT, 10)

        self.quotes = wx.CheckBox(self, label=_("Convert quotes to curly"))
        sizer1.Add(self.quotes, 0, wx.TOP | wx.LEFT, 10)

        box = wx.StaticBox(self, label=_("Scene breaks"))
        sizer1.Add(box, 0, wx.EXPAND | wx.TOP, 10)
        sizer4 = wx.BoxSizer(wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.VERTICAL)
        sizer4.Add(sizer5, 1, wx.EXPAND | wx.ALL, 10)
        box.SetSizer(sizer4)
        self.blank = wx.CheckBox(box, label=_("Look for blank lines if no other breaks found"))
        sizer5.Add(self.blank, 0, wx.TOP, 15)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(sizer6, 0, wx.EXPAND | wx.TOP, 10)
        self.replace = wx.CheckBox(box, label=_("Replace with:"))
        sizer6.Add(self.replace, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.replace_with = wx.TextCtrl(box, value="# # #")
        sizer6.Add(self.replace_with, 1, wx.LEFT, 0)

        self.SetSizer(sizer1)

    def refresh_contents(self):
        pass
