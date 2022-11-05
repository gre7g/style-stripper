import wx

from mock_wx.event_binder import EventBinder

EVT_WEBVIEW_NAVIGATING = EventBinder(4000000)


class WebView(wx.Control):
    @staticmethod
    def New(*args, **kwargs):
        return wx.G_THE_APP.WebView.New(*args, **kwargs)


class WebViewEvent(wx.NotifyEvent):
    pass
