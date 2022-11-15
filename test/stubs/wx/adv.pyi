import six
from six import text_type as unicode
from typing import overload, Union
import wx

Text = Union[unicode, str]

if not six.PY2:
    long = int

DP_DROPDOWN: long = ...
DP_SHOWCENTURY: long = ...
EVT_CALENDAR_SEL_CHANGED: wx.PyEventBinder = ...
EVT_DATE_CHANGED: wx.PyEventBinder = ...

class CalendarCtrl(wx.Control):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(
        self,
        parent: wx.Window,
        id: wx.WindowID = ...,
        date: wx.DateTime = ...,
        pos: wx.Point = ...,
        size: wx.Size = ...,
        name: Text = ...,
    ) -> None: ...
    def GetDate(self) -> wx.DateTime: ...
    def SetDate(
        self,
        date: wx.DateTime,
    ) -> None: ...

class DateEvent(wx.CommandEvent):
    pass

class CalendarEvent(DateEvent):
    pass

class DatePickerCtrl(wx.Control):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(
        self,
        parent: wx.Window,
        id: wx.WindowID = ...,
        dt: wx.DateTime = ...,
        pos: wx.Point = ...,
        size: wx.Size = ...,
        style: long = ...,
        validator: wx.Validator = ...,
        name: Text = ...,
    ) -> None: ...
    def GetValue(self) -> wx.DateTime: ...
    def SetValue(
        self,
        dt: wx.DateTime,
    ) -> None: ...
