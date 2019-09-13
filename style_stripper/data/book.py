import wx


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
