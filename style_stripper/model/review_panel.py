import logging
from typing import List
import wx
from wx.lib.scrolledpanel import ScrolledPanel

from style_stripper.data.constants import CONSTANTS
from style_stripper.data.enums import *
from style_stripper.data.paragraph import Paragraph, QuestionableTick
from style_stripper.model.utility import add_stretcher

try:
    from style_stripper.model.main_app import StyleStripperApp
except ImportError:
    StyleStripperApp = None

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


class ReviewPanel(wx.Panel):
    app: StyleStripperApp
    questionable: List[QuestionableTick]

    def __init__(self, parent):
        super(ReviewPanel, self).__init__(parent)
        self.app = wx.GetApp()
        self.state = STATE_IDLE
        self.part = self.chapter = self.end = self.symbolic = self.blanks = self.questionable = None

        sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer1)
        self.processing = wx.StaticText(self, label=_("Processing..."))
        sizer1.Add(self.processing, 0, 0, 0)
        sizer2 = wx.FlexGridSizer(4, 10, 10)
        sizer2.AddGrowableCol(1)
        sizer2.AddGrowableCol(3)
        sizer1.Add(sizer2, 0, wx.EXPAND | wx.TOP, 10)
        text = wx.StaticText(self, label=_("• Spaces"))
        sizer2.Add(text, 0, 0, 0)
        self.spaces = wx.StaticText(self)
        sizer2.Add(self.spaces)
        text = wx.StaticText(self, label=_("• Ticks"))
        sizer2.Add(text, 0, 0, 0)
        self.ticks = wx.StaticText(self)
        sizer2.Add(self.ticks)
        text = wx.StaticText(self, label=_("• Italics"))
        sizer2.Add(text, 0, 0, 0)
        self.italics = wx.StaticText(self)
        sizer2.Add(self.italics)
        text = wx.StaticText(self, label=_("• Headers"))
        sizer2.Add(text, 0, 0, 0)
        self.headers = wx.StaticText(self)
        sizer2.Add(self.headers)
        text = wx.StaticText(self, label=_("• Quotes and dashes"))
        sizer2.Add(text, 0, 0, 0)
        self.quotes_and_dashes = wx.StaticText(self)
        sizer2.Add(self.quotes_and_dashes)
        text = wx.StaticText(self, label=_("• Scene breaks"))
        sizer2.Add(text, 0, 0, 0)
        self.scene_breaks = wx.StaticText(self)
        sizer2.Add(self.scene_breaks)

        text = wx.StaticText(
            self,
            label=_(
                "The following are probably all quoted text found inside dialogue. "
                "Leave checked if they are, uncheck if not:"
            ),
        )
        sizer1.Add(text, 0, wx.TOP, 20)
        self.scroll = ScrolledPanel(self, style=wx.BORDER_STATIC)
        sizer1.Add(self.scroll, 1, wx.EXPAND, 0)
        sizer3 = wx.BoxSizer(wx.VERTICAL)
        self.scroll.SetSizer(sizer3)
        self.sizer3 = wx.BoxSizer(wx.VERTICAL)
        sizer3.Add(self.sizer3, 1, wx.EXPAND | wx.LEFT, 5)

        sizer23 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(sizer23, 0, wx.EXPAND | wx.TOP, 10)
        button = wx.Button(self, label=_("Back (reload document)"))
        button.Bind(wx.EVT_BUTTON, self.app.frame_controls.on_reload)
        sizer23.Add(button, 0, 0, 0)
        add_stretcher(sizer23)
        self.apply_button = wx.Button(self, label=_("Apply Options"))
        self.apply_button.Bind(wx.EVT_BUTTON, self.app.frame_controls.on_apply)
        sizer23.Add(self.apply_button, 0, 0, 0)

    def apply(self):
        self.state = STATE_READY
        self.apply_button.Enable(False)
        wx.CallLater(CONSTANTS.UI.APPLY_DELAY, self.refresh_contents)

    def refresh_contents(self):
        document = self.app.book.original_docx
        config = self.app.settings.latest_config

        if self.state == STATE_READY:
            # The Paragraph class has a class member that tracks what sort of dash we're using so we don't have to do
            # this comparison constantly. Set the class member now based on book configuration.
            Paragraph.set_dash_class_member(config)

            self.state = STATE_FIX_SPACES
            wx.CallLater(CONSTANTS.UI.APPLY_DELAY, self.refresh_contents)

        elif self.state == STATE_FIX_SPACES:
            self.app.book.modified()
            if (
                config[SPACES][PURGE_DOUBLE_SPACES]
                or config[SPACES][PURGE_LEADING_WHITESPACE]
                or config[SPACES][PURGE_TRAILING_WHITESPACE]
            ):
                document.fix_spaces()
                self.spaces.SetLabel(_("Fixed"))
            else:
                self.spaces.SetLabel(_("Disabled"))
            self.state = STATE_FIX_ITALICS
            wx.CallLater(CONSTANTS.UI.APPLY_DELAY, self.app.frame.refresh_contents)

        elif self.state == STATE_FIX_ITALICS:
            if config[ITALIC][ADJUST_TO_INCLUDE_PUNCTUATION]:
                document.fix_italic_boundaries()
                self.italics.SetLabel(_("Fixed"))
            else:
                self.italics.SetLabel(_("Disabled"))
            self.state = STATE_FIX_QUOTES_AND_DASHES
            wx.CallLater(CONSTANTS.UI.APPLY_DELAY, self.refresh_contents)

        elif self.state == STATE_FIX_QUOTES_AND_DASHES:
            document.fix_quotes_and_dashes()
            self.quotes_and_dashes.SetLabel(_("Fixed"))
            self.state = STATE_FIX_TICKS
            wx.CallLater(CONSTANTS.UI.APPLY_DELAY, self.refresh_contents)

        elif self.state == STATE_FIX_TICKS:
            if config[QUOTES][CONVERT_TO_CURLY]:
                self.questionable = []
                for question in document.fix_ticks():
                    question.checkbox = wx.CheckBox(self.scroll, label=str(question))
                    question.checkbox.SetValue(True)
                    self.questionable.append(question)
                    self.sizer3.Add(question.checkbox, 0, wx.TOP, 5)
                self.scroll.SetupScrolling()
                self.ticks.SetLabel(_("Located %d special cases") % len(self.questionable))
            else:
                self.ticks.SetLabel(_("Disabled"))
            self.state = STATE_SEARCH_HEADINGS
            wx.CallLater(CONSTANTS.UI.APPLY_DELAY, self.refresh_contents)

        elif self.state == STATE_SEARCH_HEADINGS:
            text = []
            if config[HEADINGS][STYLE_PARTS_AND_CHAPTER] or config[HEADINGS][STYLE_THE_END]:
                self.part, self.chapter, self.end = document.find_heading_candidates()
                if self.part:
                    text.append(_("%d parts") % self.part)
                if self.chapter:
                    text.append(_("%d chapters") % self.chapter)
                if self.end:
                    text.append(_("%d ending") % self.end)
                self.headers.SetLabel(_("Found: ") + _(", ").join(text) if text else _("None found"))
            else:
                self.headers.SetLabel(_("Disabled"))
            self.state = STATE_REPLACE_HEADINGS
            wx.CallLater(CONSTANTS.UI.APPLY_DELAY, self.refresh_contents)

        elif self.state == STATE_REPLACE_HEADINGS:
            text = []
            if config[HEADINGS][STYLE_PARTS_AND_CHAPTER] and (self.part or self.chapter):
                chapter_style = CONSTANTS.STYLING.NAMES.HEADING2 if self.part else CONSTANTS.STYLING.NAMES.HEADING1
                document.style_part_chapter(chapter_style)
                if self.part:
                    text.append(_("%d parts") % self.part)
                if self.chapter:
                    text.append(_("%d chapters") % self.chapter)
            if config[HEADINGS][STYLE_THE_END] and self.end:
                document.style_end()
                text.append(_("%d ending") % self.end)
            if text:
                self.headers.SetLabel(_("Styled: ") + _(", ").join(text))
            self.state = STATE_SEARCH_DIVIDERS
            wx.CallLater(CONSTANTS.UI.APPLY_DELAY, self.refresh_contents)

        elif self.state == STATE_SEARCH_DIVIDERS:
            if config[DIVIDER][REPLACE_WITH_NEW]:
                self.symbolic, self.blanks = document.find_divider_candidates()
                symbolic_blank = {"symbolic": self.symbolic, "blank": self.blanks}
                self.scene_breaks.SetLabel(
                    _("Found %(symbolic)d symbolic and %(blank)d blank candidates") % symbolic_blank
                )
            else:
                self.scene_breaks.SetLabel(_("Disabled"))
            self.state = STATE_DONE
            self.state = STATE_FIX_DIVIDERS
            wx.CallLater(CONSTANTS.UI.APPLY_DELAY, self.refresh_contents)

        elif self.state == STATE_FIX_DIVIDERS:
            if config[DIVIDER][REPLACE_WITH_NEW]:
                if self.symbolic:
                    document.replace_symbolic()
                    document.remove_blanks()
                    symbolic_blank = {"symbolic": self.symbolic, "blank": self.blanks}
                    self.scene_breaks.SetLabel(
                        _("Fixed %(symbolic)d symbolic dividers, removed %(blank)d blanks") % symbolic_blank
                    )
                elif config[DIVIDER][BLANK_PARAGRAPH_IF_NO_OTHER] and self.blanks:
                    if self.blanks < CONSTANTS.DIVIDER.MAX_BLANK_PARAGRAPH_DIVIDERS:
                        document.replace_blanks()
                        self.scene_breaks.SetLabel(_("Converted %d blanks into dividers") % self.blanks)
                    else:
                        document.remove_blanks()
                        self.scene_breaks.SetLabel(_("Removed %d blanks") % self.blanks)
            self.state = STATE_DONE
            wx.CallLater(CONSTANTS.UI.APPLY_DELAY, self.refresh_contents)

        elif self.state == STATE_DONE:
            self.processing.SetLabel(_("Processing complete."))
            self.apply_button.Enable(True)

    def get_ticks(self):
        return [question for question in self.questionable if question.checkbox.GetValue()]
