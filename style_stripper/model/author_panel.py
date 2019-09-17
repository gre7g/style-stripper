import wx

try:
    from style_stripper.model.main_app import StyleStripperApp
except ImportError:
    StyleStripperApp = None

# Constants:
_ = wx.GetTranslation


class AuthorPanel(wx.Panel):
    app: StyleStripperApp

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.app = wx.GetApp()

        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.FlexGridSizer(2, 10, 5)
        sizer1.Add(sizer2, 1, wx.EXPAND, 0)
        sizer2.AddGrowableCol(1)
        text = wx.StaticText(self, label=_("Source file:"))
        sizer2.Add(text, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.file_path_ctrl = wx.StaticText(self)
        sizer3.Add(self.file_path_ctrl, 1, wx.CENTER, 0)
        button = wx.Button(self, label=_("Browse..."))
        button.Bind(wx.EVT_BUTTON, self.app.frame_controls.on_browse)
        sizer3.Add(button, 0, wx.CENTER | wx.LEFT, 5)
        sizer2.Add(sizer3, 0, wx.CENTER | wx.EXPAND, 0)
        text = wx.StaticText(self, label=_("Author:"))
        sizer2.Add(text, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 0)
        self.author_ctrl = wx.TextCtrl(self)
        self.author_ctrl.Bind(wx.EVT_TEXT, self.app.frame_controls.on_author)
        sizer2.Add(self.author_ctrl, 0, wx.CENTER | wx.EXPAND, 0)
        text = wx.StaticText(self, label=_("Title:"))
        sizer2.Add(text, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 0)
        self.title_ctrl = wx.TextCtrl(self)
        self.title_ctrl.Bind(wx.EVT_TEXT, self.app.frame_controls.on_title)
        sizer2.Add(self.title_ctrl, 0, wx.CENTER | wx.EXPAND, 0)
        text = wx.StaticText(self, label=_("Word count:"))
        sizer2.Add(text, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 0)
        self.word_count_ctrl = wx.StaticText(self)
        sizer2.Add(self.word_count_ctrl, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 0)
        text = wx.StaticText(self, label=_("Last modified:"))
        sizer2.Add(text, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 0)
        self.modified_ctrl = wx.StaticText(self)
        sizer2.Add(self.modified_ctrl, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 0)
        button = wx.Button(self, label=_("Next"))
        button.Bind(wx.EVT_BUTTON, self.app.frame_controls.on_next)
        sizer1.Add(button, 0, wx.ALIGN_RIGHT | wx.TOP, 10)
        self.SetSizer(sizer1)

    def refresh_contents(self):
        book = self.app.book
        self.file_path_ctrl.SetLabel(book.source_path)
        self.author_ctrl.SetValue(book.author)
        self.title_ctrl.SetValue(book.title)
        self.word_count_ctrl.SetLabel("" if book.word_count is None else "{:n}".format(book.word_count))

        modified = book.last_modified
        if modified is None:
            self.modified_ctrl.SetLabel("")
        else:
            dt_obj = wx.DateTime(modified.day, modified.month - 1, modified.year, modified.hour, modified.minute,
                                 modified.second)
            self.modified_ctrl.SetLabel("%s %s" % (dt_obj.FormatDate(), dt_obj.FormatTime()))
