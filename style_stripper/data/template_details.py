from dataclasses import dataclass, field
from docx import Document
from docx.styles.style import BaseStyle
from typing import Callable, Union, Optional, Dict

from style_stripper.data.constants import CONSTANTS

# Constants:
ParameterType = Union[None, int, str]


def rounding(value: float) -> str:
    return str(round(value, 3)).rstrip(".0")


@dataclass
class StyleParameters:
    font: Optional[str] = None
    font_size: Optional[int] = None
    italic: Optional[bool] = None
    bold: Optional[bool] = None
    font_text: str = ""
    alignment: Optional[int] = None
    space_before: Optional[int] = None
    before_text: Optional[str] = ""
    space_after: Optional[int] = None
    after_text: Optional[str] = ""
    first_line_indent: Optional[int] = None
    indent_imperial: str = ""
    indent_metric: str = ""
    line_spacing: Optional[Union[int, float]] = None

    def init(self, style: BaseStyle):
        self.font = self._find(style, lambda a_style: a_style.font.name)
        self.font_size = (
            self._find(style, lambda a_style: a_style.font.size)
            / CONSTANTS.MEASURING.EMUS_PER_TWIP
        )
        self.italic = bool(self._find(style, lambda a_style: a_style.font.italic))
        self.bold = bool(self._find(style, lambda a_style: a_style.font.bold))

        bold = " bold" if self.bold else ""
        italic = " italic" if self.italic else ""
        self.font_text = "%s %spt%s%s" % (
            self.font,
            rounding(self.font_size),
            bold,
            italic,
        )

        self.alignment = self._find(
            style, lambda a_style: a_style.paragraph_format.alignment
        )
        self.space_before = (
            self._find(style, lambda a_style: a_style.paragraph_format.space_before)
            or 0
        ) / CONSTANTS.MEASURING.EMUS_PER_TWIP
        self.before_text = "%spt" % rounding(self.space_before)
        self.space_after = (
            self._find(style, lambda a_style: a_style.paragraph_format.space_after) or 0
        ) / CONSTANTS.MEASURING.EMUS_PER_TWIP
        self.after_text = "%spt" % rounding(self.space_after)

        self.first_line_indent = (
            self._find(
                style, lambda a_style: a_style.paragraph_format.first_line_indent
            )
            or 0
        ) / CONSTANTS.MEASURING.EMUS_PER_TWIP
        self.indent_imperial = '%s"' % rounding(
            self.first_line_indent / CONSTANTS.MEASURING.EMUS_PER_INCH
        )
        self.indent_metric = "%scm" % rounding(
            self.first_line_indent / CONSTANTS.MEASURING.EMUS_PER_CM
        )

        line_spacing = (
            self._find(style, lambda a_style: a_style.paragraph_format.line_spacing)
            or self.font_size
        )
        if isinstance(line_spacing, float):
            line_spacing *= self.font_size
        self.line_spacing = line_spacing / CONSTANTS.MEASURING.EMUS_PER_TWIP

        return self

    def _find(
        self, style: BaseStyle, fetch_func: Callable[[BaseStyle], ParameterType]
    ) -> ParameterType:
        # Styles are a bit like subclasses: just like how a subclass may overload a function, a style may overload which
        # font to use. If a style doesn't specify a font, you need to check the base style (recursively) to see if it
        # specifies the font. This function lets you find an attribute value from a style (and its bases).
        value = fetch_func(style)

        # None indicates that the style doesn't override the setting in the base style
        if value is None:
            # Let's recurse into the base style
            style = style.base_style  # noqa (dunno why this isn't defined)
            return None if style is None else self._find(style, fetch_func)
        else:
            # Found one!
            return value


