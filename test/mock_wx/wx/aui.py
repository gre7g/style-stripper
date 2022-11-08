from wx import EvtHandler, Event

from mock_wx.event_binder import EventBinder
from mock_wx.wx.mock_wx_aui_constants import *


EVT_AUI_PANE_BUTTON = EventBinder(3000000)
EVT_AUI_PANE_CLOSE = EventBinder(3000001)
EVT_AUI_PANE_MAXIMIZE = EventBinder(3000002)
EVT_AUI_PANE_RESTORE = EventBinder(3000003)
EVT_AUI_PANE_ACTIVATED = EventBinder(3000004)
EVT_AUI_RENDER = EventBinder(3000005)
EVT_AUI_FIND_MANAGER = EventBinder(3000006)


class AuiManager(EvtHandler):
    pass


class AuiManagerEvent(Event):
    pass
