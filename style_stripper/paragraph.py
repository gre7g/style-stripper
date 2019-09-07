"""Paragraphs"""

import logging
import re

from style_stripper.constants import CONSTANTS

# Constants:
ITALIC_START = "❰"
ITALIC_STOP = "❱"
SEARCH_LEADING_WHITESPACE = re.compile(r"^\s+")
SEARCH_TRAILING_WHITESPACE = re.compile(r"\s+$")
SEARCH_DOUBLE_WHITESPACE = re.compile(r"\s{2,}")
SEARCH_ITALIC_WHITE1 = re.compile(r"❱(\s*)❰")
SEARCH_ITALIC_WHITE2 = re.compile(r"❰(\s+)")
SEARCH_ITALIC_WHITE3 = re.compile(r"(\s+)❱")
SEARCH_ITALIC_WHITE4 = re.compile("(\S+)❰")
SEARCH_ITALIC_WHITE5 = re.compile("❱(\S+)")
SEARCH_BROKEN_QUOTE1 = re.compile(r"”\s*-+\s*")
SEARCH_BROKEN_QUOTE2 = re.compile(r"\s*-+\s*“")
SEARCH_DASHES = re.compile(r"\s*-{2,}\s*")
SEARCH_ANY_QUOTE = re.compile('["“”]')
SEARCH_QUOTES_OR_TICKS = re.compile(r"[“”‘’]")
LOG = logging.getLogger(__name__)


class Paragraph(object):
    text: str

    def __init__(self) -> None:
        self.text = ""
        self.dash = "—" if CONSTANTS.DASHES.CONVERT_TO_EM_DASH else " – "

    def add(self, text: str, italic: bool) -> None:
        if italic:
            if self.text.endswith("❱"):
                self.text = self.text[:-1] + text + "❱"
            else:
                self.text += "❰%s❱" % text
        else:
            self.text += text

    def fix_spaces(self) -> None:
        if CONSTANTS.SPACES.PURGE_LEADING_WHITESPACE:
            self.text = SEARCH_LEADING_WHITESPACE.sub("", self.text)

        if CONSTANTS.SPACES.PURGE_TRAILING_WHITESPACE:
            self.text = SEARCH_TRAILING_WHITESPACE.sub("", self.text)

        if CONSTANTS.SPACES.PURGE_DOUBLE_SPACES:
            self.text = SEARCH_DOUBLE_WHITESPACE.sub(" ", self.text)

    def fix_quotes_and_dashes(self) -> None:
        if CONSTANTS.QUOTES.CONVERT_TO_CURLY:
            even = True
            for match in SEARCH_ANY_QUOTE.finditer(self.text):
                even = not even
                quote = '”' if even else '“'
                self.text = self.text[:match.start()] + quote + self.text[match.end():]

            # Can only fix dashes if we fix quotes
            if CONSTANTS.DASHES.CONVERT_TO_EM_DASH or CONSTANTS.DASHES.CONVERT_TO_EN_DASH:
                self.text = SEARCH_BROKEN_QUOTE1.sub("”" + self.dash, self.text)
                self.text = SEARCH_BROKEN_QUOTE2.sub(self.dash + "“", self.text)
            if CONSTANTS.DASHES.CONVERT_DOUBLE_DASHES:
                self.text = SEARCH_DASHES.sub(self.dash, self.text)

    def fix_italic_boundaries(self):
        if CONSTANTS.ITALIC.ADJUST_TO_INCLUDE_PUNCTUATION:
            self.text = SEARCH_ITALIC_WHITE1.sub(r"\1", self.text)
            self.text = SEARCH_ITALIC_WHITE2.sub(r"\1❰", self.text)
            self.text = SEARCH_ITALIC_WHITE3.sub(r"❱\1", self.text)
            self.text = SEARCH_ITALIC_WHITE4.sub(r"❰\1", self.text)
            self.text = SEARCH_ITALIC_WHITE5.sub(r"\1❱", self.text)

    # def fix_ticks(self):
    #     if CONSTANTS.QUOTES.CONVERT_TO_CURLY:

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return repr(self.text)
