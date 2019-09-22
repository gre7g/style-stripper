from __future__ import annotations
import attr
from docx import Document
from docx.styles.style import BaseStyle
import re
from typing import Callable, Union, Optional, Dict

from style_stripper.data.constants import CONSTANTS

# Constants:
ParameterType = Union[None, int, str]
SEARCH_VARIANT = re.compile(r"&\d+")


def rounding(value: float) -> str:
    return str(round(value, 3)).rstrip(".0")


@attr.s
class StyleParameters(object):
    font: Optional[str] = attr.ib(default=None)
    font_size: Optional[int] = attr.ib(default=None)
    italic: Optional[bool] = attr.ib(default=None)
    bold: Optional[bool] = attr.ib(default=None)
    font_text: str = attr.ib(default="")
    alignment: Optional[int] = attr.ib(default=None)
    space_before: Optional[int] = attr.ib(default=None)
    space_after: Optional[int] = attr.ib(default=None)
    first_line_indent: Optional[int] = attr.ib(default=None)
    indent_imperial: str = attr.ib(default="")
    indent_metric: str = attr.ib(default="")
    line_spacing: Optional[Union[int, float]] = attr.ib(default=None)

    def init(self, style: BaseStyle) -> StyleParameters:
        self.font = self._find(style, lambda style: style.font.name)
        self.font_size = self._find(style, lambda style: style.font.size) / CONSTANTS.MEASURING.EMUS_PER_TWIP
        self.italic = bool(self._find(style, lambda style: style.font.italic))
        self.bold = bool(self._find(style, lambda style: style.font.bold))

        bold = " bold" if self.bold else ""
        italic = " italic" if self.italic else ""
        self.font_text = "%s %spt%s%s" % (self.font, rounding(self.font_size), bold, italic)

        self.alignment = self._find(style, lambda style: style.paragraph_format.alignment)
        self.space_before = (self._find(style, lambda style: style.paragraph_format.space_before) or 0) / \
            CONSTANTS.MEASURING.EMUS_PER_TWIP
        self.space_after = (self._find(style, lambda style: style.paragraph_format.space_after) or 0) / \
            CONSTANTS.MEASURING.EMUS_PER_TWIP

        self.first_line_indent = (self._find(style, lambda style: style.paragraph_format.first_line_indent) or 0) / \
            CONSTANTS.MEASURING.EMUS_PER_TWIP
        self.indent_imperial = '%s"' % rounding(self.first_line_indent / CONSTANTS.MEASURING.EMUS_PER_INCH)
        self.indent_metric = "%scm" % rounding(self.first_line_indent / CONSTANTS.MEASURING.EMUS_PER_CM)

        line_spacing = self._find(style, lambda style: style.paragraph_format.line_spacing) or self.font_size
        if isinstance(line_spacing, float):
            line_spacing *= self.font_size
        self.line_spacing = line_spacing / CONSTANTS.MEASURING.EMUS_PER_TWIP

        return self

    def _find(self, style: BaseStyle, fetch_func: Callable[[BaseStyle], ParameterType]) -> ParameterType:
        value = fetch_func(style)

        # None indicates that the style doesn't override settings in the base style. For None values, recurse into the
        # base style to find an actual value.
        if value is None:
            style = style.base_style
            if style is None:
                # Ran out of styles to check. Just leave the value None.
                return None
            else:
                return self._find(style, fetch_func)
        else:
            # Found one!
            return value


