import logging
import os
import wx

from style_stripper.data.constants import CONSTANTS
from style_stripper.data.enums import *
from style_stripper.model.author_panel import AuthorPanel

# Constants:
_ = wx.GetTranslation
LOG = logging.getLogger(__name__)


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        self.app = wx.GetApp()
        self.statusbar = self.panel = self.file_path_ctrl = self.author_ctrl = self.title_ctrl = None
        self.word_count_ctrl = self.modified_ctrl = self.file_history = None
        wx.Frame.__init__(self, *args, **kwargs)

    def init(self):
        panel = wx.Panel(self)
        self.Bind(wx.EVT_CLOSE, self.app.frame_controls.on_close, self)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.panel = AuthorPanel(panel)
        sizer1.Add(self.panel, 1, wx.EXPAND | wx.ALL, 10)

        self.file_history = wx.FileHistory(CONSTANTS.UI.MAX_FILE_HISTORY)
        self.file_history.Load(wx.FileConfig(CONSTANTS.UI.CATEGORY_NAME))
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        menu_bar.Append(file_menu, _("&File"))
        self.SetMenuBar(menu_bar)
        new_file = file_menu.Append(-1, _("&New...\tCtrl-N"), _("Create a new project"))
        open_file = file_menu.Append(-1, _("&Open...\tCtrl-O"), _("Open a new file"))

        recent = wx.Menu()
        self.file_history.UseMenu(recent)
        self.file_history.AddFilesToMenu()
        file_menu.Append(-1, _("&Recent Files"), recent)

        file_menu.AppendSeparator()
        save = file_menu.Append(-1, _("&Save\tCtrl-S"), _("Save the current file"))
        save_as = file_menu.Append(-1, _("Save &As..."), _("Save under a new filename"))
        file_menu.AppendSeparator()
        exit_cmd = file_menu.Append(-1, _("&Quit"), _("Exit application"))
        self.Bind(wx.EVT_MENU, self.app.menu_controls.on_new, new_file)
        self.Bind(wx.EVT_MENU, self.app.menu_controls.on_open, open_file)
        self.Bind(wx.EVT_MENU_RANGE, self.app.menu_controls.on_file_history, id=wx.ID_FILE1, id2=wx.ID_FILE9)
        self.Bind(wx.EVT_MENU, self.app.menu_controls.on_save, save)
        self.Bind(wx.EVT_MENU, self.app.menu_controls.on_save_as, save_as)
        self.Bind(wx.EVT_MENU, self.app.menu_controls.on_quit, exit_cmd)

        self.statusbar = self.CreateStatusBar()

        self.Show()
        panel.SetSizerAndFit(sizer1)
        self.SetMinSize(wx.Size(400, 300))
        if self.app.settings.window_rect:
            self.SetRect(self.app.settings.window_rect)
        if self.app.settings.maximized:
            self.Maximize()

    def show_title(self):
        modified = "*" if self.app.book.is_modified() else ""
        if self.app.file_path:
            path, filename = os.path.split(self.app.file_path)
            title = "%s - %s%s" % (CONSTANTS.UI.APP_NAME, filename, modified)
        else:
            title = "%s%s" % (CONSTANTS.UI.APP_NAME, modified)
        self.SetTitle(title)

    def refresh_contents(self):
        self.panel.refresh_contents()

    def refresh_file_history(self):
        self.file_history.AddFileToHistory(self.app.file_path)
        self.file_history.Save(wx.FileConfig(CONSTANTS.UI.CATEGORY_NAME))
