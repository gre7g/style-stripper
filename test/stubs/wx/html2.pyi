from typing import overload
import wx

class WebView(wx.Control):
    @overload
    @staticmethod
    def New(backend: str = ...) -> "WebView": ...
    @overload
    @staticmethod
    def New(
        parent=wx.Window,
        id: wx.WindowID = ...,
        url: str = ...,
        pos: wx.Point = ...,
        size: wx.Size = ...,
        backend: str = ...,
        style: long = ...,
        name: str = ...,
    ) -> "WebView": ...
    def LoadURL(self, url: str = ...) -> None: ...
