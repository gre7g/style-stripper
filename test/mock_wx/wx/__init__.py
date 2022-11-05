from unittest.mock import Mock

from mock_wx.mock_wx_constants import *
from mock_wx.mock_wx_events import *

# Globals:
BLACK = None
BLUE = None
CYAN = None
CallAfter = None
CallLater = None
GREEN = None
G_THE_APP = None
GetTranslation = str
LIGHT_GREY = None
Locale = None
RED = None
WHITE = None
YELLOW = None


class BaseMockObj:
    def __init__(self, *args, **kwargs):
        name = self.__class__.__name__
        self._mock = getattr(G_THE_APP._the_mock, kwargs.get("name", name))
        self._mock(*args, **kwargs)
        self._the_mock = G_THE_APP._the_mock

        # Cheap way to track the last instantiated object of each type
        getattr(self._the_mock, self.__class__.__name__).return_value = self

        if name in G_THE_APP._patches_wx:
            patches = G_THE_APP._patches_wx[name]
            index = 0
            while index < len(patches):
                patch = patches[index]
                if isinstance(patch, str):
                    self._apply_patch_wx(patch)
                    index += 1
                else:
                    self._apply_patch_wx(patch.pop(0))
                    if patch:
                        index += 1
                    else:
                        del patches[index]

            if not patches:
                del G_THE_APP._patches_wx[name]

    def _apply_patch_wx(self, patch):
        exec("x._mock" + patch, {"x": self})

    @classmethod
    def _patch(cls, patch):
        name = cls.__name__
        patches = G_THE_APP._patches_wx.get(name, [])
        patches.append(patch)
        G_THE_APP._patches_wx[name] = patches

    def __getattr__(self, item):
        return getattr(self._mock, item)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.Destroy()
        return False


class App(BaseMockObj):
    def __init__(self, *args, **kwargs):
        global G_THE_APP, Locale, CallAfter, CallLater, TheClipboard, BLACK, BLUE, CYAN, GREEN, YELLOW, LIGHT_GREY
        global RED, WHITE

        G_THE_APP = self
        self._the_mock = Mock()
        self._patches_wx = {}
        Locale, CallAfter, CallLater = (
            self._the_mock.Locale,
            self._the_mock.CallAfter,
            self._the_mock.CallLater,
        )
        BLACK, BLUE, CYAN, GREEN = Colour(), Colour(), Colour(), Colour()
        YELLOW, LIGHT_GREY, RED, WHITE = Colour(), Colour(), Colour(), Colour()
        TheClipboard = self._the_mock.the_clipboard
        self.SetExitOnFrameDelete = self._the_mock.SetExitOnFrameDelete
        self.SetTopWindow = self._the_mock.SetTopWindow

        BaseMockObj.__init__(self, *args, **kwargs)

    @staticmethod
    def Get():
        return G_THE_APP


GetApp = App.Get


class Object(BaseMockObj):
    pass


class Event(Object):
    pass


class Window(BaseMockObj):
    pass


class ScrolledWindow(Window):
    pass


class Sizer(Object):
    pass


class Bitmap(Object):
    pass


class DC(Object):
    pass


class WindowDC(DC):
    pass


class ClientDC(WindowDC):
    pass


class PaintDC(ClientDC):
    pass


class BoxSizer(Sizer):
    pass


class Control(Window):
    pass


class AnyButton(Control):
    pass


class Button(AnyButton):
    pass


class CheckBox(Control):
    pass


class Clipboard(Object):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


class ItemContainerImmutable(BaseMockObj):
    pass


class ItemContainer(ItemContainerImmutable):
    pass


class Choice(Control, ItemContainer):
    pass


class CloseEvent(Event):
    pass


class Colour(Object):
    pass


Color = Colour


class CommandEvent(Event):
    pass


class DataObject(BaseMockObj):
    pass


class DataObjectSimple(DataObject):
    pass


class TextDataObject(DataObjectSimple):
    pass


class NonOwnedWindow(Window):
    pass


class TopLevelWindow(NonOwnedWindow):
    pass


class Dialog(TopLevelWindow):
    pass


class FileDialog(Dialog):
    pass


class GBSpan(BaseMockObj):
    pass


class GDIObject(Object):
    pass


class Font(GDIObject):
    pass


class Frame(TopLevelWindow):
    pass


class GridSizer(Sizer):
    pass


class FlexGridSizer(GridSizer):
    pass


class GridBagSizer(FlexGridSizer):
    pass


class KeyboardState(BaseMockObj):
    pass


class KeyEvent(Event, KeyboardState):
    pass


class ListCtrl(Control):
    pass


class NotifyEvent(CommandEvent):
    pass


class ListEvent(NotifyEvent):
    pass


class Trackable(BaseMockObj):
    pass


class EvtHandler(Object, Trackable):
    pass


class Menu(EvtHandler):
    pass


class MenuEvent(Event):
    pass


class MenuBar(Window):
    pass


class MenuItem(Object):
    pass


class MessageDialog(Dialog):
    pass


class MouseState(KeyboardState):
    pass


class MouseEvent(Event, MouseState):
    pass


class PaintEvent(Event):
    pass


class Panel(Window):
    pass


class Rect(BaseMockObj):
    pass


class Size(BaseMockObj):
    pass


class SizeEvent(Event):
    pass


class StandardPaths(BaseMockObj):
    @staticmethod
    def Get():
        return G_THE_APP._the_mock.standard_paths


class StaticBox(Control):
    pass


class StaticText(Control):
    pass


class StatusBar(Control):
    pass


class TextEntry(BaseMockObj):
    pass


class TextEntryDialog(Dialog):
    pass


class TextCtrl(Control, TextEntry):
    pass
