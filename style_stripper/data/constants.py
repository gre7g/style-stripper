from dataclasses import dataclass
import os
import re
import sys
from typing import List
import wx

from style_stripper.data.enums import PageToShow, ScopeOn

# Constants:
_ = wx.GetTranslation


@dataclass
class PageScopes:
    page: PageToShow
    scopes: List[ScopeOn]


# Types:
ListPageScopes: List[PageScopes]


class CONSTANTS:
    class PATHS:
        TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docx_templates")
        if sys.argv[0].endswith(".exe"):
            BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
        else:
            BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

    class MEASURING:
        EMUS_PER_INCH = 914400
        EMUS_PER_TWIP = 635
        EMUS_PER_CM = 360000
        TWIPS_PER_INCH = 1440
        TWIPS_PER_CM = 566.9291

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

    class HEADINGS:
        SEARCH_PART = [
            re.compile(r"^\s*Part [\dIV]\w*\s*$")
        ]
        SEARCH_CHAPTER = [
            re.compile(r"^\s*Chapter \d+(:\s+.+)?")
        ]
        SEARCH_THE_END = [
            re.compile(r"^\s*The End\s*$", re.I),
            re.compile(r"^\s*fin\s*$", re.I),
        ]

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

    class UI:
        MAX_FILE_HISTORY = 8
        CATEGORY_NAME = "StyleStripper"
        CONFIG_PARAM = "configuration"
        APP_NAME = _("Style Stripper")
        APPLY_DELAY = 5  # 0.005s

        class PREVIEW:
            SCOPE_RADIUS = 0.15  # 15% of preview panel
            RULER_THICKNESS = 0.02  # 2% of preview panel
            GAP = 0.02  # 2% of preview panel
            PAGE_GAP = 1440 * 0.25  # 0.25"
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
                PageScopes(PageToShow.MID_CHAPTER, [ScopeOn.GUTTER, ScopeOn.ODD_HEADER, ScopeOn.ODD_FOOTER]),
                PageScopes(PageToShow.MID_CHAPTER, [])
            ]
            CHAPTER_ONLY_PAGES = [
                PageScopes(PageToShow.CHAPTER, [ScopeOn.CHAPTER, ScopeOn.EVEN_HEADER, ScopeOn.EVEN_FOOTER]),
                PageScopes(PageToShow.CHAPTER, []),
                PageScopes(PageToShow.MID_CHAPTER, [ScopeOn.GUTTER, ScopeOn.ODD_HEADER, ScopeOn.ODD_FOOTER]),
                PageScopes(PageToShow.MID_CHAPTER, [])
            ]
