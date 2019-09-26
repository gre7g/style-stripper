import wx

from style_stripper.data.original_docx import OriginalDocx


class Book(object):
    def __init__(self, config):
        self.file_version = 1
        self.original_docx = None
        self.config = config

        self.current_page = 0
        self.source_path = ""
        self.author = ""
        self.title = ""
        self.word_count = None
        self.last_modified = None

        self._modified = False

    def init(self):
        return self

    def is_loaded(self):
        return self.original_docx is not None

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
        self.source_path = path
        self.modified()
        wx.GetApp().frame.refresh_contents()
