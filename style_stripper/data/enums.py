from enum import Enum, auto


class PanelType(Enum):
    AUTHOR = auto()
    TEMPLATE = auto()
    OPTIONS = auto()
    REVIEW = auto()
    DONE = auto()


class PageToShow(Enum):
    PART = auto()
    CHAPTER = auto()
    MID_CHAPTER = auto()


class ScopeOn(Enum):
    EVEN_HEADER = auto()
    ODD_HEADER = auto()
    EVEN_FOOTER = auto()
    ODD_FOOTER = auto()
    LEFT_MARGIN = auto()
    RIGHT_MARGIN = auto()
    GUTTER = auto()
    PART = auto()
    CHAPTER = auto()


class PaginationType(Enum):
    CONTINUOUS = auto()
    NEW_COLUMN = auto()
    NEW_PAGE = auto()
    EVEN_PAGE = auto()
    ODD_PAGE = auto()


class JustificationType(Enum):
    LEFT_JUSTIFIED = auto()
    CENTERED = auto()
    RIGHT_JUSTIFIED = auto()
    JUSTIFIED = auto()


class TextLineType(Enum):
    FIRST_LINE = auto()
    MIDDLE_LINE = auto()
    LAST_LINE = auto()
    ONLY_LINE = auto()


class Enums(Enum):
    SOURCE = auto()
    PATH = auto()
    TITLE = auto()
    WORD_COUNT = auto()
    LAST_MODIFIED = auto()
    HEADER = auto()
    FOOTER = auto()
    TOP_EDGE = auto()
    BOTTOM_EDGE = auto()
    LEFT_EDGE = auto()
    RIGHT_EDGE = auto()
    LEFT_MARGIN = auto()
    RIGHT_MARGIN = auto()
    ADD_THE_END = auto()
    THE_END = auto()


SOURCE = Enums.SOURCE
PATH = Enums.PATH
TITLE = Enums.TITLE
WORD_COUNT = Enums.WORD_COUNT
LAST_MODIFIED = Enums.LAST_MODIFIED
HEADER = Enums.HEADER
FOOTER = Enums.FOOTER
TOP_EDGE = Enums.TOP_EDGE
BOTTOM_EDGE = Enums.BOTTOM_EDGE
LEFT_EDGE = Enums.LEFT_EDGE
RIGHT_EDGE = Enums.RIGHT_EDGE
LEFT_MARGIN = Enums.LEFT_MARGIN
RIGHT_MARGIN = Enums.RIGHT_MARGIN
ADD_THE_END = Enums.ADD_THE_END
THE_END = Enums.THE_END
