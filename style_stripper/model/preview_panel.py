import re
from typing import Any, Dict, List
import wx

from style_stripper.data.constants import CONSTANTS
from style_stripper.data.enums import *

# Constants:
SEARCH_VARIANT = re.compile("&\d+")


class PreviewPanel(wx.Panel):
    def __init__(self, parent):
        super(PreviewPanel, self).__init__(parent)
        self.template_dict = self.open_to = self.scopes = self.hf_variant = None

        self.Bind(wx.EVT_PAINT, self.on_paint)

    def set_template_dict(self, template_dict: Dict[str, Any]):
        self.template_dict = template_dict
        match = SEARCH_VARIANT.search(template_dict["comments"])
        self.hf_variant = int(match.group()) if match else 1
        self.Refresh()

    def find_page_scaling(self):
        scope_radius = CONSTANTS.UI.PREVIEW.SCOPE_RADIUS
        top = TOP_EDGE
        bottom = BOTTOM_EDGE
        left = LEFT_EDGE
        right = RIGHT_EDGE
        for scope in self.scopes:
            if scope in [SCOPE_ON_EVEN_HEADER, SCOPE_ON_ODD_HEADER]:
                top = HEADER
            elif scope in [SCOPE_ON_EVEN_FOOTER, SCOPE_ON_ODD_FOOTER]:
                bottom = FOOTER
            elif scope == SCOPE_ON_LEFT_MARGIN:
                left = LEFT_MARGIN
            elif scope == SCOPE_ON_RIGHT_MARGIN:
                right == RIGHT_MARGIN
        if 

    def set_contents(self, open_to: Enums, scopes: List[Enums]):
        self.open_to, self.scopes = open_to, scopes
        self.Refresh()

    def on_paint(self, event: wx.PaintEvent):
        dc = wx.BufferedPaintDC(self)
        gcdc = wx.GCDC(dc)
        gcdc.Clear()
        # self.Draw(dc)
