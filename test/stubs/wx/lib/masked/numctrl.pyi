import builtins
from six import text_type as unicode
from typing import Any, Optional, overload, Tuple, Union
import wx

# from wx.lib.masked.textctrl import BaseMaskedTextCtrl
Text = Union[unicode, str]

if not hasattr(builtins, "long"):
    long = int

BaseMaskedNumCtrl = (
    wx.Control
)  # TODO FIXME: this really should be BaseMaskedTextCtrl but causes type issues with GetValue() and SetValue()

class NumCtrlAccessorsMixin(object):
    pass

class NumCtrl(BaseMaskedNumCtrl, NumCtrlAccessorsMixin):
    def __init__(
        self,
        parent: wx.Window,
        id: wx.WindowID = ...,
        value: Union[int, float] = ...,
        pos: wx.Point = ...,
        size: wx.Size = ...,
        style: long = ...,
        validator: wx.Validator = ...,
        name: Text = ...,
        **kwargs: Any,
    ) -> None: ...
    def ChangeValue(
        self,
        value: int,
    ) -> None: ...
    def GetBounds(self) -> Tuple[int, int]: ...
    def GetFractionWidth(self) -> int: ...
    def GetMax(self) -> int: ...
    def GetMin(self) -> int: ...
    def GetValue(self) -> float: ...
    def IsInBounds(
        self,
        value: Optional[int] = ...,
    ) -> bool: ...
    def SetBounds(
        self,
        min: Optional[int] = ...,
        max: Optional[int] = ...,
    ) -> None: ...
    def SetMax(
        self,
        max: Optional[int] = ...,
    ) -> None: ...
    def SetMin(
        self,
        min: Optional[int] = ...,
    ) -> None: ...
    def SetValue(
        self,
        value: Union[int, float],
    ) -> None: ...
