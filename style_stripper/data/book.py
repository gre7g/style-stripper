import wx

from style_stripper.data.enums import *
from style_stripper.data.original_docx import OriginalDocx


class Book(object):
    def __init__(self, config):
        self.file_version = 1
        self.original_docx = None
        self.config = config
        self._modified = False

    def init(self):
        return self

    def is_modified(self):
        return self._modified

    def not_modified(self):
        self._modified = False
        wx.GetApp().frame.show_title()

    def modified(self):
        self._modified = True
        wx.GetApp().frame.show_title()

    def load(self, path: str):
        self.original_docx = OriginalDocx(path, self)
        self.config[SOURCE][PATH] = path
        self.modified()
        wx.GetApp().frame.refresh_contents()
