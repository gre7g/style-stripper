from enum import Enum, auto


class PanelType(Enum):
    AUTHOR = 1
    TEMPLATE = 2
    OPTIONS = 3
    REVIEW = 4
    DONE = 5


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


# class Enums(Enum):
#     HEADER = auto()
#     FOOTER = auto()
#     LEFT_MARGIN = auto()
#     RIGHT_MARGIN = auto()
#     THE_END = auto()
