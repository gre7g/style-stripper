import logging
import os
import wx

# Constants:
LOG = logging.getLogger(__name__)


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        self.app = wx.GetApp()
        self.statusbar = self.panel = self.file_path_ctrl = self.author_ctrl = self.title_ctrl = None
        self.word_count_ctrl = self.modified_ctrl = None
        wx.Frame.__init__(self, *args, **kwargs)

    def init(self):
        panel = wx.Panel(self)
        self.Bind(wx.EVT_CLOSE, self.app.frame_controls.on_close, self)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(panel)
        sizer1.Add(self.panel, 1, wx.EXPAND | wx.ALL, 10)
        sizer2 = wx.BoxSizer(wx.VERTICAL)
        sizer3 = wx.FlexGridSizer(2, 10, 5)
        sizer2.Add(sizer3, 1, wx.EXPAND, 0)
        sizer3.AddGrowableCol(1)
        text = wx.StaticText(self.panel, label="Source file:")
        sizer3.Add(text, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        self.file_path_ctrl = wx.TextCtrl(self.panel)
        sizer4.Add(self.file_path_ctrl, 1, wx.CENTER, 0)
        button = wx.Button(self.panel, label="Browse...")
        button.Bind(wx.EVT_BUTTON, self.app.frame_controls.on_browse)
        sizer4.Add(button, 0, wx.CENTER | wx.LEFT, 5)
        sizer3.Add(sizer4, 0, wx.CENTER | wx.EXPAND, 0)
        text = wx.StaticText(self.panel, label="Author:")
        sizer3.Add(text, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 0)
        self.author_ctrl = wx.TextCtrl(self.panel)
        self.author_ctrl.Bind(wx.EVT_TEXT, self.app.frame_controls.on_author)
        sizer3.Add(self.author_ctrl, 0, wx.CENTER | wx.EXPAND, 0)
        text = wx.StaticText(self.panel, label="Title:")
        sizer3.Add(text, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 0)
        self.title_ctrl = wx.TextCtrl(self.panel)
        self.title_ctrl.Bind(wx.EVT_TEXT, self.app.frame_controls.on_title)
        sizer3.Add(self.title_ctrl, 0, wx.CENTER | wx.EXPAND, 0)
        text = wx.StaticText(self.panel, label="Word count:")
        sizer3.Add(text, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 0)
        self.word_count_ctrl = wx.StaticText(self.panel)
        sizer3.Add(self.word_count_ctrl, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 0)
        text = wx.StaticText(self.panel, label="Last modified:")
        sizer3.Add(text, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 0)
        self.modified_ctrl = wx.StaticText(self.panel)
        sizer3.Add(self.modified_ctrl, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 0)
        button = wx.Button(self.panel, label="Next")
        button.Bind(wx.EVT_BUTTON, self.app.frame_controls.on_next)
        sizer2.Add(button, 0, wx.ALIGN_RIGHT | wx.TOP, 10)

        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        menu_bar.Append(file_menu, "&File")
        self.SetMenuBar(menu_bar)
        new_file = file_menu.Append(-1, "&New...\tCtrl-N", "Create a new project")
        open_file = file_menu.Append(-1, "&Open...\tCtrl-O", "Open a new file")
        file_menu.AppendSeparator()
        save = file_menu.Append(-1, "&Save\tCtrl-S", "Save the current file")
        save_as = file_menu.Append(-1, "Save &As...", "Save under a new filename")
        file_menu.AppendSeparator()
        exit_cmd = file_menu.Append(-1, "&Quit", "Exit application")
        self.Bind(wx.EVT_MENU, self.app.menu_controls.on_new, new_file)
        self.Bind(wx.EVT_MENU, self.app.menu_controls.on_open, open_file)
        self.Bind(wx.EVT_MENU, self.app.menu_controls.on_save, save)
        self.Bind(wx.EVT_MENU, self.app.menu_controls.on_save_as, save_as)
        self.Bind(wx.EVT_MENU, self.app.menu_controls.on_quit, exit_cmd)

        self.statusbar = self.CreateStatusBar()

        self.Show()
        self.panel.SetSizer(sizer2)
        panel.SetSizerAndFit(sizer1)
        self.SetMinSize(wx.Size(400, 300))
        if self.app.settings.window_rect:
            self.SetRect(self.app.settings.window_rect)
        if self.app.settings.maximized:
            self.Maximize()

    def show_title(self):
        modified = "*" if self.app.book.is_modified() else ""
        if self.app.settings.file_path:
            path, filename = os.path.split(self.app.settings.file_path)
            title = "Style Stripper - %s%s" % (filename, modified)
        else:
            title = "Style Stripper%s" % modified
        self.SetTitle(title)

    def refresh_contents(self):
        source = self.app.book.config["SOURCE"]
        self.file_path_ctrl.SetValue(source["PATH"])
        self.author_ctrl.SetValue(source["AUTHOR"])
        self.title_ctrl.SetValue(source["TITLE"])
        self.word_count_ctrl.SetLabel("" if source["WORD_COUNT"] is None else "{:n}".format(source["WORD_COUNT"]))

        modified = source["LAST_MODIFIED"]
        if modified is None:
            self.modified_ctrl.SetLabel("")
        else:
            dt_obj = wx.DateTime(modified.day, modified.month - 1, modified.year, modified.hour, modified.minute,
                                 modified.second)
            self.modified_ctrl.SetLabel("%s %s" % (dt_obj.FormatDate(), dt_obj.FormatTime()))
