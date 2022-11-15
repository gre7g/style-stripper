from typing import overload
import wx
import wx.html

class HtmlWindow(wx.Scrolled, wx.html.HtmlWindowInterface):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(
        self,
        parent=wx.Window,
        id: wx.WindowID = ...,
        pos: wx.Point = ...,
        size: wx.Size = ...,
        style: long = ...,
        name: str = ...,
    ) -> None: ...
