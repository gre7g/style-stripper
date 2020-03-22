"""Paragraphs"""

from __future__ import annotations  # Allows a parameter to have type hinting of the class that contains it
import attr
import logging
import re
from typing import List, Tuple, Optional, ClassVar
import wx

from style_stripper.data.constants import CONSTANTS
from style_stripper.data.enums import *

# Constants:
SEARCH_LEADING_WHITESPACE = re.compile(r"^\s+")
SEARCH_TRAILING_WHITESPACE = re.compile(r"\s+$")
SEARCH_DOUBLE_WHITESPACE = re.compile(r"\s{2,}")
SEARCH_ITALIC_WHITE1 = re.compile(r"❱(\s*)❰")
SEARCH_ITALIC_WHITE2 = re.compile(r"❰(\s+)")
SEARCH_ITALIC_WHITE3 = re.compile(r"(\s+)❱")
SEARCH_ITALIC_WHITE4 = re.compile(r"([^ a-zA-Z]+)❰")
SEARCH_ITALIC_WHITE5 = re.compile(r"❱([^ a-zA-Z]+)")
SEARCH_BROKEN_QUOTE1 = re.compile(r"”\s*-+\s*")
SEARCH_BROKEN_QUOTE2 = re.compile(r"\s*-+\s*“")
SEARCH_DASHES = re.compile(r"\s*-{2,}\s*")
SEARCH_ANY_QUOTE = re.compile('["“”]')
SEARCH_QUOTES_OR_TICKS = re.compile(r"(\w?)([“”'‘’])(\w?)")
SEARCH_DASH_END_OF_QUOTE = re.compile(r"[—–-]+”")
SEARCH_EN_OR_EM = re.compile(" – |—")
SEARCH_WORD = re.compile("[a-z]+", re.I)
SEARCH_END_TICK = re.compile(r"(’)(\W|$)")
SEARCH_ITALIC_CHARS = re.compile(r"[❰❱]")

LOG = logging.getLogger(__name__)


