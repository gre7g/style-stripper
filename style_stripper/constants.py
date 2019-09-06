import re


class CONSTANTS(object):
    class SPACES(object):
        PURGE_DOUBLE_SPACES = True

    class QUOTES(object):
        CONVERT_TO_CURLY = True

    class DIVIDER(object):
        SEARCH = [
            re.compile(r"^\s*#\s*#\s*#\s*$"),
            re.compile(r"^\s*#\s*$"),
            re.compile(r"^\s*\*\s*\*\s*\*\s*$"),
            re.compile(r"^\s*\*\s*$"),
        ]
        BLANK_PARAGRAPH_IF_NO_OTHER = True
        MAX_BLANK_PARAGRAPH_DIVIDERS = 1000

    class DASHES(object):
        CONVERT_DOUBLE_DASHES = True
        CONVERT_TO_EN_DASH = False
        CONVERT_TO_EM_DASH = True

    class STYLING(object):
        INDENT_INCHES = 0.5
        INDENT_FIRST_PARAGRAPH = False
        CENTER_DIVIDER = True

    class PAGE(object):
        WIDTH_INCHES = 5.5
        HEIGHT_INCHES = 8.5
