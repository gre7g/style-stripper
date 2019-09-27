import logging
import wx

from style_stripper.data.constants import CONSTANTS
from style_stripper.data.enums import *
from style_stripper.data.paragraph import Paragraph
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

    def __init__(self, parent):
        super(ReviewPanel, self).__init__(parent)
        self.app = wx.GetApp()
        self.state = STATE_READY
        self.part = self.chapter = self.end = self.symbolic = self.blanks = self.questionable = None

        sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer1)
        self.processing = wx.StaticText(self, label=_("Processing..."))
        sizer1.Add(self.processing, 0, 0, 0)
        sizer2 = wx.FlexGridSizer(2, 10, 10)
        sizer1.Add(sizer2, 1, wx.EXPAND | wx.TOP, 10)
        text = wx.StaticText(self, label=_("• Spaces"))
        sizer2.Add(text, 0, 0, 0)
        self.spaces = wx.StaticText(self)
        sizer2.Add(self.spaces)
        text = wx.StaticText(self, label=_("• Italics"))
        sizer2.Add(text, 0, 0, 0)
        self.italics = wx.StaticText(self)
        sizer2.Add(self.italics)
        text = wx.StaticText(self, label=_("• Quotes and dashes"))
        sizer2.Add(text, 0, 0, 0)
        self.quotes_and_dashes = wx.StaticText(self)
        sizer2.Add(self.quotes_and_dashes)
        text = wx.StaticText(self, label=_("• Ticks"))
        sizer2.Add(text, 0, 0, 0)
        self.ticks = wx.StaticText(self)
        sizer2.Add(self.ticks)
        text = wx.StaticText(self, label=_("• Headers"))
        sizer2.Add(text, 0, 0, 0)
        self.headers = wx.StaticText(self)
        sizer2.Add(self.headers)
        text = wx.StaticText(self, label=_("• Scene breaks"))
        sizer2.Add(text, 0, 0, 0)
        self.scene_breaks = wx.StaticText(self)
        sizer2.Add(self.scene_breaks)

        add_stretcher(sizer1)
        sizer23 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(sizer23, 0, wx.EXPAND | wx.TOP, 10)
        button = wx.Button(self, label=_("Prev"))
        button.Bind(wx.EVT_BUTTON, self.app.frame_controls.on_prev)
        sizer23.Add(button, 0, 0, 0)

    def refresh_contents(self):
        document = self.app.book.original_docx
        config = self.app.settings.latest_config

        if self.state == STATE_READY:
            # The Paragraph class has a class member that tracks what sort of dash we're using so we don't have to do this
            # comparison constantly. Set the class member now based on book configuration.
            Paragraph.set_dash_class_member(config)

            self.state = STATE_FIX_SPACES
            wx.CallAfter(self.refresh_contents)

        elif self.state == STATE_FIX_SPACES:
            self.app.book.modified()
            if config[SPACES][PURGE_DOUBLE_SPACES] or config[SPACES][PURGE_LEADING_WHITESPACE] or config[SPACES][PURGE_TRAILING_WHITESPACE]:
                document.fix_spaces()
                self.spaces.SetLabel(_("Fixed"))
            else:
                self.spaces.SetLabel(_("Disabled"))
            self.state = STATE_FIX_ITALICS
            wx.CallAfter(self.app.frame.refresh_contents)

        elif self.state == STATE_FIX_ITALICS:
            if config[ITALIC][ADJUST_TO_INCLUDE_PUNCTUATION]:
                document.fix_italic_boundaries()
                self.italics.SetLabel(_("Fixed"))
            else:
                self.italics.SetLabel(_("Disabled"))
            self.state = STATE_FIX_QUOTES_AND_DASHES
            wx.CallAfter(self.refresh_contents)

        elif self.state == STATE_FIX_QUOTES_AND_DASHES:
            document.fix_quotes_and_dashes()
            self.quotes_and_dashes.SetLabel(_("Fixed"))
            self.state = STATE_FIX_TICKS
            wx.CallAfter(self.refresh_contents)

        elif self.state == STATE_FIX_TICKS:
            if config[QUOTES][CONVERT_TO_CURLY]:
                self.questionable = document.fix_ticks()
                self.ticks.SetLabel(_("Located %d special cases") % len(self.questionable))
            else:
                self.ticks.SetLabel(_("Disabled"))
            self.state = STATE_SEARCH_HEADINGS
            wx.CallAfter(self.refresh_contents)

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
            wx.CallAfter(self.refresh_contents)

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
            wx.CallAfter(self.refresh_contents)

        elif self.state == STATE_SEARCH_DIVIDERS:
            self.symbolic, self.blanks = document.find_divider_candidates()
            self.state = STATE_DONE
