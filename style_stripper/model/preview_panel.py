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


class PreviewPanel(wx.Panel):
    app: StyleStripperApp
    parameters: TemplateParameters

    def __init__(self, parent):
        super(PreviewPanel, self).__init__(parent)
        self.app = wx.GetApp()
        self.parameters = self.open_to = self.scopes = self.hf_variant = None

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

        # We need to scale according to image height or image width, depending on which will use the space more
        # efficiently. Determine that now.
        size = self.GetSize()
        panel_hw_ratio = size.height / size.width
        # content_hw_ratio =

    def set_contents(self, open_to: Enums, scopes: List[Enums]):
        self.open_to, self.scopes = open_to, scopes
        self.Refresh()

    def on_paint(self, event: wx.PaintEvent):
        dc = wx.BufferedPaintDC(self)
        gcdc = wx.GCDC(dc)
        gcdc.SetBackground(wx.Brush(self.app.frame.background_color))
        gcdc.Clear()
        db = wx.ColourDatabase()
        gcdc.SetPen(wx.Pen(db.Find("BLACK")))
        gcdc.DrawRectangle(10, 10, 200, 200)
        matrix = wx.AffineMatrix2D()
        matrix.Scale(1.1, 1.0)
        gcdc.SetTransformMatrix(matrix)
        gcdc.SetPen(wx.Pen(db.Find("RED")))
        gcdc.DrawRectangle(10, 10, 200, 200)
