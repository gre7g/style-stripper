from __future__ import annotations
import attr
from docx import Document
from docx.styles.style import BaseStyle
from typing import Callable, Union, Optional, Dict

# Constants:
ParameterType = Union[None, int, str]


@attr.s
class StyleParameters(object):
    font: Optional[str] = attr.ib(default=None)
    font_size: Optional[int] = attr.ib(default=None)
    italic: Optional[bool] = attr.ib(default=None)
    bold: Optional[bool] = attr.ib(default=None)
    alignment: Optional[int] = attr.ib(default=None)
    space_before: Optional[int] = attr.ib(default=None)
    space_after: Optional[int] = attr.ib(default=None)
    first_line_indent: Optional[int] = attr.ib(default=None)
    line_spacing: Optional[Union[int, float]] = attr.ib(default=None)

    def init(self, style: BaseStyle) -> StyleParameters:
        self.font = self._find(style, lambda style: style.font.name)
        self.font_size = self._find(style, lambda style: style.font.size)
        self.italic = bool(self._find(style, lambda style: style.font.italic))
        self.bold = bool(self._find(style, lambda style: style.font.bold))
        self.alignment = self._find(style, lambda style: style.paragraph_format.alignment)
        self.space_before = self._find(style, lambda style: style.paragraph_format.space_before) or 0
        self.space_after = self._find(style, lambda style: style.paragraph_format.space_after) or 0
        self.first_line_indent = self._find(style, lambda style: style.paragraph_format.first_line_indent) or 0
        self.line_spacing = self._find(style, lambda style: style.paragraph_format.line_spacing) or self.font_size
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
    different_first_page_header_footer: bool = attr.ib(default=True)
    page_height : Optional[int] = attr.ib(default=None)
    page_width: Optional[int] = attr.ib(default=None)
    top_margin: Optional[int] = attr.ib(default=None)
    bottom_margin: Optional[int] = attr.ib(default=None)
    left_margin: Optional[int] = attr.ib(default=None)
    right_margin: Optional[int] = attr.ib(default=None)
    header_distance: Optional[int] = attr.ib(default=None)
    footer_distance: Optional[int] = attr.ib(default=None)
    gutter: Optional[int] = attr.ib(default=None)
    styles: Optional[Dict[str, StyleParameters]] = attr.ib(default={})

    def load(
        self, path: str  # Path to file
    ) -> None:
        doc = Document(path)

        # Basic info we need can be found in the first (only) section
        first_section = doc.sections[0]
        self.comments = doc.core_properties.comments
        self.different_first_page_header_footer = bool(first_section.different_first_page_header_footer)
        self.page_height = first_section.page_height
        self.page_width = first_section.page_width
        self.top_margin = first_section.top_margin
        self.bottom_margin = first_section.bottom_margin
        self.left_margin = first_section.left_margin
        self.right_margin = first_section.right_margin
        self.header_distance = first_section.header_distance
        self.footer_distance = first_section.footer_distance
        self.gutter = first_section.gutter

        # Look up some info on the following styles:
        self.styles = {}
        for style in doc.styles:
            name = style.name
            if name in ["Normal", "Heading 1", "Heading 2", "Header", "Footer", "Separator", "First Paragraph"]:
                self.styles[name] = StyleParameters().init(style)