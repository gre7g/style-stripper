import logging
from typing import List
import wx
from wx.lib.scrolledpanel import ScrolledPanel

from style_stripper.data.constants import CONSTANTS
from style_stripper.data.paragraph import Paragraph, QuestionableTick
from style_stripper.model.content_pane import ContentPanel
from style_stripper.model.utility import add_stretcher

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


class ReviewPanel(ContentPanel):
    questionable: List[QuestionableTick]
    part: int  # number of parts
    chapter: int  # number of chapters
    end: int  # number of "The End"
    symbolic: int  # number of divider symbols
    blanks: int  # number of blank dividers

    def __init__(self, *args, **kwargs):
        super(ReviewPanel, self).__init__(*args, **kwargs)
        self.questionable = []

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
        text = wx.StaticText(self, label=_("• Ellipses"))
        sizer2.Add(text, 0, 0, 0)
        self.ellipses = wx.StaticText(self)
        sizer2.Add(self.ellipses)
        text = wx.StaticText(self, label=_("• Scene breaks"))
        sizer2.Add(text, 0, 0, 0)
        self.scene_breaks = wx.StaticText(self)
        sizer2.Add(self.scene_breaks)
        text = wx.StaticText(self, label=_("• Quotes and dashes"))
        sizer2.Add(text, 0, 0, 0)
        self.quotes_and_dashes = wx.StaticText(self)
        sizer2.Add(self.quotes_and_dashes)

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
        button = wx.Button(self, label=_("Previous"))
        button.Bind(wx.EVT_BUTTON, self.app.frame_controls.on_reload)
        sizer23.Add(button, 0, 0, 0)
        add_stretcher(sizer23)
        self.apply_button = wx.Button(self, label=_("Next"))
        self.apply_button.Bind(wx.EVT_BUTTON, self.app.frame_controls.on_apply)
        sizer23.Add(self.apply_button, 0, 0, 0)

    def apply(self):
        self.apply_button.Enable(False)
        wx.CallLater(CONSTANTS.UI.APPLY_DELAY, self.apply1)

    def apply1(self):
        config = self.app.settings.latest_config

        # The Paragraph class has a class member that tracks what sort of dash we're using so we don't have to do
        # this comparison constantly. Set the class member now based on book configuration.
        Paragraph.set_dash_class_member(config)

        self.app.book.modified()
        if (
            config.spaces.purge_double
            or config.spaces.purge_leading
            or config.spaces.purge_trailing
        ):
            self.app.book.original_docx.fix_spaces()
            self.spaces.SetLabel(_("Fixed"))
        else:
            self.spaces.SetLabel(_("Disabled"))

        wx.CallLater(CONSTANTS.UI.APPLY_DELAY, self.apply2)

    def apply2(self):
        if self.app.settings.latest_config.italic.adjust_to_include_punctuation:
            self.app.book.original_docx.fix_italic_boundaries()
            self.italics.SetLabel(_("Fixed"))
        else:
            self.italics.SetLabel(_("Disabled"))

        wx.CallLater(CONSTANTS.UI.APPLY_DELAY, self.apply3)

    def apply3(self):
        if self.app.settings.latest_config.ellipses.replace_with_new:
            self.app.book.original_docx.fix_ellipses()
            self.ellipses.SetLabel(_("Fixed"))
        else:
            self.ellipses.SetLabel(_("Disabled"))

        wx.CallLater(CONSTANTS.UI.APPLY_DELAY, self.apply4)

    def apply4(self):
        self.app.book.original_docx.fix_quotes_and_dashes()
        self.quotes_and_dashes.SetLabel(_("Fixed"))

        wx.CallLater(CONSTANTS.UI.APPLY_DELAY, self.apply5)

    def apply5(self):
        if self.app.settings.latest_config.quotes.convert_to_curly:
            if not self.questionable:
                self.questionable = []
                for question in self.app.book.original_docx.fix_ticks():
                    question.checkbox = wx.CheckBox(self.scroll, label=str(question))
                    question.checkbox.SetValue(True)
                    self.questionable.append(question)
                    self.sizer3.Add(question.checkbox, 0, wx.TOP, 5)
                self.scroll.SetupScrolling()
                self.ticks.SetLabel(
                    _("Located %d special cases") % len(self.questionable)
                )
        else:
            self.ticks.SetLabel(_("Disabled"))

        wx.CallLater(CONSTANTS.UI.APPLY_DELAY, self.apply6)

    def apply6(self):
        config = self.app.settings.latest_config

        text = []
        if config.headings.style_parts_and_chapter or config.headings.style_the_end:
            results = self.app.book.original_docx.find_heading_candidates()
            self.part, self.chapter, self.end = results
            if self.part:
                text.append(_("%d parts") % self.part)
            if self.chapter:
                text.append(_("%d chapters") % self.chapter)
            if self.end:
                text.append(_("%d ending") % self.end)
            self.headers.SetLabel(
                _("Found: ") + _(", ").join(text) if text else _("None found")
            )
        else:
            self.headers.SetLabel(_("Disabled"))

        wx.CallLater(CONSTANTS.UI.APPLY_DELAY, self.apply7)

    def apply7(self):
        document = self.app.book.original_docx
        config = self.app.settings.latest_config

        text = []
        if config.headings.style_parts_and_chapter and (self.part or self.chapter):
            chapter_style = (
                CONSTANTS.STYLING.NAMES.HEADING2
                if self.part
                else CONSTANTS.STYLING.NAMES.HEADING1
            )
            document.style_part_chapter(chapter_style)
            if self.part:
                text.append(_("%d parts") % self.part)
            if self.chapter:
                text.append(_("%d chapters") % self.chapter)
        if config.headings.style_the_end and self.end:
            document.style_end()
            text.append(_("%d ending") % self.end)
        if text:
            self.headers.SetLabel(_("Styled: ") + _(", ").join(text))

        wx.CallLater(CONSTANTS.UI.APPLY_DELAY, self.apply8)

    def apply8(self):
        if self.app.settings.latest_config.divider.replace_with_new:
            results = self.app.book.original_docx.find_divider_candidates()
            self.symbolic, self.blanks = results
            self.scene_breaks.SetLabel(
                _("Found %(symbolic)d symbolic and %(blank)d blank candidates")
                % {"symbolic": self.symbolic, "blank": self.blanks}
            )
        else:
            self.scene_breaks.SetLabel(_("Disabled"))

        wx.CallLater(CONSTANTS.UI.APPLY_DELAY, self.apply9)

    def apply9(self):
        document = self.app.book.original_docx
        config = self.app.settings.latest_config

        if config.divider.replace_with_new:
            if self.symbolic:
                document.replace_symbolic()
                document.remove_blanks()
                self.scene_breaks.SetLabel(
                    _("Fixed %(symbolic)d symbolic dividers, removed %(blank)d blanks")
                    % {"symbolic": self.symbolic, "blank": self.blanks}
                )
            elif config.divider.blank_paragraph_if_no_other and self.blanks:
                if self.blanks < CONSTANTS.DIVIDER.MAX_BLANK_PARAGRAPH_DIVIDERS:
                    document.replace_blanks()
                    self.scene_breaks.SetLabel(
                        _("Converted %d blanks into dividers") % self.blanks
                    )
                else:
                    document.remove_blanks()
                    self.scene_breaks.SetLabel(_("Removed %d blanks") % self.blanks)
        if config.headings.add_the_end and not self.end:
            document.add_end()

        wx.CallLater(CONSTANTS.UI.APPLY_DELAY, self.apply10)

    def apply10(self):
        self.processing.SetLabel(_("Processing complete."))
        self.apply_button.Enable(True)
