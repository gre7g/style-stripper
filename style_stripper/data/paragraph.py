"""Paragraphs"""

from dataclasses import dataclass
import logging
import pickle
from typing import List, Dict, Optional, ClassVar
import wx

from style_stripper.data.constants import CONSTANTS
from style_stripper.control.settings_control import ConfigSettings

# Constants:
LOG = logging.getLogger(__name__)

# Types:
OffsetType = int


class Paragraph:
    DASH: ClassVar[str]
    text: str
    word_count: int
    style: Optional[str]

    @classmethod
    def set_dash_class_member(cls, config: ConfigSettings):
        cls.DASH = "—" if config.dashes.convert_to_em_dash else " – "

    def __init__(self, text: Optional[str] = None, style: Optional[str] = None):
        self.text = ""
        self.word_count = 0
        self.style = style
        if text:
            self.add(text)

    def add(self, text: str, italic: bool = False):
        if italic:
            if self.text.endswith("❱"):
                self.text = self.text[:-1] + text + "❱"
            else:
                self.text += "❰%s❱" % text
        else:
            self.text += text

    def get_word_count(self):
        self.word_count = len(CONSTANTS.PARAGRAPHS.SEARCH_WORD.findall(self.text))

    def fix_spaces(self, config: ConfigSettings):
        if config.spaces.purge_leading:
            self.text = CONSTANTS.PARAGRAPHS.SEARCH_LEADING_WHITESPACE.sub(
                "", self.text
            )

        if config.spaces.purge_trailing:
            self.text = CONSTANTS.PARAGRAPHS.SEARCH_TRAILING_WHITESPACE.sub(
                "", self.text
            )

        if config.spaces.purge_double:
            self.text = CONSTANTS.PARAGRAPHS.SEARCH_DOUBLE_WHITESPACE.sub(
                " ", self.text
            )

    def fix_quotes_and_dashes(self, config: ConfigSettings):
        if config.quotes.convert_to_curly:
            even = True
            for match in CONSTANTS.PARAGRAPHS.SEARCH_ANY_QUOTE.finditer(self.text):
                even = not even
                quote = "”" if even else "“"
                self.text = (
                    self.text[: match.start()] + quote + self.text[match.end() :]
                )

            # Can only fix dashes if we fix quotes
            if config.dashes.convert_to_em_dash or config.dashes.convert_to_en_dash:
                self.text = CONSTANTS.PARAGRAPHS.SEARCH_BROKEN_QUOTE1.sub(
                    "”" + self.DASH, self.text
                )
                self.text = CONSTANTS.PARAGRAPHS.SEARCH_BROKEN_QUOTE2.sub(
                    self.DASH + "“", self.text
                )
            if config.dashes.convert_double:
                self.text = CONSTANTS.PARAGRAPHS.SEARCH_DASHES.sub(self.DASH, self.text)
            if config.dashes.fix_at_end_of_quote:
                self.text = CONSTANTS.PARAGRAPHS.SEARCH_DASH_END_OF_QUOTE.sub(
                    self.DASH + "”", self.text
                )
            if config.dashes.force_all_en_or_em:
                self.text = CONSTANTS.PARAGRAPHS.SEARCH_EN_OR_EM.sub(
                    self.DASH, self.text
                )

    def fix_ellipses(self, config: ConfigSettings):
        for search, replace in CONSTANTS.ELLIPSES.SUB_SPACE:
            self.text = search.sub(replace, self.text)
        self.text = CONSTANTS.ELLIPSES.SEARCH.sub(config.ellipses.new, self.text)

    def fix_italic_boundaries(self):
        self.text = CONSTANTS.PARAGRAPHS.SEARCH_ITALIC_WHITE1.sub(r"\1", self.text)
        self.text = CONSTANTS.PARAGRAPHS.SEARCH_ITALIC_WHITE2.sub(r"\1❰", self.text)
        self.text = CONSTANTS.PARAGRAPHS.SEARCH_ITALIC_WHITE3.sub(r"❱\1", self.text)
        self.text = CONSTANTS.PARAGRAPHS.SEARCH_ITALIC_WHITE4.sub(r"❰\1", self.text)
        self.text = CONSTANTS.PARAGRAPHS.SEARCH_ITALIC_WHITE5.sub(r"\1❱", self.text)

    def fix_ticks(self, questionable_ticks: List["QuestionableTick"]):
        inside_quote = False
        must_change: Dict[OffsetType, str] = {}
        change_unknown: List[OffsetType] = []
        offset = 0
        while True:
            match = CONSTANTS.PARAGRAPHS.SEARCH_QUOTES_OR_TICKS.search(
                self.text, offset
            )
            if not match:
                break

            match match.group(2):
                # Start quote?
                case "“":
                    inside_quote = True
                # End quote?
                case "”":
                    inside_quote = False

                    # There was no matching end tick, so they must be close
                    while change_unknown:
                        must_change[change_unknown.pop()] = "’"
                case _:
                    # Contraction or end of word?
                    if match.group(1):
                        if match.group(3):
                            # Contraction, always a close
                            must_change[match.start(2)] = "’"
                        else:
                            # End of word, is a close but could also be end of a quote, so ask
                            must_change[match.start(2)] = "’"
                            while change_unknown:
                                offset = change_unknown.pop()
                                questionable_ticks.append(
                                    QuestionableTick(self, offset)
                                )
                    else:
                        if match.group(3):
                            # Start of a word, but is it inside quotes?
                            if inside_quote:
                                # Yes, queue this up as unknown
                                change_unknown.append(match.start(2))
                            else:
                                # Not in quotes. Must be a close.
                                must_change[match.start(2)] = "’"
                        else:
                            # Tick after some punctuation and before a space, so close, but could also be end of a
                            # quote, so ask
                            must_change[match.start(2)] = "’"
                            while change_unknown:
                                offset = change_unknown.pop()
                                questionable_ticks.append(
                                    QuestionableTick(self, offset)
                                )

            offset = match.end(2)

        # There was no matching end tick so leftovers must be close
        while change_unknown:
            must_change[change_unknown.pop()] = "’"

        # Change all queued up
        for offset, tick in must_change.items():
            self.text = self.text[:offset] + tick + self.text[offset + 1 :]

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return repr(self.text)


@dataclass
class QuestionableTick:
    paragraph: Paragraph
    start: int
    checkbox: wx.CheckBox = None

    def __str__(self):
        match = CONSTANTS.PARAGRAPHS.SEARCH_END_TICK.search(
            self.paragraph.text, self.start + 1
        )
        return CONSTANTS.PARAGRAPHS.SEARCH_ITALIC_CHARS.sub(
            "", self.paragraph.text[self.start : match.end(1)]
        )

    def apply(self):
        self.paragraph.text = (
            self.paragraph.text[: self.start]
            + ("‘" if self.checkbox.IsChecked() else "’")
            + self.paragraph.text[self.start + 1 :]
        )


# Patch pickle so that QuestionableTick objects won't include a wx.CheckBox member. These can't be pickled.
pickle.dispatch_table[QuestionableTick] = lambda obj: (
    QuestionableTick,
    (obj.paragraph, obj.start, None),
)
