from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import logging
from math import sin, cos
import os
from typing import List, Tuple, Union, Optional
import wx

from style_stripper.data.constants import CONSTANTS
from style_stripper.data.enums import *

try:
    from style_stripper.model.main_app import StyleStripperApp
except ImportError:
    StyleStripperApp = None

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation
WORDS_TYPE = List[Tuple[str, int]]  # Each word is a string and the width in twips
LINE_TYPE = Tuple[Enums, int, WORDS_TYPE, int]  # First/last, indent, words, additional spacing to justify


class PreviewPanel(wx.Panel):
    app: StyleStripperApp
    lorem_ipsum: List[str]

    def __init__(self, parent):
        super(PreviewPanel, self).__init__(parent)
        self.app = wx.GetApp()
        self.open_to = self.scopes = self.scale = self.x_orig = self.y_orig = self.scope_radius = None
        self.measure_to_twips = None
        self.color_db = wx.ColourDatabase()
        self.initialized = False

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)

        path = os.path.join(self.app.base_dir, "data", "lorem_ipsum.txt")
        with open(path, "rt") as file_obj:
            self.lorem_ipsum = file_obj.readlines()

    def find_page_scaling(self):
        scope_radius = CONSTANTS.UI.PREVIEW.SCOPE_RADIUS

        # Loop over the scopes and find what will be the edges of the content
        template = self.app.template
        measure_from_top = CONSTANTS.UI.PREVIEW.GAP + CONSTANTS.UI.PREVIEW.RULER_THICKNESS + CONSTANTS.UI.PREVIEW.GAP
        measure_from_bottom = 1.0 - CONSTANTS.UI.PREVIEW.GAP
        measure_from_left = CONSTANTS.UI.PREVIEW.RULER_THICKNESS + CONSTANTS.UI.PREVIEW.GAP
        measure_from_right = 1.0 - CONSTANTS.UI.PREVIEW.GAP
        top_point = 0
        bottom_point = template.page_height
        left_point = 0
        right_point = (template.page_width * 2) + CONSTANTS.UI.PREVIEW.PAGE_GAP
        if (SCOPE_ON_EVEN_HEADER in self.scopes) or (SCOPE_ON_ODD_HEADER in self.scopes):
            measure_from_top = CONSTANTS.UI.PREVIEW.GAP + CONSTANTS.UI.PREVIEW.RULER_THICKNESS + \
                CONSTANTS.UI.PREVIEW.GAP + scope_radius
            top_point = template.header_distance + \
                (template.styles[CONSTANTS.STYLING.NAMES.HEADER].font_size // 2)
        if (SCOPE_ON_EVEN_FOOTER in self.scopes) or (SCOPE_ON_ODD_FOOTER in self.scopes):
            measure_from_bottom = 1.0 - CONSTANTS.UI.PREVIEW.GAP - scope_radius
            bottom_point = template.page_height - template.footer_distance -\
                (template.styles[CONSTANTS.STYLING.NAMES.FOOTER].font_size // 2)
        if SCOPE_ON_LEFT_MARGIN in self.scopes:
            measure_from_left = CONSTANTS.UI.PREVIEW.RULER_THICKNESS + CONSTANTS.UI.PREVIEW.GAP + scope_radius
            left_point = template.left_margin
        if SCOPE_ON_RIGHT_MARGIN in self.scopes:
            measure_from_right = 1.0 - CONSTANTS.UI.PREVIEW.GAP - scope_radius
            right_point = (template.page_width * 2) + CONSTANTS.UI.PREVIEW.PAGE_GAP - \
                template.right_margin
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
        self.initialized = True
        self.open_to, self.scopes = open_to, scopes
        self.find_page_scaling()
        self.Refresh()

    def on_size(self, event: wx.PaintEvent):
        if self.initialized:
            self.find_page_scaling()
            self.Refresh()
        event.Skip()

    def on_paint(self, event: wx.PaintEvent):
        template = self.app.template
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
        gcdc.DrawRectangle(self.x_orig, 0, thickness, template.page_height)

        font_size = thickness // 2
        gcdc.SetFont(wx.Font(font_size, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        # Label the vertical ruler
        gcdc.SetPen(wx.Pen(self.color_db.Find("BLACK")))
        for index, y in enumerate(range(0, int(template.page_height), CONSTANTS.MEASURING.TWIPS_PER_INCH)):
            label = str(index)
            size = gcdc.GetTextExtent(label)
            gcdc.DrawRotatedText(
                label,
                self.x_orig + ((thickness - font_size) * CONSTANTS.UI.PREVIEW.RULER_TEXT),
                y + (size.width // 2), 90
            )

        # Draw ticks at the half-inch spots along the horizontal ruler
        half_inch = CONSTANTS.MEASURING.TWIPS_PER_INCH // 2
        for index, y in enumerate(range(half_inch, int(template.page_height),
                                        CONSTANTS.MEASURING.TWIPS_PER_INCH)):
            gcdc.DrawLine(
                self.x_orig + (thickness * CONSTANTS.UI.PREVIEW.TICK_FROM), y,
                self.x_orig + (thickness * CONSTANTS.UI.PREVIEW.TICK_TO), y
            )

        # Draw horizontal rulers
        self.draw_horizontal_ruler(gcdc, 0)
        self.draw_horizontal_ruler(gcdc, template.page_width + CONSTANTS.UI.PREVIEW.PAGE_GAP)

        self.draw_content(gcdc, self.color_db.Find("BLACK"), self.color_db.Find("LIGHT GREY"))
        self.draw_scopes(gcdc)

    def draw_content(self, gcdc: wx.GCDC, black: wx.Colour, grey: wx.Colour):
        template = self.app.template

        # Draw blank pages
        self.draw_page(gcdc, 0, black, grey)
        self.draw_page(gcdc, template.page_width + CONSTANTS.UI.PREVIEW.PAGE_GAP, black, grey)

        # Draw text on pages
        even_page = template.page_width + CONSTANTS.UI.PREVIEW.PAGE_GAP + template.gutter
        if self.open_to == OPEN_TO_PART:
            lines = self.gather_back_lines_to(gcdc, CONSTANTS.UI.PREVIEW.TEXT_TO_OPPOSITE_PART)
            self.draw_in_style(gcdc, 0, template.top_margin, CONSTANTS.STYLING.NAMES.NORMAL, lines, black)
            self.draw_in_style(gcdc, even_page, template.top_margin, CONSTANTS.STYLING.NAMES.HEADING1, _("Part II"), black)
        elif self.open_to == OPEN_TO_CHAPTER:
            lines = self.gather_back_lines_to(gcdc, CONSTANTS.UI.PREVIEW.TEXT_TO_OPPOSITE_CHAPTER)
            self.draw_in_style(gcdc, 0, template.top_margin, CONSTANTS.STYLING.NAMES.NORMAL, lines, black)
            y_offset = self.draw_in_style(gcdc, template.page_width + CONSTANTS.UI.PREVIEW.PAGE_GAP + template.left_margin, template.top_margin, CONSTANTS.STYLING.NAMES.HEADING2, _("Chapter 7: Lorem"), black)
            lines, para_index, word_index = self.gather_forward_lines_from(gcdc, 0, y_offset, CONSTANTS.STYLING.NAMES.FIRST_PARAGRAPH)
            self.draw_in_style(gcdc, template.page_width + CONSTANTS.UI.PREVIEW.PAGE_GAP + template.left_margin, y_offset, CONSTANTS.STYLING.NAMES.FIRST_PARAGRAPH, lines, black)
        elif self.open_to == OPEN_TO_MID_CHAPTER:
            lines, para_index, word_index = self.gather_forward_lines_from(gcdc, 0, template.top_margin, CONSTANTS.STYLING.NAMES.FIRST_PARAGRAPH)
            self.draw_in_style(gcdc, 0, template.top_margin, CONSTANTS.STYLING.NAMES.FIRST_PARAGRAPH, lines, black)
            lines, para_index, word_index = self.gather_forward_lines_from(gcdc, para_index, template.top_margin, CONSTANTS.STYLING.NAMES.FIRST_PARAGRAPH)
            self.draw_in_style(gcdc, template.page_width + CONSTANTS.UI.PREVIEW.PAGE_GAP + template.left_margin, template.top_margin, CONSTANTS.STYLING.NAMES.FIRST_PARAGRAPH, lines, black)

        if True:  # template.head_foot_variant == 1:
            header = template.header_distance
            self.draw_in_style(gcdc, 0, header, CONSTANTS.STYLING.NAMES.HEADER, _("Author’s Name"), black,
                               align=WD_PARAGRAPH_ALIGNMENT.CENTER)
            if self.open_to == OPEN_TO_MID_CHAPTER:
                self.draw_in_style(gcdc, even_page, header, CONSTANTS.STYLING.NAMES.HEADER, _("Book Title"), black,
                                   align=WD_PARAGRAPH_ALIGNMENT.CENTER)
            footer = template.page_height - template.footer_distance
            font_size = template.styles[CONSTANTS.STYLING.NAMES.FOOTER].font_size
            self.draw_in_style(gcdc, 0, footer - font_size, CONSTANTS.STYLING.NAMES.FOOTER, _("126"), black,
                               align=WD_PARAGRAPH_ALIGNMENT.LEFT)
            if self.open_to == OPEN_TO_MID_CHAPTER:
                self.draw_in_style(gcdc, even_page, footer - font_size, CONSTANTS.STYLING.NAMES.FOOTER, _("127"), black,
                                   align=WD_PARAGRAPH_ALIGNMENT.RIGHT)

    def draw_scope(self, gcdc: wx.GCDC, x: int, y: int, lines: List[str]):
        magnification = CONSTANTS.UI.PREVIEW.MAGNIFIER_SCALING
        points = [(x-self.x_orig+cos(a*6.283/15)*self.scope_radius, y-self.y_orig+sin(a*6.283/15)*self.scope_radius) for a in range(15)]
        region = wx.Region(points)
        gcdc.SetDeviceClippingRegion(region)
        gcdc.SetLogicalOrigin(x - ((x - self.x_orig) / magnification), y - ((y - self.y_orig) / magnification))
        gcdc.SetLogicalScale(self.scale * magnification, self.scale * magnification)
        self.draw_content(gcdc, wx.Colour(*CONSTANTS.UI.PREVIEW.MEDIUM_GREY), wx.Colour(*CONSTANTS.UI.PREVIEW.LIGHT_GREY))
        gcdc.DestroyClippingRegion()
        gcdc.SetLogicalOrigin(self.x_orig, self.y_orig)
        gcdc.SetLogicalScale(self.scale, self.scale)
        gcdc.SetBrush(wx.NullBrush)
        black = self.color_db.Find("BLACK")
        gcdc.SetPen(wx.Pen(black))
        gcdc.SetTextForeground(black)
        gcdc.DrawCircle(x, y, self.scope_radius)
        font_size = 0.02 * self.measure_to_twips
        gcdc.SetFont(wx.Font(font_size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        line_spacing = font_size * CONSTANTS.UI.PREVIEW.LINE_SPACING
        height = font_size + (line_spacing * (len(lines) - 1))
        y_pos = y - (height // 2)
        for text in lines:
            size = gcdc.GetTextExtent(text)
            gcdc.DrawText(text, x - (size.width // 2), y_pos)
            y_pos += line_spacing

    def draw_scopes(self, gcdc: wx.GCDC):
        template = self.app.template
        mid_offset = CONSTANTS.UI.PREVIEW.MID_TEXT_OFFSET
        width_in_twips = (template.page_width - template.left_margin - template.right_margin -
                          template.gutter)
        left_centered = template.left_margin + (width_in_twips // 2)
        right_centered = left_centered + template.page_width + CONSTANTS.UI.PREVIEW.PAGE_GAP + template.gutter
        mid_vertical = template.page_height // 2
        style = template.styles[CONSTANTS.STYLING.NAMES.HEADING1]
        part = template.top_margin + style.space_before + (style.font_size * mid_offset)
        style = template.styles[CONSTANTS.STYLING.NAMES.HEADING2]
        chapter = template.top_margin + style.space_before + (style.font_size * mid_offset)
        header = template.header_distance
        font_size = template.styles[CONSTANTS.STYLING.NAMES.HEADER].font_size
        even_header = (left_centered, header + (font_size * mid_offset))
        odd_header = (right_centered, header + (font_size * mid_offset))
        font_size = template.styles[CONSTANTS.STYLING.NAMES.FOOTER].font_size
        footer = template.page_height - template.footer_distance
        even_footer = (template.left_margin, footer - (font_size * (1 - mid_offset)))
        even_page = (template.page_width * 2) + CONSTANTS.UI.PREVIEW.PAGE_GAP - template.right_margin
        odd_footer = (even_page, footer - (font_size * (1 - mid_offset)))

        gcdc.SetBrush(wx.Brush(self.color_db.Find("WHITE")))
        style = template.styles[CONSTANTS.STYLING.NAMES.HEADER]
        height = _("Header height: %s") % template.header_imperial
        margin = _("Top margin: %s") % template.top_imperial
        if SCOPE_ON_EVEN_HEADER in self.scopes:
            self.draw_scope(gcdc, even_header[0], even_header[1], [style.font_text, height, "", "", margin, ""])
        if SCOPE_ON_ODD_HEADER in self.scopes:
            self.draw_scope(gcdc, odd_header[0], odd_header[1], [style.font_text, height, "", "", margin, ""])
        style = template.styles[CONSTANTS.STYLING.NAMES.FOOTER]
        height = _("Footer height: %s") % template.footer_imperial
        if SCOPE_ON_EVEN_FOOTER in self.scopes:
            margin = _("Left margin: %s") % template.left_imperial
            self.draw_scope(gcdc, even_footer[0], even_footer[1], [style.font_text, height, "", "", margin, ""])
        if SCOPE_ON_ODD_FOOTER in self.scopes:
            self.draw_scope(gcdc, odd_footer[0], odd_footer[1], [style.font_text, "", "", height])
        if SCOPE_ON_LEFT_MARGIN in self.scopes:
            self.draw_scope(gcdc, template.left_margin, mid_vertical, [])
        if SCOPE_ON_RIGHT_MARGIN in self.scopes:
            self.draw_scope(gcdc, (template.page_width * 2) + CONSTANTS.UI.PREVIEW.PAGE_GAP - template.right_margin,
                            mid_vertical, [])
        if SCOPE_ON_GUTTER in self.scopes:
            margin = _("Right margin: %s") % template.right_imperial
            gutter = _("Gutter: %s") % template.gutter_imperial
            self.draw_scope(gcdc, template.page_width - template.gutter, mid_vertical, [margin, gutter])
        if SCOPE_ON_PART in self.scopes:
            style = template.styles[CONSTANTS.STYLING.NAMES.HEADING1]
            above = "Space above: %s" % style.before_text
            self.draw_scope(gcdc, right_centered, part, [above, "", "", "", "", style.font_text])
        if SCOPE_ON_CHAPTER in self.scopes:
            style = template.styles[CONSTANTS.STYLING.NAMES.HEADING2 if template.part_and_chapter else CONSTANTS.STYLING.NAMES.HEADING1]
            above = "Space above: %s" % style.before_text
            below = "Space below: %s" % style.after_text
            self.draw_scope(gcdc, right_centered, chapter, [style.font_text, above, "", "", "", below, ""])

    def draw_in_style(
        self, gcdc: wx.GCDC,  # Graphic context
        x_offset: int,  # X-offset of text page
        y_offset: int,  # Y-offset of first line
        style_name: str,  # "Normal" or "First Paragraph"
        lines: Union[str, List[LINE_TYPE]],  # Either a single string or a list of lines
        black: wx.Colour,
        align: Optional[int] = None,  # Alignment override
    ) -> int:  # New Y-offset
        template = self.app.template

        """Draw lines of text."""
        width_in_twips = (template.page_width - template.left_margin - template.right_margin -
                          template.gutter)

        style = template.styles[style_name]
        italic = wx.FONTSTYLE_ITALIC if style.italic else wx.FONTSTYLE_NORMAL
        bold = wx.FONTWEIGHT_BOLD if style.bold else wx.FONTWEIGHT_NORMAL
        font = wx.Font(style.font_size, wx.FONTFAMILY_DEFAULT, italic, bold, faceName=style.font)
        gcdc.SetTextForeground(black)
        gcdc.SetFont(font)

        size = gcdc.GetTextExtent(" ")
        width_of_space = size.width
        if isinstance(lines, str):
            size = gcdc.GetTextExtent(lines)
            lines = [(ONLY_LINE, style.first_line_indent, [(lines, size.width)], 0)]

        for descriptor, indent, words, spacing in lines:
            # Technically this resets us back to Normal after each line instead of each paragraph. This isn't ideal but
            # I'm not certain I care enough to track the end of paragraphs.
            style_name = CONSTANTS.STYLING.NAMES.NORMAL

            total_width = sum(width for word, width in words)

            if descriptor in [FIRST_LINE, ONLY_LINE]:
                y_offset += style.space_before

            x = template.left_margin + indent
            if align is None:
                align = style.alignment
            if align == WD_PARAGRAPH_ALIGNMENT.CENTER:
                x += (width_in_twips - total_width) // 2
            elif align == WD_PARAGRAPH_ALIGNMENT.RIGHT:
                x += width_in_twips - total_width
            for word, width in words:
                gcdc.DrawText(word, x_offset + x, y_offset)
                if align == WD_PARAGRAPH_ALIGNMENT.JUSTIFY:
                    x += width + spacing
                else:
                    x += width + width_of_space
            y_offset += style.line_spacing

            if descriptor in [LAST_LINE, ONLY_LINE]:
                y_offset += style.space_after

        return y_offset

    def gather_paragraph(self, gcdc: wx.GCDC, text: str, style: str, width_of_space: int, width_in_twips: int) -> list:
        line = text.split(" ")
        word_and_widths = []
        for word in line:
            size = gcdc.GetTextExtent(word)
            word_and_widths.append((word, size.width))
        paragraph = []
        indent = self.app.template.styles[style].first_line_indent
        line_start = 0
        line_end = 1
        current_line = None
        while True:
            line_width = indent + sum(width for word, width in word_and_widths[line_start:line_end]) + \
                         (width_of_space * (line_end - line_start - 1))
            if line_width > width_in_twips:
                words, total_width = current_line
                paragraph.append(
                    (MIDDLE_LINE, indent, words, width_of_space + (width_in_twips - total_width) / (len(words) - 1))
                )
                line_start = line_end - 1
                word, width = word_and_widths[line_start]
                current_line = ([(word, width)], width)
                indent = 0
            else:
                current_line = (word_and_widths[line_start:line_end], line_width)

            if line_end >= len(word_and_widths):
                break
            else:
                line_end += 1

        if paragraph:
            paragraph[0] = (FIRST_LINE,) + paragraph[0][1:]
            paragraph.append((LAST_LINE, indent, current_line[0], width_of_space))
        else:
            paragraph.append((ONLY_LINE, indent, current_line[0], width_of_space))

        return paragraph

    def gather_forward_lines_from(self, gcdc: wx.GCDC, line_index: int, y: int, style_name: str):
        template = self.app.template
        width_in_twips = (template.page_width - template.left_margin - template.right_margin -
                          template.gutter)
        style = template.styles[style_name]
        italic = wx.FONTSTYLE_ITALIC if style.italic else wx.FONTSTYLE_NORMAL
        bold = wx.FONTWEIGHT_BOLD if style.bold else wx.FONTWEIGHT_NORMAL
        gcdc.SetFont(wx.Font(style.font_size, wx.FONTFAMILY_DEFAULT, italic, bold, faceName=style.font))
        size = gcdc.GetTextExtent(" ")
        width_of_space = size.width
        lines = []
        while True:
            paragraph = self.gather_paragraph(gcdc, self.lorem_ipsum[line_index], style_name, width_of_space, width_in_twips)

            while paragraph:
                lines.append(paragraph.pop(0))
                y += style.line_spacing
                if y > (template.page_height - template.bottom_margin):
                    return lines, line_index, 0

            line_index += 1
            style_name = CONSTANTS.STYLING.NAMES.NORMAL

    def gather_back_lines_to(
            self, gcdc: wx.GCDC,  # Graphic context
            length_of_text: float  # How much text to generate (0.0=None, 1.0=Full page)
    ) -> List[LINE_TYPE]:  # List of line descriptors
        """Starting at the end of the lorem ipsum, gather lines to fill a percentage of a page."""
        template = self.app.template
        width_in_twips = (template.page_width - template.left_margin - template.right_margin -
                          template.gutter)
        normal = template.styles[CONSTANTS.STYLING.NAMES.NORMAL]
        italic = wx.FONTSTYLE_ITALIC if normal.italic else wx.FONTSTYLE_NORMAL
        bold = wx.FONTWEIGHT_BOLD if normal.bold else wx.FONTWEIGHT_NORMAL
        gcdc.SetFont(wx.Font(normal.font_size, wx.FONTFAMILY_DEFAULT, italic, bold, faceName=normal.font))
        size = gcdc.GetTextExtent(" ")
        width_of_space = size.width
        line_index = -1
        lines = []
        y = template.top_margin
        while True:
            paragraph = self.gather_paragraph(gcdc, self.lorem_ipsum[line_index], CONSTANTS.STYLING.NAMES.NORMAL, width_of_space, width_in_twips)

            while paragraph:
                lines.insert(0, paragraph.pop())
                y += normal.line_spacing
                if (y / template.page_height) >= length_of_text:
                    return lines

            line_index -= 1

    def draw_horizontal_ruler(self, gcdc: wx.GCDC, x_offset: int):
        template = self.app.template

        # White bar for horizontal ruler
        thickness = CONSTANTS.UI.PREVIEW.RULER_THICKNESS * self.measure_to_twips
        gap = CONSTANTS.UI.PREVIEW.GAP * self.measure_to_twips
        gcdc.SetPen(wx.Pen(self.color_db.Find("WHITE")))
        gcdc.DrawRectangle(x_offset, self.y_orig + gap, template.page_width, thickness)

        font_size = thickness // 2
        gcdc.SetFont(wx.Font(font_size, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        gcdc.SetPen(wx.Pen(self.color_db.Find("BLACK")))

        # Label the horizontal ruler
        for index, x in enumerate(range(0, int(template.page_width), CONSTANTS.MEASURING.TWIPS_PER_INCH)):
            label = str(index)
            size = gcdc.GetTextExtent(label)
            gcdc.DrawText(
                label,
                x_offset + x - (size.width // 2),
                self.y_orig + gap + ((thickness - font_size) * CONSTANTS.UI.PREVIEW.RULER_TEXT)
            )

        # Draw ticks at the half-inch spots along the horizontal ruler
        half_inch = CONSTANTS.MEASURING.TWIPS_PER_INCH // 2
        for index, x in enumerate(range(half_inch, int(template.page_width),
                                        CONSTANTS.MEASURING.TWIPS_PER_INCH)):
            gcdc.DrawLine(
                x_offset + x, self.y_orig + gap + (thickness * CONSTANTS.UI.PREVIEW.TICK_FROM),
                x_offset + x, self.y_orig + gap + (thickness * CONSTANTS.UI.PREVIEW.TICK_TO)
            )

    def draw_page(self, gcdc: wx.GCDC, x_offset: int, black: wx.Colour, grey: wx.Colour):
        template = self.app.template

        # White box for page
        gcdc.SetBrush(wx.Brush(self.color_db.Find("WHITE")))
        gcdc.SetPen(wx.Pen(black))
        gcdc.DrawRectangle(x_offset, 0, template.page_width, template.page_height)
        gcdc.SetBrush(wx.Brush(grey))
        gcdc.SetPen(wx.Pen(grey))
        if x_offset:
            gcdc.DrawRectangle(x_offset, 0, template.gutter, template.page_height)
        else:
            gcdc.DrawRectangle(template.page_width - template.gutter, 0,
                               template.gutter, template.page_height)
        gcdc.SetPen(wx.Pen(black))
        gcdc.SetBrush(wx.NullBrush)
        gcdc.DrawRectangle(x_offset, 0, template.page_width, template.page_height)
