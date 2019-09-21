import os
import re
import wx

_ = wx.GetTranslation


class CONSTANTS(object):
    class MEASURING(object):
        EMUS_PER_INCH = 914400
        EMUS_PER_POINT = 12700
        EMUS_PER_CM = 360000

    class DIVIDER(object):
        SEARCH = [
            re.compile(r"^\s*❰?#\s*#\s*#❱?\s*$"),
            re.compile(r"^\s*❰?#❱?\s*$"),
            re.compile(r"^\s*❰?\*\s*\*\s*\*❱?\s*$"),
            re.compile(r"^\s*❰?\*❱?\s*$"),
        ]
        MAX_BLANK_PARAGRAPH_DIVIDERS = 400

    class ELLIPSES(object):
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
            THE_END = "Separator"

    class PAGE(object):
        TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docx_templates", "5x8+bleed.docx")

    class UI(object):
        MAX_FILE_HISTORY = 8
        CATEGORY_NAME = "StyleStripper"
        CONFIG_PARAM = "configuration"
        APP_NAME = _("Style Stripper")

        class PREVIEW(object):
            SCOPE_RADIUS = 0.15  # 15% of preview panel
            RULER_THICKNESS = 0.02  # 1.7% of preview panel
            GAP = 0.02  # 2% of preview panel
            PAGE_GAP = 914400 * 0.25  # 0.25"
            RULER_TEXT = 0.3  # 30% of ruler size
            TICK_FROM = 0.4  # Draw tick from 40%
            TICK_TO = 0.6  # to 60% point on ruler
