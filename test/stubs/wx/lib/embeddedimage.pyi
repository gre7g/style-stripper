import wx

class PyEmbeddedImage(object):
    def __init__(
        self,
        data: bytes,
        isBase64: bool = ...,
    ) -> None: ...
    def GetIcon(self) -> wx.Icon: ...