@attr.s
class TemplateParameters(object):
    comments: Optional[str] = attr.ib(default=None)
    head_foot_variant: int = attr.ib(default=1)
    different_first_page_header_footer: bool = attr.ib(default=True)
    page_height: Optional[int] = attr.ib(default=None)
    page_width: Optional[int] = attr.ib(default=None)
    top_margin: Optional[int] = attr.ib(default=None)
    bottom_margin: Optional[int] = attr.ib(default=None)
    left_margin: Optional[int] = attr.ib(default=None)
    right_margin: Optional[int] = attr.ib(default=None)
    header_distance: Optional[int] = attr.ib(default=None)
    footer_distance: Optional[int] = attr.ib(default=None)
    gutter: Optional[int] = attr.ib(default=None)

    height_imperial: str = attr.ib(default="")
    width_imperial: str = attr.ib(default="")
    top_imperial: str = attr.ib(default="")
    bottom_imperial: str = attr.ib(default="")
    left_imperial: str = attr.ib(default="")
    right_imperial: str = attr.ib(default="")
    header_imperial: str = attr.ib(default="")
    footer_imperial: str = attr.ib(default="")
    gutter_imperial: str = attr.ib(default="")

    height_metric: str = attr.ib(default="")
    width_metric: str = attr.ib(default="")
    top_metric: str = attr.ib(default="")
    bottom_metric: str = attr.ib(default="")
    left_metric: str = attr.ib(default="")
    right_metric: str = attr.ib(default="")
    header_metric: str = attr.ib(default="")
    footer_metric: str = attr.ib(default="")
    gutter_metric: str = attr.ib(default="")

    styles: Optional[Dict[str, StyleParameters]] = attr.ib(default={})

    def load(
        self, path: str  # Path to file
    ) -> None:
        doc = Document(path)

        # Basic info we need can be found in the first (only) section
        first_section = doc.sections[0]
        self.comments = doc.core_properties.comments

        match = SEARCH_VARIANT.search(self.comments)
        self.head_foot_variant = int(match.group()) if match else 1

        self.different_first_page_header_footer = bool(first_section.different_first_page_header_footer)
        self.page_height = first_section.page_height / CONSTANTS.MEASURING.EMUS_PER_TWIP
        self.page_width = first_section.page_width / CONSTANTS.MEASURING.EMUS_PER_TWIP
        self.top_margin = first_section.top_margin / CONSTANTS.MEASURING.EMUS_PER_TWIP
        self.bottom_margin = first_section.bottom_margin / CONSTANTS.MEASURING.EMUS_PER_TWIP
        self.left_margin = first_section.left_margin / CONSTANTS.MEASURING.EMUS_PER_TWIP
        self.right_margin = first_section.right_margin / CONSTANTS.MEASURING.EMUS_PER_TWIP
        self.header_distance = first_section.header_distance / CONSTANTS.MEASURING.EMUS_PER_TWIP
        self.footer_distance = first_section.footer_distance / CONSTANTS.MEASURING.EMUS_PER_TWIP
        self.gutter = first_section.gutter / CONSTANTS.MEASURING.EMUS_PER_TWIP

        self.height_imperial = '%s"' % rounding(first_section.page_height / CONSTANTS.MEASURING.EMUS_PER_INCH)
        self.width_imperial = '%s"' % rounding(first_section.page_width / CONSTANTS.MEASURING.EMUS_PER_INCH)
        self.top_imperial = '%s"' % rounding(first_section.top_margin / CONSTANTS.MEASURING.EMUS_PER_INCH)
        self.bottom_imperial = '%s"' % rounding(first_section.bottom_margin / CONSTANTS.MEASURING.EMUS_PER_INCH)
        self.left_imperial = '%s"' % rounding(first_section.left_margin / CONSTANTS.MEASURING.EMUS_PER_INCH)
        self.right_imperial = '%s"' % rounding(first_section.right_margin / CONSTANTS.MEASURING.EMUS_PER_INCH)
        self.header_imperial = '%s"' % rounding(first_section.header_distance / CONSTANTS.MEASURING.EMUS_PER_INCH)
        self.footer_imperial = '%s"' % rounding(first_section.footer_distance / CONSTANTS.MEASURING.EMUS_PER_INCH)
        self.gutter_imperial = '%s"' % rounding(first_section.gutter / CONSTANTS.MEASURING.EMUS_PER_INCH)

        self.height_metric = "%scm" % rounding(first_section.page_height / CONSTANTS.MEASURING.EMUS_PER_CM)
        self.width_metric = "%scm" % rounding(first_section.page_height / CONSTANTS.MEASURING.EMUS_PER_CM)
        self.top_metric = "%scm" % rounding(first_section.page_height / CONSTANTS.MEASURING.EMUS_PER_CM)
        self.bottom_metric = "%scm" % rounding(first_section.page_height / CONSTANTS.MEASURING.EMUS_PER_CM)
        self.left_metric = "%scm" % rounding(first_section.page_height / CONSTANTS.MEASURING.EMUS_PER_CM)
        self.right_metric = "%scm" % rounding(first_section.page_height / CONSTANTS.MEASURING.EMUS_PER_CM)
        self.header_metric = "%scm" % rounding(first_section.page_height / CONSTANTS.MEASURING.EMUS_PER_CM)
        self.footer_metric = "%scm" % rounding(first_section.page_height / CONSTANTS.MEASURING.EMUS_PER_CM)
        self.gutter_metric = "%scm" % rounding(first_section.page_height / CONSTANTS.MEASURING.EMUS_PER_CM)

        # Look up some info on the following styles:
        self.styles = {}
        for style in doc.styles:
            name = style.name
            if name in [
                CONSTANTS.STYLING.NAMES.NORMAL, CONSTANTS.STYLING.NAMES.HEADING1, CONSTANTS.STYLING.NAMES.HEADING2,
                CONSTANTS.STYLING.NAMES.HEADER, CONSTANTS.STYLING.NAMES.FOOTER, CONSTANTS.STYLING.NAMES.DIVIDER,
                CONSTANTS.STYLING.NAMES.FIRST_PARAGRAPH
            ]:
                self.styles[name] = StyleParameters().init(style)
