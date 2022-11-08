from dataclasses import dataclass
from docx.enum.section import WD_SECTION_START  # noqa
import os
import re
import sys
from typing import List
import wx

from style_stripper.data.enums import PageToShow, ScopeOn, PaginationType

# Constants:
_ = wx.GetTranslation


@dataclass
class PageScopes:
    page: PageToShow
    scopes: List[ScopeOn]


# Types:
ListPageScopes = List[PageScopes]


class CONSTANTS:
    class PATHS:
        TEMPLATES_PATH = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "docx_templates"
        )
        if sys.argv[0].endswith(".exe"):
            BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
        else:
            BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

    class DOCUMENTS:
        SEARCH_DIMENSIONS = re.compile(r"(\d+(?:\.\d+)?)x(\d+(?:\.\d+)?)")
        DIMENSIONS = [
            '5" x 8"',
            '5.06" x 7.81"',
            '5.25" x 8"',
            '5.5" x 8.5"',
            '6" x 9"',
            '6.14" x 9.21"',
            '6.69" x 9.61"',
            '7" x 10"',
            '7.44" x 9.69"',
            '7.5" x 9.25"',
            '8" x 10"',
            '8.25" x 6"',
            '8.25" x 8.25"',
            '8.5" x 11"',
            '8.27" x 11.69"',
        ]

    class MEASURING:
        EMUS_PER_INCH = 914400
        EMUS_PER_TWIP = 635
        EMUS_PER_CM = 360000
        TWIPS_PER_INCH = 1440
        TWIPS_PER_CM = 566.9291

    class STYLING:
        class NAMES:
            FIRST_PARAGRAPH = "First Paragraph"
            NORMAL = "Normal"
            DIVIDER = "Separator"
            HEADING1 = "Heading 1"
            HEADING2 = "Heading 2"
            HEADER = "Header"
            FOOTER = "Footer"
            THE_END = "Separator"

    class HEADINGS:
        SEARCH_PART = [re.compile(r"^\s*Part [\dIV]\w*\s*$")]
        SEARCH_CHAPTER = [re.compile(r"^\s*Chapter \d+(:\s+.+)?")]
        SEARCH_THE_END = [
            re.compile(r"^\s*The End\s*$", re.I),
            re.compile(r"^\s*fin\s*$", re.I),
        ]
        BREAK_MAP = {
            PaginationType.NEW_PAGE: WD_SECTION_START.NEW_PAGE,
            PaginationType.ODD_PAGE: WD_SECTION_START.ODD_PAGE,
            PaginationType.EVEN_PAGE: WD_SECTION_START.EVEN_PAGE,
        }

    class PARAGRAPHS:
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

    class DIVIDER:
        SEARCH = re.compile(r"\w")
        MAX_BLANK_PARAGRAPH_DIVIDERS = 400

    class ELLIPSES:
        SUB_SPACE = [
            (re.compile(r"(^| )(\.\.\.|…)( |$)"), r"\2"),
            (re.compile(r"(\W) (\.\.\.|…)"), r"\1\2"),
            (re.compile(r"(\W)(\.\.\.|…) "), r"\1\2"),
            (re.compile(r"(\.\.\.|…) (\W)"), r"\1\2"),
            (re.compile(r" (\.\.\.|…)(\W)"), r"\1\2"),
        ]
        SEARCH = re.compile(r"\.\.\.|…")

    class ITALIC:
        SEARCH = re.compile(r"❰(.*?)❱")

    class UI:
        MAX_FILE_HISTORY = 8
        CATEGORY_NAME = "StyleStripper"
        CONFIG_PARAM = "configuration"
        APP_NAME = _("Style Stripper")
        APPLY_DELAY = 5  # 0.005s

        class PREVIEW:
            SCOPE_RADIUS = 0.15  # 15% of preview panel
            SCOPE_SEGMENTS = 15  # a 15-gram is nearly a circle
            RULER_THICKNESS = 0.02  # 2% of preview panel
            GAP = 0.02  # 2% of preview panel
            PAGE_GAP = int(1440 * 0.25)  # 0.25"
            RULER_TEXT = 0.3  # 30% of ruler size
            TICK_FROM = 0.4  # Draw tick from 40%
            TICK_TO = 0.6  # to 60% point on ruler
            TEXT_TO_OPPOSITE_PART = 0.7  # 70% text opposite the part page
            TEXT_TO_OPPOSITE_CHAPTER = 0.4  # 40% text opposite the chapter page
            MAGNIFIER_SCALING = 3.0  # 3x magnification
            MEDIUM_GREY = (160, 160, 255)
            LIGHT_GREY = (240, 240, 255)
            MID_TEXT_OFFSET = 0.7  # 70% of text height
            LINE_SPACING = 1.6  # +60% font size
            PART_AND_CHAPTER_PAGES = [
                PageScopes(PageToShow.PART, [ScopeOn.PART, ScopeOn.EVEN_HEADER]),
                PageScopes(PageToShow.PART, []),
                PageScopes(PageToShow.CHAPTER, [ScopeOn.CHAPTER, ScopeOn.EVEN_FOOTER]),
                PageScopes(PageToShow.CHAPTER, []),
                PageScopes(
                    PageToShow.MID_CHAPTER,
                    [ScopeOn.GUTTER, ScopeOn.ODD_HEADER, ScopeOn.ODD_FOOTER],
                ),
                PageScopes(PageToShow.MID_CHAPTER, []),
            ]
            CHAPTER_ONLY_PAGES = [
                PageScopes(
                    PageToShow.CHAPTER,
                    [ScopeOn.CHAPTER, ScopeOn.EVEN_HEADER, ScopeOn.EVEN_FOOTER],
                ),
                PageScopes(PageToShow.CHAPTER, []),
                PageScopes(
                    PageToShow.MID_CHAPTER,
                    [ScopeOn.GUTTER, ScopeOn.ODD_HEADER, ScopeOn.ODD_FOOTER],
                ),
                PageScopes(PageToShow.MID_CHAPTER, []),
            ]
