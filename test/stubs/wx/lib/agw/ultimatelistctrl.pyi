from six import text_type as unicode  # pip install six
from typing import Union
import wx

Text = Union[unicode, str]

class UltimateListCtrl(wx.Control):
    def __init__(
        self,
        parent: wx.Window,
        id: int = ...,
        pos: wx.Point = ...,
        size: wx.Size = ...,
        style: int = ...,
        agwStyle: int = ...,
        validator: wx.Validator = ...,
        name: Text = ...,
    ) -> None: ...
    def GetColumnCount(self) -> int: ...
    def InsertColumn(
        self,
        col: int,
        heading: Text,
        format: int = ...,
        width: int = ...,
    ) -> int: ...
    def RefreshItems(
        self,
        itemFrom: int,
        itemTo: int,
    ) -> None: ...
    def SetItemCount(self, count: int) -> None: ...