@dataclass
class TemplateParameters:
    comments: Optional[str] = None
    head_foot_variant: int = 1
    pages_per_100k: int = 300
    part_and_chapter: bool = True
    different_first_page_header_footer: bool = True
    page_height: Optional[int] = None
    page_width: Optional[int] = None
    top_margin: Optional[int] = None
    bottom_margin: Optional[int] = None
    left_margin: Optional[int] = None
    right_margin: Optional[int] = None
    header_distance: Optional[int] = None
    footer_distance: Optional[int] = None
    gutter: Optional[int] = None

    height_imperial: str = ""
    width_imperial: str = ""
    top_imperial: str = ""
    bottom_imperial: str = ""
    left_imperial: str = ""
    right_imperial: str = ""
    header_imperial: str = ""
    footer_imperial: str = ""
    gutter_imperial: str = ""

    height_metric: str = ""
    width_metric: str = ""
    top_metric: str = ""
    bottom_metric: str = ""
    left_metric: str = ""
    right_metric: str = ""
    header_metric: str = ""
    footer_metric: str = ""
    gutter_metric: str = ""

    styles: Optional[Dict[str, StyleParameters]] = field(default_factory=dict)

    def load(self, path: Union[str, Document]):  # Path to file
        doc = Document(path) if isinstance(path, str) else path

        # Basic info we need can be found in the first (only) section
        first_section = doc.sections[0]
        self.comments = doc.core_properties.comments

        parts = self.comments.split(",")
        self.head_foot_variant = int(parts[0])
        self.pages_per_100k = int(parts[1])
        self.part_and_chapter = parts[2] == "1"

        self.different_first_page_header_footer = bool(
            first_section.different_first_page_header_footer
        )
        self.page_height = first_section.page_height / CONSTANTS.MEASURING.EMUS_PER_TWIP
        self.page_width = first_section.page_width / CONSTANTS.MEASURING.EMUS_PER_TWIP
        self.top_margin = first_section.top_margin / CONSTANTS.MEASURING.EMUS_PER_TWIP
        self.bottom_margin = (
            first_section.bottom_margin / CONSTANTS.MEASURING.EMUS_PER_TWIP
        )
        self.left_margin = first_section.left_margin / CONSTANTS.MEASURING.EMUS_PER_TWIP
        self.right_margin = (
            first_section.right_margin / CONSTANTS.MEASURING.EMUS_PER_TWIP
        )
        self.header_distance = (
            first_section.header_distance / CONSTANTS.MEASURING.EMUS_PER_TWIP
        )
        self.footer_distance = (
            first_section.footer_distance / CONSTANTS.MEASURING.EMUS_PER_TWIP
        )
        self.gutter = first_section.gutter / CONSTANTS.MEASURING.EMUS_PER_TWIP

        self.height_imperial = '%s"' % rounding(
            first_section.page_height / CONSTANTS.MEASURING.EMUS_PER_INCH
        )
        self.width_imperial = '%s"' % rounding(
            first_section.page_width / CONSTANTS.MEASURING.EMUS_PER_INCH
        )
        self.top_imperial = '%s"' % rounding(
            first_section.top_margin / CONSTANTS.MEASURING.EMUS_PER_INCH
        )
        self.bottom_imperial = '%s"' % rounding(
            first_section.bottom_margin / CONSTANTS.MEASURING.EMUS_PER_INCH
        )
        self.left_imperial = '%s"' % rounding(
            first_section.left_margin / CONSTANTS.MEASURING.EMUS_PER_INCH
        )
        self.right_imperial = '%s"' % rounding(
            first_section.right_margin / CONSTANTS.MEASURING.EMUS_PER_INCH
        )
        self.header_imperial = '%s"' % rounding(
            first_section.header_distance / CONSTANTS.MEASURING.EMUS_PER_INCH
        )
        self.footer_imperial = '%s"' % rounding(
            first_section.footer_distance / CONSTANTS.MEASURING.EMUS_PER_INCH
        )
        self.gutter_imperial = '%s"' % rounding(
            first_section.gutter / CONSTANTS.MEASURING.EMUS_PER_INCH
        )

        self.height_metric = "%scm" % rounding(
            first_section.page_height / CONSTANTS.MEASURING.EMUS_PER_CM
        )
        self.width_metric = "%scm" % rounding(
            first_section.page_height / CONSTANTS.MEASURING.EMUS_PER_CM
        )
        self.top_metric = "%scm" % rounding(
            first_section.page_height / CONSTANTS.MEASURING.EMUS_PER_CM
        )
        self.bottom_metric = "%scm" % rounding(
            first_section.page_height / CONSTANTS.MEASURING.EMUS_PER_CM
        )
        self.left_metric = "%scm" % rounding(
            first_section.page_height / CONSTANTS.MEASURING.EMUS_PER_CM
        )
        self.right_metric = "%scm" % rounding(
            first_section.page_height / CONSTANTS.MEASURING.EMUS_PER_CM
        )
        self.header_metric = "%scm" % rounding(
            first_section.page_height / CONSTANTS.MEASURING.EMUS_PER_CM
        )
        self.footer_metric = "%scm" % rounding(
            first_section.page_height / CONSTANTS.MEASURING.EMUS_PER_CM
        )
        self.gutter_metric = "%scm" % rounding(
            first_section.page_height / CONSTANTS.MEASURING.EMUS_PER_CM
        )

        # Look up some info on the following styles:
        self.styles = {}
        for style in doc.styles:
            name = style.name
            if name in [
                CONSTANTS.STYLING.NAMES.NORMAL,
                CONSTANTS.STYLING.NAMES.HEADING1,
                CONSTANTS.STYLING.NAMES.HEADING2,
                CONSTANTS.STYLING.NAMES.HEADER,
                CONSTANTS.STYLING.NAMES.FOOTER,
                CONSTANTS.STYLING.NAMES.DIVIDER,
                CONSTANTS.STYLING.NAMES.FIRST_PARAGRAPH,
            ]:
                self.styles[name] = StyleParameters().init(style)
