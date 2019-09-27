from enum import Enum, auto


class Enums(Enum):
    SOURCE = auto()
    PATH = auto()
    AUTHOR = auto()
    TITLE = auto()
    WORD_COUNT = auto()
    LAST_MODIFIED = auto()
    SPACES = auto()
    PURGE_DOUBLE_SPACES = auto()
    PURGE_LEADING_WHITESPACE = auto()
    PURGE_TRAILING_WHITESPACE = auto()
    ITALIC = auto()
    ADJUST_TO_INCLUDE_PUNCTUATION = auto()
    QUOTES = auto()
    CONVERT_TO_CURLY = auto()
    DIVIDER = auto()
    BLANK_PARAGRAPH_IF_NO_OTHER = auto()
    REPLACE_WITH_NEW = auto()
    NEW = auto()
    REMOVE_DIVIDERS_BEFORE_HEADINGS = auto()
    ELLIPSES = auto()
    HEADINGS = auto()
    STYLE_PARTS_AND_CHAPTER = auto()
    STYLE_THE_END = auto()
    HEADER_FOOTER_AFTER_BREAK = auto()
    BREAK_BEFORE_HEADING = auto()
    DASHES = auto()
    CONVERT_DOUBLE_DASHES = auto()
    CONVERT_TO_EN_DASH = auto()
    CONVERT_TO_EM_DASH = auto()
    FIX_DASH_AT_END_OF_QUOTE = auto()
    FORCE_ALL_EN_OR_EM = auto()
    STYLING = auto()
    NAMES = auto()
    INDENT_FIRST_PARAGRAPH = auto()
    CENTER_DIVIDER = auto()
    CONTINUOUS = auto()
    NEW_COLUMN = auto()
    NEW_PAGE = auto()
    EVEN_PAGE = auto()
    ODD_PAGE = auto()
    OPEN_TO_PART = auto()
    OPEN_TO_CHAPTER = auto()
    OPEN_TO_MID_CHAPTER = auto()
    SCOPE_ON_EVEN_HEADER = auto()
    SCOPE_ON_ODD_HEADER = auto()
    SCOPE_ON_EVEN_FOOTER = auto()
    SCOPE_ON_ODD_FOOTER = auto()
    SCOPE_ON_LEFT_MARGIN = auto()
    SCOPE_ON_RIGHT_MARGIN = auto()
    SCOPE_ON_GUTTER = auto()
    SCOPE_ON_PART = auto()
    SCOPE_ON_CHAPTER = auto()
    LEFT_JUSTIFIED = auto()
    CENTERED = auto()
    RIGHT_JUSTIFIED = auto()
    JUSTIFIED = auto()
    HEADER = auto()
    FOOTER = auto()
    TOP_EDGE = auto()
    BOTTOM_EDGE = auto()
    LEFT_EDGE = auto()
    RIGHT_EDGE = auto()
    LEFT_MARGIN = auto()
    RIGHT_MARGIN = auto()
    FIRST_LINE = auto()
    MIDDLE_LINE = auto()
    LAST_LINE = auto()
    ONLY_LINE = auto()
    ADD_THE_END = auto()
    THE_END = auto()
    STATE_READY = auto()
    STATE_DONE = auto()
    STATE_SEARCH_HEADINGS = auto()
    STATE_SEARCH_DIVIDERS = auto()
    STATE_REPLACE_HEADINGS = auto()
    STATE_FIX_SPACES = auto()
    STATE_FIX_ITALICS = auto()
    STATE_FIX_QUOTES_AND_DASHES = auto()
    STATE_FIX_TICKS = auto()


