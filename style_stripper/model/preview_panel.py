import logging
import re
from typing import Any, Dict, List
import wx

from style_stripper.data.constants import CONSTANTS
from style_stripper.data.enums import *
from style_stripper.data.template_details import TemplateParameters

try:
    from style_stripper.model.main_app import StyleStripperApp
except ImportError:
    StyleStripperApp = None

# Constants:
SEARCH_VARIANT = re.compile("&\d+")
LOG = logging.getLogger(__name__)


class PreviewPanel(wx.Panel):
    app: StyleStripperApp
    parameters: TemplateParameters

    def __init__(self, parent):
        super(PreviewPanel, self).__init__(parent)
        self.app = wx.GetApp()
        self.parameters = self.open_to = self.scopes = self.hf_variant = self.scale = self.x_orig = self.y_orig = None
        self.scope_radius = None

        self.Bind(wx.EVT_PAINT, self.on_paint)

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
        right_point = self.parameters.page_width
        for scope in self.scopes:
            if scope in [SCOPE_ON_EVEN_HEADER, SCOPE_ON_ODD_HEADER]:
                measure_from_top = CONSTANTS.UI.PREVIEW.GAP + CONSTANTS.UI.PREVIEW.RULER_THICKNESS + \
                    CONSTANTS.UI.PREVIEW.GAP + scope_radius
                top_point = self.parameters.header_distance + (self.parameters.styles["Header"].font_size // 2)
            elif scope in [SCOPE_ON_EVEN_FOOTER, SCOPE_ON_ODD_FOOTER]:
                measure_from_bottom = 1.0 - CONSTANTS.UI.PREVIEW.GAP - scope_radius
                bottom_point = self.parameters.page_height - self.parameters.footer_distance -\
                    (self.parameters.styles["Footer"].font_size // 2)
            elif scope == SCOPE_ON_LEFT_MARGIN:
                measure_from_left = CONSTANTS.UI.PREVIEW.RULER_THICKNESS + CONSTANTS.UI.PREVIEW.GAP + scope_radius
                left_point = self.parameters.left_margin
            elif scope == SCOPE_ON_RIGHT_MARGIN:
                measure_from_right = 1.0 - CONSTANTS.UI.PREVIEW.GAP - scope_radius
                right_point = self.parameters.page_width - self.parameters.right_margin
        LOG.debug("measure_from_top=%r measure_from_bottom=%r measure_from_left=%r measure_from_right=%r top_point=%r "
                  "bottom_point=%r left_point=%r right_point=%r", measure_from_top, measure_from_bottom,
                  measure_from_left, measure_from_right, top_point, bottom_point, left_point, right_point)
        height_in_emu = (bottom_point - top_point) / (measure_from_bottom - measure_from_top)
        width_in_emu = (right_point - left_point) / (measure_from_right - measure_from_left)
        LOG.debug("height_in_emu=%r width_in_emu=%r", height_in_emu, width_in_emu)

        # We need to scale according to image height or image width, depending on which will use the space more
        # efficiently. Determine that now.
        size = self.GetSize()
        LOG.debug("panel height=%r width=%r", size.height, size.width)
        panel_hw_ratio = size.height / size.width
        content_hw_ratio = height_in_emu / width_in_emu
        if content_hw_ratio > panel_hw_ratio:
            # Content taller than panel
            self.scale = size.height / height_in_emu
            panel_w_in_emu = size.width / self.scale
            self.x_orig = -(panel_w_in_emu - width_in_emu) / 2
            self.y_orig = -((CONSTANTS.UI.PREVIEW.GAP + CONSTANTS.UI.PREVIEW.RULER_THICKNESS + CONSTANTS.UI.PREVIEW.GAP + CONSTANTS.UI.PREVIEW.SCOPE_RADIUS) * size.height / self.scale) + self.parameters.header_distance + (self.parameters.styles["Header"].font_size / 2)
            self.scope_radius = CONSTANTS.UI.PREVIEW.SCOPE_RADIUS * size.height / self.scale
            LOG.debug("taller scale=%r radius=%r", self.scale, self.scope_radius)
        else:
            # Content wider than panel
            self.scale = size.width / width_in_emu
            panel_h_in_emu = size.height / self.scale
            self.x_orig = (measure_from_left / self.scale) - left_point
            self.y_orig = -(panel_h_in_emu - height_in_emu) / 2
            self.scope_radius = CONSTANTS.UI.PREVIEW.SCOPE_RADIUS * size.width / self.scale
            LOG.debug("wider scale=%r radius=%r", self.scale, self.scope_radius)

    def set_contents(self, open_to: Enums, scopes: List[Enums]):
        self.open_to, self.scopes = open_to, scopes
        self.Refresh()

    def on_paint(self, event: wx.PaintEvent):
        dc = wx.BufferedPaintDC(self)
        gcdc = wx.GCDC(dc)
        gcdc.SetBackground(wx.Brush(self.app.frame.background_color))
        gcdc.Clear()
        db = wx.ColourDatabase()
        gcdc.SetLogicalOrigin(self.x_orig, self.y_orig)
        gcdc.SetLogicalScale(self.scale, self.scale)
        gcdc.SetPen(wx.Pen(db.Find("BLACK")))
        gcdc.DrawRectangle(0, 0, self.parameters.page_width, self.parameters.page_height)
        gcdc.DrawCircle(self.parameters.page_width / 2, self.parameters.header_distance + (self.parameters.styles["Header"].font_size / 2), self.scope_radius)
