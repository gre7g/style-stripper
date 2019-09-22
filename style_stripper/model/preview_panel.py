from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import logging
import os
import re
from typing import List, Tuple, Union
import wx

from style_stripper.data.constants import CONSTANTS
from style_stripper.data.enums import *
from style_stripper.data.template_details import TemplateParameters

try:
    from style_stripper.model.main_app import StyleStripperApp
except ImportError:
    StyleStripperApp = None

# Constants:
SEARCH_VARIANT = re.compile(r"&\d+")
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation
WORDS_TYPE = List[Tuple[str, int]]  # Each word is a string and the width in twips
LINE_TYPE = Tuple[int, WORDS_TYPE, int]  # Indent, words, additional spacing to justify

class PreviewPanel(wx.Panel):
    app: StyleStripperApp
    parameters: TemplateParameters
    lorem_ipsum: List[str]

    def __init__(self, parent):
        super(PreviewPanel, self).__init__(parent)
        self.app = wx.GetApp()
        self.parameters = self.open_to = self.scopes = self.hf_variant = self.scale = self.x_orig = self.y_orig = None
        self.scope_radius = self.measure_to_twips = None
        self.color_db = wx.ColourDatabase()

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)

        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "lorem_ipsum.txt")
        with open(path, "rt") as file_obj:
            self.lorem_ipsum = file_obj.readlines()

    def set_parameters(self, parameters: TemplateParameters):
        self.parameters = parameters
        match = SEARCH_VARIANT.search(parameters.comments)
        self.hf_variant = int(match.group()) if match else 1
        self.Refresh()

    def find_page_scaling(self):
        scope_radius = CONSTANTS.UI.PREVIEW.SCOPE_RADIUS

        # Loop over the scopes and find what will be the edges of the content
        measure_from_top = CONSTANTS.UI.PREVIEW.GAP + CONSTANTS.UI.PREVIEW.RULER_THICKNESS + CONSTANTS.UI.PREVIEW.GAP
        measure_from_bottom = 1.0 - CONSTANTS.UI.PREVIEW.GAP
        measure_from_left = CONSTANTS.UI.PREVIEW.RULER_THICKNESS + CONSTANTS.UI.PREVIEW.GAP
        measure_from_right = 1.0 - CONSTANTS.UI.PREVIEW.GAP
        top_point = 0
        bottom_point = self.parameters.page_height
        left_point = 0
        right_point = (self.parameters.page_width * 2) + CONSTANTS.UI.PREVIEW.PAGE_GAP
        if (SCOPE_ON_EVEN_HEADER in self.scopes) or (SCOPE_ON_ODD_HEADER in self.scopes):
            measure_from_top = CONSTANTS.UI.PREVIEW.GAP + CONSTANTS.UI.PREVIEW.RULER_THICKNESS + \
                CONSTANTS.UI.PREVIEW.GAP + scope_radius
            top_point = self.parameters.header_distance + \
                (self.parameters.styles[CONSTANTS.STYLING.NAMES.HEADER].font_size // 2)
        if (SCOPE_ON_EVEN_FOOTER in self.scopes) or (SCOPE_ON_ODD_FOOTER in self.scopes):
            measure_from_bottom = 1.0 - CONSTANTS.UI.PREVIEW.GAP - scope_radius
            bottom_point = self.parameters.page_height - self.parameters.footer_distance -\
                (self.parameters.styles[CONSTANTS.STYLING.NAMES.FOOTER].font_size // 2)
        if SCOPE_ON_LEFT_MARGIN in self.scopes:
            measure_from_left = CONSTANTS.UI.PREVIEW.RULER_THICKNESS + CONSTANTS.UI.PREVIEW.GAP + scope_radius
            left_point = self.parameters.left_margin
        if SCOPE_ON_RIGHT_MARGIN in self.scopes:
            measure_from_right = 1.0 - CONSTANTS.UI.PREVIEW.GAP - scope_radius
            right_point = (self.parameters.page_width * 2) + CONSTANTS.UI.PREVIEW.PAGE_GAP - \
                self.parameters.right_margin
        LOG.debug("measure_from_top=%r measure_from_bottom=%r measure_from_left=%r measure_from_right=%r top_point=%r "
                  "bottom_point=%r left_point=%r right_point=%r", measure_from_top, measure_from_bottom,
                  measure_from_left, measure_from_right, top_point, bottom_point, left_point, right_point)
        height = (bottom_point - top_point) / (measure_from_bottom - measure_from_top)
        width = (right_point - left_point) / (measure_from_right - measure_from_left)
        LOG.debug("height=%r width=%r", height, width)

        # We need to scale according to image height or image width, depending on which will use the space more
        # efficiently. Determine that now.
        size = self.GetSize()
        LOG.debug("panel height=%r width=%r", size.height, size.width)
        panel_hw_ratio = size.height / size.width
        content_hw_ratio = height / width
        LOG.debug("content_hw_ratio=%r panel_hw_ratio=%r", content_hw_ratio, panel_hw_ratio)
        if content_hw_ratio > panel_hw_ratio:
            # Content taller than panel
            self.scale = size.height / height
            self.measure_to_twips = size.height / self.scale
            if SCOPE_ON_LEFT_MARGIN in self.scopes:
                left_point -= scope_radius * self.measure_to_twips
            if SCOPE_ON_RIGHT_MARGIN in self.scopes:
                right_point += scope_radius * self.measure_to_twips
            blank_space = (size.width / self.scale) - (right_point - left_point)
            self.x_orig = left_point - (blank_space // 2)
            self.y_orig = top_point - (measure_from_top * self.measure_to_twips)
            self.scope_radius = CONSTANTS.UI.PREVIEW.SCOPE_RADIUS * self.measure_to_twips
            LOG.debug("taller scale=%r radius=%r", self.scale, self.scope_radius)
        else:
            # Content wider than panel
            self.scale = size.width / width
            self.measure_to_twips = size.width / self.scale
            if (SCOPE_ON_EVEN_HEADER in self.scopes) or (SCOPE_ON_ODD_HEADER in self.scopes):
                top_point -= scope_radius * self.measure_to_twips
            if (SCOPE_ON_EVEN_FOOTER in self.scopes) or (SCOPE_ON_ODD_FOOTER in self.scopes):
                bottom_point += scope_radius * self.measure_to_twips
            blank_space = (size.height / self.scale) - (bottom_point - top_point)
            self.x_orig = left_point - (measure_from_left * self.measure_to_twips)
            self.y_orig = top_point - (blank_space // 2)
            self.scope_radius = CONSTANTS.UI.PREVIEW.SCOPE_RADIUS * self.measure_to_twips
            LOG.debug("wider scale=%r radius=%r", self.scale, self.scope_radius)

    def set_contents(self, open_to: Enums, scopes: List[Enums]):
        self.open_to, self.scopes = open_to, scopes
        self.Refresh()

    def on_size(self, event: wx.PaintEvent):
        self.find_page_scaling()
        self.Refresh()
        event.Skip()

    def on_paint(self, event: wx.PaintEvent):
        dc = wx.BufferedPaintDC(self)
        gcdc = wx.GCDC(dc)
        gcdc.SetBackground(wx.Brush(self.app.frame.background_color))
        gcdc.Clear()
        gcdc.SetLogicalOrigin(self.x_orig, self.y_orig)
        gcdc.SetLogicalScale(self.scale, self.scale)

        # Draw white bar for vertical ruler
        white = self.color_db.Find("WHITE")
        gcdc.SetBrush(wx.Brush(white))
        gcdc.SetPen(wx.Pen(white))
        thickness = CONSTANTS.UI.PREVIEW.RULER_THICKNESS * self.measure_to_twips
        gcdc.DrawRectangle(self.x_orig, 0, thickness, self.parameters.page_height)

        font_size = thickness // 2
        gcdc.SetFont(wx.Font(font_size, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        # Label the vertical ruler
        gcdc.SetPen(wx.Pen(self.color_db.Find("BLACK")))
        for index, y in enumerate(range(0, int(self.parameters.page_height), CONSTANTS.MEASURING.TWIPS_PER_INCH)):
            label = str(index)
            size = gcdc.GetTextExtent(label)
            gcdc.DrawRotatedText(
                label,
                self.x_orig + ((thickness - font_size) * CONSTANTS.UI.PREVIEW.RULER_TEXT),
                y + (size.width // 2), 90
            )

        # Draw ticks at the half-inch spots along the horizontal ruler
        half_inch = CONSTANTS.MEASURING.TWIPS_PER_INCH // 2
        for index, y in enumerate(range(half_inch, int(self.parameters.page_height),
                                        CONSTANTS.MEASURING.TWIPS_PER_INCH)):
            gcdc.DrawLine(
                self.x_orig + (thickness * CONSTANTS.UI.PREVIEW.TICK_FROM), y,
                self.x_orig + (thickness * CONSTANTS.UI.PREVIEW.TICK_TO), y
            )

        # Draw blank pages and horizontal rulers
        self.draw_page(gcdc, 0)
        self.draw_page(gcdc, self.parameters.page_width + CONSTANTS.UI.PREVIEW.PAGE_GAP)

        # Draw text on pages
        if self.open_to == OPEN_TO_PART:
            lines = self.gather_back_lines_to(gcdc, CONSTANTS.UI.PREVIEW.TEXT_TO_OPPOSITE_PART)
            self.draw_in_style(gcdc, 0, self.parameters.top_margin, CONSTANTS.STYLING.NAMES.NORMAL, lines)
            y_offset = self.draw_in_style(gcdc, self.parameters.page_width + CONSTANTS.UI.PREVIEW.GAP + self.parameters.gutter, self.parameters.top_margin, CONSTANTS.STYLING.NAMES.HEADING1, _("Part II"))
            # lines, para_index, word_index = self.gather_forward_lines_from(gcdc, 0, 0, y_offset, CONSTANTS.STYLING.NAMES.FIRST_PARAGRAPH)
            # self.draw_in_style(gcdc, self.parameters.page_width + CONSTANTS.UI.PREVIEW.GAP, y_offset, CONSTANTS.STYLING.NAMES.FIRST_PARAGRAPH, lines)
        elif self.open_to == OPEN_TO_CHAPTER:
            lines = self.gather_back_lines_to(gcdc, CONSTANTS.UI.PREVIEW.TEXT_TO_OPPOSITE_CHAPTER)
            self.draw_in_style(gcdc, 0, self.parameters.top_margin, CONSTANTS.STYLING.NAMES.NORMAL, lines)
            y_offset = self.draw_in_style(gcdc, self.parameters.page_width + CONSTANTS.UI.PREVIEW.GAP, 0, CONSTANTS.STYLING.NAMES.HEADING1, (0, _("Chapter 7: Loren Ipsum"), 0))
            lines, para_index, word_index = self.gather_forward_lines_from(gcdc, 0, 0, y_offset, CONSTANTS.STYLING.NAMES.FIRST_PARAGRAPH)
            self.draw_in_style(gcdc, self.parameters.page_width + CONSTANTS.UI.PREVIEW.GAP, y_offset, CONSTANTS.STYLING.NAMES.FIRST_PARAGRAPH, lines)
        elif self.open_to == OPEN_TO_MID_CHAPTER:
            lines, para_index, word_index = self.gather_forward_lines_from(gcdc, 0, 0, 0, CONSTANTS.STYLING.NAMES.FIRST_PARAGRAPH)
            self.draw_in_style(gcdc, self.parameters.page_width + CONSTANTS.UI.PREVIEW.GAP, y_offset, CONSTANTS.STYLING.NAMES.FIRST_PARAGRAPH, lines)

        gcdc.DrawCircle(self.parameters.page_width / 2, self.parameters.header_distance +
            (self.parameters.styles[CONSTANTS.STYLING.NAMES.HEADER].font_size / 2), self.scope_radius)

    def draw_in_style(
        self, gcdc: wx.GCDC,  # Graphic context
        x_offset: int,  # X-offset of text page
        y_offset: int,  # Y-offset of first line
        style_name: str,  # "Normal" or "First Paragraph"
        lines: Union[str, List[LINE_TYPE]]  # Either a single string or a list of lines
    ) -> int:  # New Y-offset
        """Draw lines of text."""
        width_in_twips = (self.parameters.page_width - self.parameters.left_margin - self.parameters.right_margin -
                          self.parameters.gutter)

        style = self.parameters.styles[style_name]
        italic = wx.FONTSTYLE_ITALIC if style.italic else wx.FONTSTYLE_NORMAL
        bold = wx.FONTWEIGHT_BOLD if style.bold else wx.FONTWEIGHT_NORMAL
        font = wx.Font(style.font_size, wx.FONTFAMILY_DEFAULT, italic, bold, faceName=style.font)
        gcdc.SetFont(font)

        size = gcdc.GetTextExtent(" ")
        width_of_space = size.width
        if isinstance(lines, str):
            size = gcdc.GetTextExtent(lines)
            lines = [(style.first_line_indent, [(lines, size.width)], 0)]

        for indent, words, spacing in lines:
            # Technically this resets us back to Normal after each line instead of each paragraph. This isn't ideal but
            # I'm not certain I care enough to track the end of paragraphs.
            style_name = CONSTANTS.STYLING.NAMES.NORMAL

            total_width = sum(width for word, width in words)

            x = self.parameters.left_margin + indent
            if style.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER:
                x += (width_in_twips - total_width) // 2
            elif style.alignment == WD_PARAGRAPH_ALIGNMENT.RIGHT:
                x += width_in_twips - total_width
            for word, width in words:
                gcdc.DrawText(word, x_offset + x, y_offset)
                if style.alignment == WD_PARAGRAPH_ALIGNMENT.JUSTIFY:
                    x += width + spacing
                else:
                    x += width + width_of_space
            y_offset += style.line_spacing

        return y_offset

    def gather_back_lines_to(
            self, gcdc: wx.GCDC,  # Graphic context
            length_of_text: float  # How much text to generate (0.0=None, 1.0=Full page)
    ) -> List[Tuple[int, List[Tuple[str, int]], int]]:  # Each tuple is indent amount, list of words, space between each
        """Starting at the end of the lorem ipsum, gather lines to fill a percentage of a page."""
        width_in_twips = (self.parameters.page_width - self.parameters.left_margin - self.parameters.right_margin -
                          self.parameters.gutter)
        normal = self.parameters.styles[CONSTANTS.STYLING.NAMES.NORMAL]
        italic = wx.FONTSTYLE_ITALIC if normal.italic else wx.FONTSTYLE_NORMAL
        bold = wx.FONTWEIGHT_BOLD if normal.bold else wx.FONTWEIGHT_NORMAL
        gcdc.SetFont(wx.Font(normal.font_size, wx.FONTFAMILY_DEFAULT, italic, bold, faceName=normal.font))
        size = gcdc.GetTextExtent(" ")
        width_of_space = size.width
        line_index = -1
        lines = []
        y = self.parameters.top_margin
        while True:
            line = self.lorem_ipsum[line_index].split(" ")
            word_and_widths = []
            for word in line:
                size = gcdc.GetTextExtent(word)
                word_and_widths.append((word, size.width))
            line_index -= 1
            paragraph = []
            indent = self.parameters.styles[CONSTANTS.STYLING.NAMES.NORMAL].first_line_indent
            line_start = 0
            line_end = 1
            current_line = None
            while line_end < len(word_and_widths):
                line_width = indent + sum(width for word, width in word_and_widths[line_start:line_end]) + \
                    (width_of_space * (line_end - line_start - 1))
                if line_width > width_in_twips:
                    words, total_width = current_line
                    paragraph.append(
                        (indent, words, width_of_space + (width_in_twips - total_width) / (len(words) - 1))
                    )
                    line_start = line_end
                    word, width = word_and_widths[line_start]
                    current_line = ([(word, width)], width)
                    indent = 0
                else:
                    current_line = (word_and_widths[line_start:line_end], line_width)
                line_end += 1
            paragraph.append((indent, current_line[0], width_of_space))
            while paragraph:
                lines.insert(0, paragraph.pop())
                y += normal.line_spacing
                if (y / self.parameters.page_height) >= length_of_text:
                    return lines

    def draw_page(self, gcdc: wx.GCDC, x_offset: int):
        # White bar for horizontal ruler
        thickness = CONSTANTS.UI.PREVIEW.RULER_THICKNESS * self.measure_to_twips
        gap = CONSTANTS.UI.PREVIEW.GAP * self.measure_to_twips
        gcdc.SetPen(wx.Pen(self.color_db.Find("WHITE")))
        gcdc.DrawRectangle(x_offset, self.y_orig + gap, self.parameters.page_width, thickness)

        # White box for page
        gcdc.SetPen(wx.Pen(self.color_db.Find("BLACK")))
        gcdc.DrawRectangle(x_offset, 0, self.parameters.page_width, self.parameters.page_height)

        font_size = thickness // 2
        gcdc.SetFont(wx.Font(font_size, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        # Label the horizontal ruler
        for index, x in enumerate(range(0, int(self.parameters.page_width), CONSTANTS.MEASURING.TWIPS_PER_INCH)):
            label = str(index)
            size = gcdc.GetTextExtent(label)
            gcdc.DrawText(
                label,
                x_offset + x - (size.width // 2),
                self.y_orig + gap + ((thickness - font_size) * CONSTANTS.UI.PREVIEW.RULER_TEXT)
            )

        # Draw ticks at the half-inch spots along the horizontal ruler
        half_inch = CONSTANTS.MEASURING.TWIPS_PER_INCH // 2
        for index, x in enumerate(range(half_inch, int(self.parameters.page_width),
                                        CONSTANTS.MEASURING.TWIPS_PER_INCH)):
            gcdc.DrawLine(
                x_offset + x, self.y_orig + gap + (thickness * CONSTANTS.UI.PREVIEW.TICK_FROM),
                x_offset + x, self.y_orig + gap + (thickness * CONSTANTS.UI.PREVIEW.TICK_TO)
            )