class Paragraph(object):
    text: str
    DASH: ClassVar[str]

    @classmethod
    def set_dash_class_member(cls, config: dict):
        cls.DASH = "—" if config[DASHES][CONVERT_TO_EM_DASH] else " – "

    def __init__(self, text: Optional[str] = None) -> None:
        self.text = ""
        self.word_count = 0
        if text:
            self.add(text)
        self.style: Optional[str] = None

    def add(self, text: str, italic: bool = False) -> None:
        if italic:
            if self.text.endswith("❱"):
                self.text = self.text[:-1] + text + "❱"
            else:
                self.text += "❰%s❱" % text
        else:
            self.text += text

    def get_word_count(self) -> None:
        self.word_count = len(SEARCH_WORD.findall(self.text))

    def fix_spaces(self, config: dict) -> None:
        if config[SPACES][PURGE_LEADING_WHITESPACE]:
            self.text = SEARCH_LEADING_WHITESPACE.sub("", self.text)

        if config[SPACES][PURGE_TRAILING_WHITESPACE]:
            self.text = SEARCH_TRAILING_WHITESPACE.sub("", self.text)

        if config[SPACES][PURGE_DOUBLE_SPACES]:
            self.text = SEARCH_DOUBLE_WHITESPACE.sub(" ", self.text)

    def fix_quotes_and_dashes(self, config: dict) -> None:
        if config[QUOTES][CONVERT_TO_CURLY]:
            even = True
            for match in SEARCH_ANY_QUOTE.finditer(self.text):
                even = not even
                quote = "”" if even else "“"
                self.text = self.text[: match.start()] + quote + self.text[match.end() :]

            # Can only fix dashes if we fix quotes
            if config[DASHES][CONVERT_TO_EM_DASH] or config[DASHES][CONVERT_TO_EN_DASH]:
                self.text = SEARCH_BROKEN_QUOTE1.sub("”" + self.DASH, self.text)
                self.text = SEARCH_BROKEN_QUOTE2.sub(self.DASH + "“", self.text)
            if config[DASHES][CONVERT_DOUBLE_DASHES]:
                self.text = SEARCH_DASHES.sub(self.DASH, self.text)
            if config[DASHES][FIX_DASH_AT_END_OF_QUOTE]:
                self.text = SEARCH_DASH_END_OF_QUOTE.sub(self.DASH + "”", self.text)
            if config[DASHES][FORCE_ALL_EN_OR_EM]:
                self.text = SEARCH_EN_OR_EM.sub(self.DASH, self.text)

    def fix_ellipses(self, config: dict):
        for search, replace in CONSTANTS.ELLIPSES.SUB_SPACE:
            self.text = search.sub(replace, self.text)
        self.text = CONSTANTS.ELLIPSES.SEARCH.sub(config[ELLIPSES][NEW], self.text)

    def fix_italic_boundaries(self, config: dict):
        self.text = SEARCH_ITALIC_WHITE1.sub(r"\1", self.text)
        self.text = SEARCH_ITALIC_WHITE2.sub(r"\1❰", self.text)
        self.text = SEARCH_ITALIC_WHITE3.sub(r"❱\1", self.text)
        self.text = SEARCH_ITALIC_WHITE4.sub(r"❰\1", self.text)
        self.text = SEARCH_ITALIC_WHITE5.sub(r"\1❱", self.text)

    def fix_ticks(self, config: dict, questionable_ticks: List[QuestionableTick]):  # Configuration dictionary
        inside_quote = False
        must_change: List[Tuple[int, str]] = []  # [(offset, new_tick), ...]
        change_unknown: List[int] = []  # [offset, ...]
        offset = 0
        while True:
            match = SEARCH_QUOTES_OR_TICKS.search(self.text, offset)
            if not match:
                break

            # Start quote?
            if match.group(2) == "“":
                inside_quote = True
            # End quote?
            elif match.group(2) == "”":
                inside_quote = False

                # There was no matching end tick so they must be close
                while change_unknown:
                    must_change.append((change_unknown.pop(), "’"))
            else:
                # Contraction or end of word?
                if match.group(1):
                    if match.group(3):
                        # Contraction, always a close
                        must_change.append((match.start(2), "’"))
                    else:
                        # End of word, is a close but could also be end of a quote, so ask
                        must_change.append((match.start(2), "’"))
                        while change_unknown:
                            offset = change_unknown.pop()
                            questionable_ticks.append(QuestionableTick(self, offset))
                else:
                    if match.group(3):
                        # Start of a word, but is it inside quotes?
                        if inside_quote:
                            # Yes, queue this up as unknown
                            change_unknown.append(match.start(2))
                        else:
                            # Not in quotes. Must be a close.
                            must_change.append((match.start(2), "’"))
                    else:
                        # Tick after some punctuation and before a space, so close, but could also be end of a
                        # quote, so ask
                        must_change.append((match.start(2), "’"))
                        while change_unknown:
                            offset = change_unknown.pop()
                            questionable_ticks.append(QuestionableTick(self, offset))

            offset = match.end(2)

        # There was no matching end tick so leftovers must be close
        while change_unknown:
            must_change.append((change_unknown.pop(), "’"))

        # Change all queued up
        for offset, tick in must_change:
            self.text = self.text[:offset] + tick + self.text[offset + 1 :]

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return repr(self.text)


@attr.s
class QuestionableTick(object):
    paragraph: Paragraph = attr.ib()
    start: int = attr.ib()
    checkbox: wx.CheckBox = attr.ib(default=None)

    def __str__(self):
        match = SEARCH_END_TICK.search(self.paragraph.text, self.start + 1)
        return SEARCH_ITALIC_CHARS.sub("", self.paragraph.text[self.start : match.end(1)])

    def apply(self):
        self.paragraph.text = (
            self.paragraph.text[: self.start]
            + ("‘" if self.checkbox.IsChecked() else "’")
            + self.paragraph.text[self.start + 1 :]
        )
