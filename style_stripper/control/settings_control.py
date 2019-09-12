import logging
import pickle
import wx

# Constants:
LOG = logging.getLogger(__name__)


class Settings(object):
    file_path = None
    window_rect = None
    maximized = False

    def __init__(self):
        self.file_version = 1

    def init(self):
        return self


class SettingsControl(object):
    def __init__(self, app):
        self.app = app
        self._save_maximized = True

    def load_settings(self):
        config_pickle = wx.FileConfig("StyleStripper").Read("configuration", "")
        self.app.settings = pickle.loads(bytes(config_pickle, "ascii")) if config_pickle else Settings()
        self.app.settings = self.app.settings.init()

    def save_settings_on_exit(self, event):
        self.app.book.not_modified()

        maximized = self.app.frame.IsMaximized()
        if self._save_maximized:
            self.app.settings.maximized = maximized
            self._save_maximized = False

        if maximized:
            self.app.frame.Maximize(False)
            wx.CallLater(100, self.save_settings_on_exit2, True)
        else:
            event.Skip()
            self.save_settings_on_exit2(False)

    def save_settings_on_exit2(self, close_frame):
        self.app.settings.window_rect = self.app.frame.GetRect()
        wx.FileConfig("StyleStripper").Write("configuration", pickle.dumps(self.app.settings, 0))
        if close_frame:
            self.app.frame.Close()