SOURCE = Enums.SOURCE
PATH = Enums.PATH
AUTHOR = Enums.AUTHOR
TITLE = Enums.TITLE
WORD_COUNT = Enums.WORD_COUNT
LAST_MODIFIED = Enums.LAST_MODIFIED
SPACES = Enums.SPACES
PURGE_DOUBLE_SPACES = Enums.PURGE_DOUBLE_SPACES
PURGE_LEADING_WHITESPACE = Enums.PURGE_LEADING_WHITESPACE
PURGE_TRAILING_WHITESPACE = Enums.PURGE_TRAILING_WHITESPACE
ITALIC = Enums.ITALIC
ADJUST_TO_INCLUDE_PUNCTUATION = Enums.ADJUST_TO_INCLUDE_PUNCTUATION
QUOTES = Enums.QUOTES
CONVERT_TO_CURLY = Enums.CONVERT_TO_CURLY
DIVIDER = Enums.DIVIDER
BLANK_PARAGRAPH_IF_NO_OTHER = Enums.BLANK_PARAGRAPH_IF_NO_OTHER
REPLACE_WITH_NEW = Enums.REPLACE_WITH_NEW
NEW = Enums.NEW
REMOVE_DIVIDERS_BEFORE_HEADINGS = Enums.REMOVE_DIVIDERS_BEFORE_HEADINGS
ELLIPSES = Enums.ELLIPSES
HEADINGS = Enums.HEADINGS
STYLE_PARTS_AND_CHAPTER = Enums.STYLE_PARTS_AND_CHAPTER
STYLE_THE_END = Enums.STYLE_THE_END
HEADER_FOOTER_AFTER_BREAK = Enums.HEADER_FOOTER_AFTER_BREAK
BREAK_BEFORE_HEADING = Enums.BREAK_BEFORE_HEADING
DASHES = Enums.DASHES
CONVERT_DOUBLE_DASHES = Enums.CONVERT_DOUBLE_DASHES
CONVERT_TO_EN_DASH = Enums.CONVERT_TO_EN_DASH
CONVERT_TO_EM_DASH = Enums.CONVERT_TO_EM_DASH
FIX_DASH_AT_END_OF_QUOTE = Enums.FIX_DASH_AT_END_OF_QUOTE
FORCE_ALL_EN_OR_EM = Enums.FORCE_ALL_EN_OR_EM
STYLING = Enums.STYLING
NAMES = Enums.NAMES
INDENT_FIRST_PARAGRAPH = Enums.INDENT_FIRST_PARAGRAPH
CENTER_DIVIDER = Enums.CENTER_DIVIDER
CONTINUOUS = Enums.CONTINUOUS
NEW_COLUMN = Enums.NEW_COLUMN
NEW_PAGE = Enums.NEW_PAGE
EVEN_PAGE = Enums.EVEN_PAGE
ODD_PAGE = Enums.ODD_PAGE
OPEN_TO_PART = Enums.OPEN_TO_PART
OPEN_TO_CHAPTER = Enums.OPEN_TO_CHAPTER
OPEN_TO_MID_CHAPTER = Enums.OPEN_TO_MID_CHAPTER
SCOPE_ON_EVEN_HEADER = Enums.SCOPE_ON_EVEN_HEADER
SCOPE_ON_ODD_HEADER = Enums.SCOPE_ON_ODD_HEADER
SCOPE_ON_EVEN_FOOTER = Enums.SCOPE_ON_EVEN_FOOTER
SCOPE_ON_ODD_FOOTER = Enums.SCOPE_ON_ODD_FOOTER
SCOPE_ON_LEFT_MARGIN = Enums.SCOPE_ON_LEFT_MARGIN
SCOPE_ON_RIGHT_MARGIN = Enums.SCOPE_ON_RIGHT_MARGIN
SCOPE_ON_GUTTER = Enums.SCOPE_ON_GUTTER
SCOPE_ON_PART = Enums.SCOPE_ON_PART
SCOPE_ON_CHAPTER = Enums.SCOPE_ON_CHAPTER
LEFT_JUSTIFIED = Enums.LEFT_JUSTIFIED
CENTERED = Enums.CENTERED
RIGHT_JUSTIFIED = Enums.RIGHT_JUSTIFIED
JUSTIFIED = Enums.JUSTIFIED
HEADER = Enums.HEADER
FOOTER = Enums.FOOTER
TOP_EDGE = Enums.TOP_EDGE
BOTTOM_EDGE = Enums.BOTTOM_EDGE
LEFT_EDGE = Enums.LEFT_EDGE
RIGHT_EDGE = Enums.RIGHT_EDGE
LEFT_MARGIN = Enums.LEFT_MARGIN
RIGHT_MARGIN = Enums.RIGHT_MARGIN
FIRST_LINE = Enums.FIRST_LINE
MIDDLE_LINE = Enums.MIDDLE_LINE
LAST_LINE = Enums.LAST_LINE
ONLY_LINE = Enums.ONLY_LINE
ADD_THE_END = Enums.ADD_THE_END
THE_END = Enums.THE_END
STATE_READY = Enums.STATE_READY
STATE_DONE = Enums.STATE_DONE
STATE_SEARCH_HEADINGS = Enums.STATE_SEARCH_HEADINGS
STATE_SEARCH_DIVIDERS = Enums.STATE_SEARCH_DIVIDERS
STATE_REPLACE_HEADINGS = Enums.STATE_REPLACE_HEADINGS
STATE_FIX_SPACES = Enums.STATE_FIX_SPACES
STATE_FIX_ITALICS = Enums.STATE_FIX_ITALICS
STATE_FIX_QUOTES_AND_DASHES = Enums.STATE_FIX_QUOTES_AND_DASHES
STATE_FIX_TICKS = Enums.STATE_FIX_TICKS
