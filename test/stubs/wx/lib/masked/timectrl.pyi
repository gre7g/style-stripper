import builtins
from six import text_type as unicode
from typing import Optional, overload, Union
import wx
from wx.lib.masked.textctrl import BaseMaskedTextCtrl

Text = Union[unicode, str]

if not hasattr(builtins, "long"):
    long = int

class TimeCtrl(BaseMaskedTextCtrl):
    def __init__(
        self,
        parent: wx.Window,
        id: wx.WindowID = ...,
        value: Text = ...,
        pos: wx.Point = ...,
        size: wx.Size = ...,
        style: long = ...,
        validator: wx.Validator = ...,
        name: Text = ...,
        format: Text = ...,
        fmt24hr: bool = ...,
        displaySeconds: bool = ...,
        spinButton: Optional[wx.SpinButton] = ...,
        min: Text = ...,  # TODO FIXME: is this right?
        max: Text = ...,  # TODO FIXME: is this right?
        limited: Optional[bool] = ...,
        oob_color: Text = ...,
    ) -> None: ...
    @overload
    def GetValue(self) -> Text: ...
    @overload
    def GetValue(self, as_wxDateTime: bool) -> wx.DateTime: ...
    @overload
    def GetValue(self, as_wxTimeSpan: bool) -> wx.TimeSpan: ...
    def SetValue(self, value: Union[Text, wx.DateTime, wx.TimeSpan]) -> None: ...
