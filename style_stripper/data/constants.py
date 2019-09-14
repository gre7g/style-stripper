import os
import re


class CONSTANTS(object):
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
