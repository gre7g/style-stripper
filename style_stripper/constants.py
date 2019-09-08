from docx.enum.section import WD_SECTION
import os
import re


class CONSTANTS(object):
    class SPACES(object):
        PURGE_DOUBLE_SPACES = True
        PURGE_LEADING_WHITESPACE = True
        PURGE_TRAILING_WHITESPACE = True

    class ITALIC(object):
        ADJUST_TO_INCLUDE_PUNCTUATION = True

    class QUOTES(object):
        CONVERT_TO_CURLY = True

    class DIVIDER(object):
        SEARCH = [
            re.compile(r"^\s*❰?#\s*#\s*#❱?\s*$"),
            re.compile(r"^\s*❰?#❱?\s*$"),
            re.compile(r"^\s*❰?\*\s*\*\s*\*❱?\s*$"),
            re.compile(r"^\s*❰?\*❱?\s*$"),
        ]
        BLANK_PARAGRAPH_IF_NO_OTHER = True
        MAX_BLANK_PARAGRAPH_DIVIDERS = 1000
        REPLACE_DIVIDER_WITH_NEW = True
        NEW_DIVIDER = "# # #"
        REMOVE_DIVIDERS_BEFORE_HEADINGS = True

    class HEADINGS(object):
        STYLE_PART = True
        STYLE_CHAPTER = True
        STYLE_THE_END = True
        FLATTEN_IF_NO_PARTS = True
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
        HEADER_FOOTER_AFTER_BREAK = False
        BREAK_BEFORE_HEADING = WD_SECTION.ODD_PAGE

    class DASHES(object):
        CONVERT_DOUBLE_DASHES = True
        CONVERT_TO_EN_DASH = False
        CONVERT_TO_EM_DASH = True
        FIX_DASH_AT_END_OF_QUOTE = True
        FORCE_ALL_EN_OR_EM = True

    class STYLING(object):
        INDENT_INCHES = 0.5
        INDENT_FIRST_PARAGRAPH = False
        CENTER_DIVIDER = True

        class NAMES(object):
            FIRST_PARAGRAPH = "First Paragraph"
            NORMAL = "Normal"
            DIVIDER = "Separator"
            HEADING1 = "Heading 1"
            HEADING2 = "Heading 2"
            THE_END = "Separator"

    class PAGE(object):
        TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docx_templates", "5x8+bleed.docx")
