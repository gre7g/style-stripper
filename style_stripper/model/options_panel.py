from copy import deepcopy
import logging
import wx

from style_stripper.data.enums import PaginationType, PanelType
from style_stripper.model.content_panel import ContentPanel
from style_stripper.model.utility import add_stretcher

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


class OptionsPanel(ContentPanel):
    PANEL_TYPE = PanelType.OPTIONS
    double: wx.CheckBox
    leading: wx.CheckBox
    trailing: wx.CheckBox
    italic: wx.CheckBox
    quotes: wx.CheckBox
    blank: wx.CheckBox
    replace_divider: wx.CheckBox
    divider: wx.TextCtrl
    replace_ellipses: wx.CheckBox
    ellipses1: wx.RadioButton
    ellipses1_text: wx.StaticText
    ellipses2: wx.RadioButton
    ellipses2_text: wx.StaticText
    ellipses3: wx.RadioButton
    ellipses3_text: wx.StaticText
    ellipses4: wx.RadioButton
    ellipses4_text: wx.StaticText
    template_headings = wx.StaticText
    part_chapter = wx.CheckBox
    style_end = wx.CheckBox
    add_end = wx.CheckBox
    end = wx.TextCtrl
    breaks_text = wx.StaticText
    breaks = wx.Choice
    indent = wx.CheckBox
    replace_dashes = wx.CheckBox
    replace_hyphens = wx.CheckBox
    hyphen_at_end = wx.CheckBox
    en_dash = wx.RadioButton
    em_dash = wx.RadioButton

    def __init__(self, *args, **kwargs):
        super(OptionsPanel, self).__init__(*args, **kwargs)
        big_font = wx.Font(
            20,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
            faceName="Times New Roman",
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
        self.double = wx.CheckBox(box, label=_("Purge double"), name="double")
        self.double.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(sizer6, 0, wx.TOP, 15)
        sizer6.Add(self.double, 0, 0, 0)
        self.leading = wx.CheckBox(box, label=_("Purge leading"), name="leading")
        self.leading.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer6.Add(self.leading, 0, wx.LEFT, 20)
        self.trailing = wx.CheckBox(box, label=_("Purge trailing"), name="trailing")
        self.trailing.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer6.Add(self.trailing, 0, wx.LEFT, 20)

        sizer7 = wx.BoxSizer(wx.VERTICAL)
        sizer3.Add(sizer7, 0, wx.EXPAND | wx.LEFT, 10)
        self.italic = wx.CheckBox(
            self, label=_("Adjust italic to include punctuation"), name="italic"
        )
        self.italic.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer7.Add(self.italic, 0, wx.TOP, 16)

        self.quotes = wx.CheckBox(
            self, label=_("Convert quotes to curly"), name="quotes"
        )
        self.quotes.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer7.Add(self.quotes, 0, wx.TOP, 16)

        box = wx.StaticBox(self, label=_("Scene Breaks"))
        sizer3.Add(box, 0, wx.EXPAND | wx.TOP, 16)
        sizer8 = wx.BoxSizer(wx.VERTICAL)
        sizer9 = wx.BoxSizer(wx.VERTICAL)
        sizer8.Add(sizer9, 1, wx.EXPAND | wx.ALL, 10)
        box.SetSizer(sizer8)
        self.blank = wx.CheckBox(
            box, label=_("Look for blank lines if no other breaks found"), name="blank"
        )
        self.blank.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer9.Add(self.blank, 0, wx.TOP, 15)
        sizer10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer9.Add(sizer10, 0, wx.EXPAND | wx.TOP, 10)
        self.replace_divider = wx.CheckBox(
            box, label=_("Replace with:"), name="replace_divider"
        )
        self.replace_divider.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer10.Add(self.replace_divider, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.divider = wx.TextCtrl(box, value="# # #", name="divider")
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
        self.replace_ellipses = wx.CheckBox(
            box, label=_("Replace with:"), name="replace_ellipses"
        )
        self.replace_ellipses.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer13.Add(self.replace_ellipses, 0, wx.TOP, 15)
        sizer14 = wx.FlexGridSizer(2, 10, 2)
        sizer13.Add(sizer14, 0, wx.TOP, 5)
        self.ellipses1 = wx.RadioButton(box, name="ellipses1")
        self.ellipses1.Bind(wx.EVT_RADIOBUTTON, self.app.frame_controls.on_option)
        sizer14.Add(self.ellipses1, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        before = _("before")
        after = _("after")
        self.ellipses1_text = wx.StaticText(
            box, label=f"{before}...{after}", name="ellipses1_text"
        )
        self.ellipses1_text.SetFont(big_font)
        sizer14.Add(self.ellipses1_text, 0, 0, 0)
        self.ellipses2 = wx.RadioButton(box, name="ellipses2")
        self.ellipses2.Bind(wx.EVT_RADIOBUTTON, self.app.frame_controls.on_option)
        sizer14.Add(self.ellipses2, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.ellipses2_text = wx.StaticText(
            box, label=f"{before}…{after}", name="ellipses2_text"
        )
        self.ellipses2_text.SetFont(big_font)
        sizer14.Add(self.ellipses2_text, 0, 0, 0)
        self.ellipses3 = wx.RadioButton(box, name="ellipses3")
        self.ellipses3.Bind(wx.EVT_RADIOBUTTON, self.app.frame_controls.on_option)
        sizer14.Add(self.ellipses3, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.ellipses3_text = wx.StaticText(
            box,
            label=f"{before}\u200a.\u200a.\u200a.\u200a{after}",
            name="ellipses3_text",
        )
        self.ellipses3_text.SetFont(big_font)
        sizer14.Add(self.ellipses3_text, 0, 0, 0)
        self.ellipses4 = wx.RadioButton(box, name="ellipses4")
        self.ellipses4.Bind(wx.EVT_RADIOBUTTON, self.app.frame_controls.on_option)
        sizer14.Add(self.ellipses4, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.ellipses4_text = wx.StaticText(
            box,
            label=f"{before}\u2009.\u2009.\u2009.\u2009{after}",
            name="ellipses4_text",
        )
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
        self.template_headings = wx.StaticText(
            box,
            label=_("Selected template supports both parts and chapters"),
            name="template_headings",
        )
        sizer17.Add(self.template_headings, 0, wx.TOP, 15)
        self.part_chapter = wx.CheckBox(
            box, label=_("Style parts and chapters"), name="part_chapter"
        )
        self.part_chapter.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer17.Add(self.part_chapter, 0, wx.TOP, 7)
        self.style_end = wx.CheckBox(box, label=_('Style "The End"'), name="style_end")
        self.style_end.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer17.Add(self.style_end, 0, wx.TOP, 10)
        sizer18 = wx.BoxSizer(wx.HORIZONTAL)
        sizer17.Add(sizer18, 0, wx.EXPAND | wx.TOP, 7)
        self.add_end = wx.CheckBox(box, label=_("Add if missing:"), name="add_end")
        self.add_end.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer18.Add(self.add_end, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.end = wx.TextCtrl(box, value="The End", name="end")
        self.end.Bind(wx.EVT_TEXT, self.app.frame_controls.on_option)
        sizer18.Add(self.end, 1, 0, 0)
        sizer19 = wx.BoxSizer(wx.HORIZONTAL)
        sizer17.Add(sizer19, 0, wx.EXPAND | wx.TOP, 10)
        self.breaks_text = wx.StaticText(
            box, label=_("Page breaks:"), name="breaks_text"
        )
        sizer19.Add(self.breaks_text, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.breaks = wx.Choice(
            box,
            choices=[
                _("Continuous (no breaks before part/chapter text)"),
                _("Next page (keep headers/footers on first page of part/chapter)"),
                _("Next page (no headers/footers on first page of part/chapter)"),
                _("Odd page (no headers/footers on first page of part/chapter)"),
                _("Even page (no headers/footers on first page of part/chapter)"),
            ],
            name="breaks",
        )
        self.breaks.Bind(wx.EVT_CHOICE, self.app.frame_controls.on_option)
        sizer19.Add(self.breaks, 1, wx.LEFT, 5)
        self.indent = wx.CheckBox(
            box, label=_("Indent first paragraph of scenes"), name="indent"
        )
        self.indent.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer17.Add(self.indent, 0, wx.TOP, 8)

        box = wx.StaticBox(self, label=_("Dashes and Hyphens"))
        sizer15.Add(box, 1, wx.LEFT, 20)
        sizer20 = wx.BoxSizer(wx.VERTICAL)
        sizer21 = wx.BoxSizer(wx.VERTICAL)
        box.SetSizer(sizer20)
        sizer20.Add(sizer21, 1, wx.EXPAND | wx.ALL, 10)
        self.replace_dashes = wx.CheckBox(
            box, label=_("Replace dashes"), name="replace_dashes"
        )
        self.replace_dashes.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer21.Add(self.replace_dashes, 0, wx.TOP, 15)
        self.replace_hyphens = wx.CheckBox(
            box, label=_("Replace double-hyphens (--)"), name="replace_hyphens"
        )
        self.replace_hyphens.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer21.Add(self.replace_hyphens, 0, wx.TOP, 12)
        self.hyphen_at_end = wx.CheckBox(
            box, label=_('Fix hyphen at end of quotes (before-")'), name="hyphen_at_end"
        )
        self.hyphen_at_end.Bind(wx.EVT_CHECKBOX, self.app.frame_controls.on_option)
        sizer21.Add(self.hyphen_at_end, 0, wx.TOP, 12)
        sizer22 = wx.FlexGridSizer(2, 5, 2)
        sizer21.Add(sizer22, 0, wx.TOP, 10)
        self.en_dash = wx.RadioButton(box, name="en_dash")
        self.en_dash.Bind(wx.EVT_RADIOBUTTON, self.app.frame_controls.on_option)
        sizer22.Add(self.en_dash, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        text = wx.StaticText(box, label=f"{before} – {after}")
        text.SetFont(big_font)
        sizer22.Add(text, 0, 0, 0)
        self.em_dash = wx.RadioButton(box, name="em_dash")
        self.em_dash.Bind(wx.EVT_RADIOBUTTON, self.app.frame_controls.on_option)
        sizer22.Add(self.em_dash, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        text = wx.StaticText(box, label=f"{before}—{after}")
        text.SetFont(big_font)
        sizer22.Add(text, 0, 0, 0)

        add_stretcher(sizer1)
        sizer23 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(sizer23, 0, wx.EXPAND | wx.TOP, 10)
        button = wx.Button(self, label=_("Previous"))
        button.Bind(wx.EVT_BUTTON, self.app.frame_controls.on_prev)
        sizer23.Add(button, 0, 0, 0)
        add_stretcher(sizer23)
        button = wx.Button(self, label=_("Next"))
        button.Bind(wx.EVT_BUTTON, self.app.frame_controls.on_apply_and_next)
        sizer23.Add(button, 0, 0, 0)

        self.SetSizer(sizer1)
        self.refresh_contents()

    def refresh_contents(self):
        super(OptionsPanel, self).refresh_contents()
        config = self.app.settings.latest_config
        self.double.SetValue(config.spaces.purge_double)
        self.leading.SetValue(config.spaces.purge_leading)
        self.trailing.SetValue(config.spaces.purge_trailing)
        self.italic.SetValue(config.italic.adjust_to_include_punctuation)
        self.quotes.SetValue(config.quotes.convert_to_curly)
        self.blank.SetValue(config.divider.blank_paragraph_if_no_other)
        self.replace_divider.SetValue(config.divider.replace_with_new)
        self.divider.Enable(config.divider.replace_with_new)
        self.divider.SetValue(config.divider.new)
        enable = config.ellipses.replace_with_new
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
        match config.ellipses.new:
            case "...":
                self.ellipses1.SetValue(True)
            case "…":
                self.ellipses2.SetValue(True)
            case "\u200a.\u200a.\u200a.\u200a":
                self.ellipses3.SetValue(True)
            case "\u2009.\u2009.\u2009.\u2009":
                self.ellipses3.SetValue(True)
        self.part_chapter.SetValue(config.headings.style_parts_and_chapter)
        self.style_end.SetValue(config.headings.style_the_end)
        self.add_end.SetValue(config.headings.add_the_end)
        self.end.Enable(config.headings.add_the_end)
        self.end.SetValue(config.headings.the_end)
        if config.headings.header_footer_after_break:
            match config.headings.break_before_heading:
                case PaginationType.CONTINUOUS:
                    self.breaks.SetSelection(0)
                case PaginationType.NEW_PAGE:
                    self.breaks.SetSelection(1)
        else:
            match config.headings.break_before_heading:
                case PaginationType.NEW_PAGE:
                    self.breaks.SetSelection(2)
                case PaginationType.ODD_PAGE:
                    self.breaks.SetSelection(3)
                case PaginationType.EVEN_PAGE:
                    self.breaks.SetSelection(4)
        self.indent.SetValue(config.styling.indent_first_paragraph)
        self.replace_dashes.SetValue(config.dashes.force_all_en_or_em)
        self.replace_hyphens.SetValue(config.dashes.convert_double)
        self.hyphen_at_end.SetValue(config.dashes.fix_at_end_of_quote)
        if config.dashes.convert_to_en_dash:
            self.en_dash.SetValue(True)
        else:
            self.em_dash.SetValue(True)

    def grab_contents(self):
        assert self.app.initialized

        config = self.app.settings.latest_config
        config_copy = deepcopy(config)
        refresh = False
        config.spaces.purge_double = self.double.GetValue()
        config.spaces.purge_leading = self.leading.GetValue()
        config.spaces.purge_trailing = self.trailing.GetValue()
        config.italic.adjust_to_include_punctuation = self.italic.GetValue()
        config.quotes.convert_to_curly = self.quotes.GetValue()
        config.divider.blank_paragraph_if_no_other = self.blank.GetValue()
        if config.divider.replace_with_new != self.replace_divider.GetValue():
            config.divider.replace_with_new = self.replace_divider.GetValue()
            refresh = True
        config.divider.new = self.divider.GetValue()
        if config.ellipses.replace_with_new != self.replace_ellipses.GetValue():
            config.ellipses.replace_with_new = self.replace_ellipses.GetValue()
            refresh = True
        if self.ellipses1.GetValue():
            config.ellipses.new = "..."
        elif self.ellipses2.GetValue():
            config.ellipses.new = "…"
        elif self.ellipses3.GetValue():
            config.ellipses.new = "\u200a.\u200a.\u200a.\u200a"
        elif self.ellipses4.GetValue():
            config.ellipses.new = "\u2009.\u2009.\u2009.\u2009"
        config.headings.style_parts_and_chapter = self.part_chapter.GetValue()
        config.headings.style_the_end = self.style_end.GetValue()
        if config.headings.add_the_end != self.add_end.GetValue():
            config.headings.add_the_end = self.add_end.GetValue()
            refresh = True
        config.headings.the_end = self.end.GetValue()
        match self.breaks.GetSelection():
            case 0:
                config.headings.header_footer_after_break = True
                config.headings.break_before_heading = PaginationType.CONTINUOUS
            case 1:
                config.headings.header_footer_after_break = True
                config.headings.break_before_heading = PaginationType.NEW_PAGE
            case 2:
                config.headings.header_footer_after_break = False
                config.headings.break_before_heading = PaginationType.NEW_PAGE
            case 3:
                config.headings.header_footer_after_break = False
                config.headings.break_before_heading = PaginationType.ODD_PAGE
            case 4:
                config.headings.header_footer_after_break = False
                config.headings.break_before_heading = PaginationType.EVEN_PAGE
        config.styling.indent_first_paragraph = self.indent.GetValue()
        config.dashes.force_all_en_or_em = self.replace_dashes.GetValue()
        config.dashes.convert_double = self.replace_hyphens.GetValue()
        config.dashes.fix_at_end_of_quote = self.hyphen_at_end.GetValue()
        config.dashes.convert_to_en_dash = self.en_dash.GetValue()
        config.dashes.convert_to_em_dash = self.em_dash.GetValue()

        if config != config_copy:
            self.app.book.modified()

        if refresh:
            self.app.refresh_contents()
