from copy import deepcopy
import logging
import wx

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
        self.double.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(sizer6, 0, wx.TOP, 15)
        sizer6.Add(self.double, 0, 0, 0)
        self.leading = wx.CheckBox(box, label=_("Purge leading"))
        self.leading.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer6.Add(self.leading, 0, wx.LEFT, 20)
        self.trailing = wx.CheckBox(box, label=_("Purge trailing"))
        self.trailing.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer6.Add(self.trailing, 0, wx.LEFT, 20)

        sizer7 = wx.BoxSizer(wx.VERTICAL)
        sizer3.Add(sizer7, 0, wx.EXPAND | wx.LEFT, 10)
        self.italic = wx.CheckBox(self, label=_("Adjust italic to include punctuation"))
        self.italic.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer7.Add(self.italic, 0, wx.TOP, 16)

        self.quotes = wx.CheckBox(self, label=_("Convert quotes to curly"))
        self.quotes.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer7.Add(self.quotes, 0, wx.TOP, 16)

        box = wx.StaticBox(self, label=_("Scene Breaks"))
        sizer3.Add(box, 0, wx.EXPAND | wx.TOP, 16)
        sizer8 = wx.BoxSizer(wx.VERTICAL)
        sizer9 = wx.BoxSizer(wx.VERTICAL)
        sizer8.Add(sizer9, 1, wx.EXPAND | wx.ALL, 10)
        box.SetSizer(sizer8)
        self.blank = wx.CheckBox(box, label=_("Look for blank lines if no other breaks found"))
        self.blank.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer9.Add(self.blank, 0, wx.TOP, 15)
        sizer10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer9.Add(sizer10, 0, wx.EXPAND | wx.TOP, 10)
        self.replace_divider = wx.CheckBox(box, label=_("Replace with:"))
        self.replace_divider.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer10.Add(self.replace_divider, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.divider = wx.TextCtrl(box, value="# # #")
        self.divider.Bind(wx.EVT_TEXT, self.app.frame_controls.on_option)
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
        self.replace_ellipses.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer13.Add(self.replace_ellipses, 0, wx.TOP, 15)
        sizer14 = wx.FlexGridSizer(2, 10, 2)
        sizer13.Add(sizer14, 0, wx.TOP, 5)
        self.ellipses1 = wx.RadioButton(box)
        self.ellipses1.Bind(wx.EVT_RADIOBUTTON, self.app.frame_controls.on_option)
        sizer14.Add(self.ellipses1, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.ellipses1_text = wx.StaticText(box, label="before...after")
        self.ellipses1_text.SetFont(big_font)
        sizer14.Add(self.ellipses1_text, 0, 0, 0)
        self.ellipses2 = wx.RadioButton(box)
        self.ellipses2.Bind(wx.EVT_RADIOBUTTON, self.app.frame_controls.on_option)
        sizer14.Add(self.ellipses2, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.ellipses2_text = wx.StaticText(box, label="before…after")
        self.ellipses2_text.SetFont(big_font)
        sizer14.Add(self.ellipses2_text, 0, 0, 0)
        self.ellipses3 = wx.RadioButton(box)
        self.ellipses3.Bind(wx.EVT_RADIOBUTTON, self.app.frame_controls.on_option)
        sizer14.Add(self.ellipses3, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.ellipses3_text = wx.StaticText(box, label="before\u200a.\u200a.\u200a.\u200aafter")
        self.ellipses3_text.SetFont(big_font)
        sizer14.Add(self.ellipses3_text, 0, 0, 0)
        self.ellipses4 = wx.RadioButton(box)
        self.ellipses4.Bind(wx.EVT_RADIOBUTTON, self.app.frame_controls.on_option)
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
        self.part_chapter.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer17.Add(self.part_chapter, 0, wx.TOP, 7)
        self.style_end = wx.CheckBox(box, label=_('Style "The End"'))
        self.style_end.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer17.Add(self.style_end, 0, wx.TOP, 10)
        sizer18 = wx.BoxSizer(wx.HORIZONTAL)
        sizer17.Add(sizer18, 0, wx.EXPAND | wx.TOP, 7)
        self.add_end = wx.CheckBox(box, label=_("Add if missing:"))
        self.add_end.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer18.Add(self.add_end, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.end = wx.TextCtrl(box, value="The End")
        self.end.Bind(wx.EVT_TEXT, self.app.frame_controls.on_option)
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
        self.breaks.Bind(wx.EVT_CHOICE, self.app.frame_controls.on_option)
        sizer19.Add(self.breaks, 1, wx.LEFT, 5)
        self.indent = wx.CheckBox(box, label=_("Indent first paragraph of scenes"))
        self.indent.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer17.Add(self.indent, 0, wx.TOP, 8)

        box = wx.StaticBox(self, label=_("Dashes and Hyphens"))
        sizer15.Add(box, 1, wx.LEFT, 20)
        sizer20 = wx.BoxSizer(wx.VERTICAL)
        sizer21 = wx.BoxSizer(wx.VERTICAL)
        box.SetSizer(sizer20)
        sizer20.Add(sizer21, 1, wx.EXPAND | wx.ALL, 10)
        self.replace_dashes = wx.CheckBox(box, label=_("Replace dashes"))
        self.replace_dashes.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer21.Add(self.replace_dashes, 0, wx.TOP, 15)
        self.replace_hyphens = wx.CheckBox(box, label=_("Replace double-hyphens (--)"))
        self.replace_hyphens.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer21.Add(self.replace_hyphens, 0, wx.TOP, 12)
        self.hyphen_at_end = wx.CheckBox(box, label=_('Fix hyphen at end of quotes (before-")'))
        self.hyphen_at_end.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer21.Add(self.hyphen_at_end, 0, wx.TOP, 12)
        sizer22 = wx.FlexGridSizer(2, 5, 2)
        sizer21.Add(sizer22, 0, wx.TOP, 10)
        self.en_dash = wx.RadioButton(box)
        self.en_dash.Bind(wx.EVT_RADIOBUTTON, self.app.frame_controls.on_option)
        sizer22.Add(self.en_dash, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        text = wx.StaticText(box, label="before – after")
        text.SetFont(big_font)
        sizer22.Add(text, 0, 0, 0)
        self.em_dash = wx.RadioButton(box)
        self.em_dash.Bind(wx.EVT_RADIOBUTTON, self.app.frame_controls.on_option)
        sizer22.Add(self.em_dash, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        text = wx.StaticText(box, label="before—after")
        text.SetFont(big_font)
        sizer22.Add(text, 0, 0, 0)

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
        self.refresh_contents()

    def refresh_contents(self):
        config = self.app.settings.latest_config
        self.double.SetValue(config[SPACES][PURGE_DOUBLE_SPACES])
        self.leading.SetValue(config[SPACES][PURGE_LEADING_WHITESPACE])
        self.trailing.SetValue(config[SPACES][PURGE_TRAILING_WHITESPACE])
        self.italic.SetValue(config[ITALIC][ADJUST_TO_INCLUDE_PUNCTUATION])
        self.quotes.SetValue(config[QUOTES][CONVERT_TO_CURLY])
        self.blank.SetValue(config[DIVIDER][BLANK_PARAGRAPH_IF_NO_OTHER])
        self.replace_divider.SetValue(config[DIVIDER][REPLACE_WITH_NEW])
        self.divider.Enable(config[DIVIDER][REPLACE_WITH_NEW])
        self.divider.SetValue(config[DIVIDER][NEW])
        enable = config[ELLIPSES][REPLACE_WITH_NEW]
        self.replace_ellipses.SetValue(enable)
        for control in [
            self.ellipses1,
            self.ellipses1_text,
            self.ellipses2,
            self.ellipses2_text,
            self.ellipses3,
            self.ellipses3_text,
            self.ellipses4,
            self.ellipses4_text,
        ]:
            control.Enable(enable)
        if config[ELLIPSES][NEW] == "...":
            self.ellipses1.SetValue(True)
        elif config[ELLIPSES][NEW] == "…":
            self.ellipses2.SetValue(True)
        elif config[ELLIPSES][NEW] == "\u200a.\u200a.\u200a.\u200a":
            self.ellipses3.SetValue(True)
        elif config[ELLIPSES][NEW] == "\u2009.\u2009.\u2009.\u2009":
            self.ellipses3.SetValue(True)
        self.part_chapter.SetValue(config[HEADINGS][STYLE_PARTS_AND_CHAPTER])
        self.style_end.SetValue(config[HEADINGS][STYLE_THE_END])
        self.add_end.SetValue(config[HEADINGS][ADD_THE_END])
        self.end.Enable(config[HEADINGS][ADD_THE_END])
        self.end.SetValue(config[HEADINGS][THE_END])
        if config[HEADINGS][HEADER_FOOTER_AFTER_BREAK]:
            if config[HEADINGS][BREAK_BEFORE_HEADING] == CONTINUOUS:
                self.breaks.SetSelection(0)
            elif config[HEADINGS][BREAK_BEFORE_HEADING] == NEW_PAGE:
                self.breaks.SetSelection(1)
        else:
            if config[HEADINGS][BREAK_BEFORE_HEADING] == NEW_PAGE:
                self.breaks.SetSelection(2)
            elif config[HEADINGS][BREAK_BEFORE_HEADING] == ODD_PAGE:
                self.breaks.SetSelection(3)
            elif config[HEADINGS][BREAK_BEFORE_HEADING] == EVEN_PAGE:
                self.breaks.SetSelection(4)
        self.indent.SetValue(config[STYLING][INDENT_FIRST_PARAGRAPH])
        self.replace_dashes.SetValue(config[DASHES][FORCE_ALL_EN_OR_EM])
        self.replace_hyphens.SetValue(config[DASHES][CONVERT_DOUBLE_DASHES])
        self.hyphen_at_end.SetValue(config[DASHES][FIX_DASH_AT_END_OF_QUOTE])
        if config[DASHES][CONVERT_TO_EN_DASH]:
            self.en_dash.SetValue(True)
        else:
            self.em_dash.SetValue(True)

    def grab_contents(self):
        config = self.app.settings.latest_config
        config_copy = deepcopy(config)
        refresh = False
        config[SPACES][PURGE_DOUBLE_SPACES] = self.double.GetValue()
        config[SPACES][PURGE_LEADING_WHITESPACE] = self.leading.GetValue()
        config[SPACES][PURGE_TRAILING_WHITESPACE] = self.trailing.GetValue()
        config[ITALIC][ADJUST_TO_INCLUDE_PUNCTUATION] = self.italic.GetValue()
        config[QUOTES][CONVERT_TO_CURLY] = self.quotes.GetValue()
        config[DIVIDER][BLANK_PARAGRAPH_IF_NO_OTHER] = self.blank.GetValue()
        if config[DIVIDER][REPLACE_WITH_NEW] != self.replace_divider.GetValue():
            config[DIVIDER][REPLACE_WITH_NEW] = self.replace_divider.GetValue()
            refresh = True
        config[DIVIDER][NEW] = self.divider.GetValue()
        if config[ELLIPSES][REPLACE_WITH_NEW] != self.replace_ellipses.GetValue():
            config[ELLIPSES][REPLACE_WITH_NEW] = self.replace_ellipses.GetValue()
            refresh = True
        if self.ellipses1.GetValue():
            config[ELLIPSES][NEW] = "..."
        elif self.ellipses2.GetValue():
            config[ELLIPSES][NEW] = "…"
        elif self.ellipses3.GetValue():
            config[ELLIPSES][NEW] = "\u200a.\u200a.\u200a.\u200a"
        elif self.ellipses3.GetValue():
            config[ELLIPSES][NEW] = "\u2009.\u2009.\u2009.\u2009"
        config[HEADINGS][STYLE_PARTS_AND_CHAPTER] = self.part_chapter.GetValue()
        config[HEADINGS][STYLE_THE_END] = self.style_end.GetValue()
        if config[HEADINGS][ADD_THE_END] != self.add_end.GetValue():
            config[HEADINGS][ADD_THE_END] = self.add_end.GetValue()
            refresh = True
        config[HEADINGS][THE_END] = self.end.GetValue()
        value = self.breaks.GetSelection()
        if value == 0:
            config[HEADINGS][HEADER_FOOTER_AFTER_BREAK] = True
            config[HEADINGS][BREAK_BEFORE_HEADING] = CONTINUOUS
        elif value == 1:
            config[HEADINGS][HEADER_FOOTER_AFTER_BREAK] = True
            config[HEADINGS][BREAK_BEFORE_HEADING] = NEW_PAGE
        elif value == 2:
            config[HEADINGS][HEADER_FOOTER_AFTER_BREAK] = False
            config[HEADINGS][BREAK_BEFORE_HEADING] = NEW_PAGE
        elif value == 3:
            config[HEADINGS][HEADER_FOOTER_AFTER_BREAK] = False
            config[HEADINGS][BREAK_BEFORE_HEADING] = ODD_PAGE
        elif value == 4:
            config[HEADINGS][HEADER_FOOTER_AFTER_BREAK] = False
            config[HEADINGS][BREAK_BEFORE_HEADING] = EVEN_PAGE
        config[STYLING][INDENT_FIRST_PARAGRAPH]= self.indent.GetValue()
        config[DASHES][FORCE_ALL_EN_OR_EM] = self.replace_dashes.GetValue()
        config[DASHES][CONVERT_DOUBLE_DASHES] = self.replace_hyphens.GetValue()
        config[DASHES][FIX_DASH_AT_END_OF_QUOTE] = self.hyphen_at_end.GetValue()
        config[DASHES][CONVERT_TO_EN_DASH] = self.en_dash.GetValue()
        config[DASHES][CONVERT_TO_EM_DASH] = self.em_dash.GetValue()

        if config != config_copy:
            self.app.book.modified()

        if refresh:
            self.app.frame.refresh_contents()
