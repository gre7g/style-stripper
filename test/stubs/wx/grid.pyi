from six import text_type as unicode
from typing import Optional, Type, Union
from types import TracebackType
import wx

Text = Union[unicode, str]

class Grid(wx.ScrolledWindow):
    def BeginBatch(self) -> None: ...
    def EndBatch(self) -> None: ...
    def SetColLabelValue(
        self,
        col: int,
        label: Text,
    ) -> None: ...

class GridCellEditor(wx.ClientDataContainer, wx.RefCounter):
    pass

class GridCellRenderer(wx.ClientDataContainer, wx.RefCounter):
    pass

class GridUpdateLocker(object):
    def __init__(
        self,
        grid: Optional[Grid] = ...,
    ) -> None: ...
    def __enter__(self) -> GridUpdateLocker: ...
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[Exception],
        exc_tb: Optional[TracebackType],
    ) -> bool: ...
