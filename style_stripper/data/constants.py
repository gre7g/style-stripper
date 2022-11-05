import re
import wx

from style_stripper.data.enums import *

# Constants:
_ = wx.GetTranslation


class CONSTANTS(object):
    class MEASURING(object):
        EMUS_PER_INCH = 914400
        EMUS_PER_TWIP = 635
        EMUS_PER_CM = 360000
        TWIPS_PER_INCH = 1440
        TWIPS_PER_CM = 566.9291

    class DIVIDER(object):
        SEARCH = re.compile(r"\w")
        MAX_BLANK_PARAGRAPH_DIVIDERS = 400

    class ELLIPSES(object):
        SUB_SPACE = [
            (re.compile(r"(^| )(\.\.\.|…)( |$)"), r"\2"),
            (re.compile(r"(\W) (\.\.\.|…)"), r"\1\2"),
            (re.compile(r"(\W)(\.\.\.|…) "), r"\1\2"),
            (re.compile(r"(\.\.\.|…) (\W)"), r"\1\2"),
            (re.compile(r" (\.\.\.|…)(\W)"), r"\1\2"),
        ]
        SEARCH = re.compile(r"\.\.\.|…")

    class HEADINGS(object):
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

    class STYLING(object):
        class NAMES(object):
            FIRST_PARAGRAPH = "First Paragraph"
            NORMAL = "Normal"
            DIVIDER = "Separator"
            HEADING1 = "Heading 1"
            HEADING2 = "Heading 2"
            HEADER = "Header"
            FOOTER = "Footer"
            THE_END = "Separator"

    class UI(object):
        MAX_FILE_HISTORY = 8
        CATEGORY_NAME = "StyleStripper"
        CONFIG_PARAM = "configuration"
        APP_NAME = _("Style Stripper")
        APPLY_DELAY = 5  # 0.005s

        class PREVIEW(object):
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
                (OPEN_TO_PART, [SCOPE_ON_PART, SCOPE_ON_EVEN_HEADER]),
                (OPEN_TO_PART, []),
                (OPEN_TO_CHAPTER, [SCOPE_ON_CHAPTER, SCOPE_ON_EVEN_FOOTER]),
                (OPEN_TO_CHAPTER, []),
                (OPEN_TO_MID_CHAPTER, [SCOPE_ON_GUTTER, SCOPE_ON_ODD_HEADER, SCOPE_ON_ODD_FOOTER]),
                (OPEN_TO_MID_CHAPTER, [])
            ]
            CHAPTER_ONLY_PAGES = [
                (OPEN_TO_CHAPTER, [SCOPE_ON_CHAPTER, SCOPE_ON_EVEN_HEADER, SCOPE_ON_EVEN_FOOTER]),
                (OPEN_TO_CHAPTER, []),
                (OPEN_TO_MID_CHAPTER, [SCOPE_ON_GUTTER, SCOPE_ON_ODD_HEADER, SCOPE_ON_ODD_FOOTER]),
                (OPEN_TO_MID_CHAPTER, [])
            ]
