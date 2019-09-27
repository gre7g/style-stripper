import logging
import os
import wx

from style_stripper.data.constants import CONSTANTS
from style_stripper.model.author_panel import AuthorPanel
from style_stripper.model.template_panel import TemplatePanel
from style_stripper.model.options_panel import OptionsPanel
from style_stripper.model.review_panel import ReviewPanel

# Constants:
_ = wx.GetTranslation
LOG = logging.getLogger(__name__)


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        self.app = wx.GetApp()
        self.main_panel = self.file_history = self.statusbar = self.file_path_ctrl = self.author_ctrl = None
        self.title_ctrl = self.word_count_ctrl = self.modified_ctrl = self.background_color = None
        self.author_panel = self.template_panel = self.options_panel = self.review_panel = None
        self.panels = []
        wx.Frame.__init__(self, *args, **kwargs)

    def init(self):
        self.main_panel = wx.Panel(self)
        self.Bind(wx.EVT_CLOSE, self.app.frame_controls.on_close, self)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.VERTICAL)

        self.author_panel = AuthorPanel(self.main_panel)
        sizer2.Add(self.author_panel, 1, wx.EXPAND, 0)
        self.panels.append(self.author_panel)

        self.template_panel = TemplatePanel(self.main_panel)
        sizer2.Add(self.template_panel, 1, wx.EXPAND, 0)
        self.panels.append(self.template_panel)

        self.options_panel = OptionsPanel(self.main_panel)
        sizer2.Add(self.options_panel, 1, wx.EXPAND, 0)
        self.panels.append(self.options_panel)

        self.review_panel = ReviewPanel(self.main_panel)
        sizer2.Add(self.review_panel, 1, wx.EXPAND, 0)
        self.panels.append(self.review_panel)

        sizer1.Add(sizer2, 1, wx.EXPAND | wx.ALL, 10)

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
        self.main_panel.SetSizerAndFit(sizer1)
        self.SetMinSize(wx.Size(400, 300))
        if self.app.settings.window_rect:
            self.SetRect(self.app.settings.window_rect)
        if self.app.settings.maximized:
            self.Maximize()

        self.background_color = self.main_panel.GetBackgroundColour()

    def show_title(self):
        modified = "*" if self.app.book.is_modified() else ""
        if self.app.file_path:
            path, filename = os.path.split(self.app.file_path)
            title = "%s - %s%s" % (CONSTANTS.UI.APP_NAME, filename, modified)
        else:
            title = "%s%s" % (CONSTANTS.UI.APP_NAME, modified)
        self.SetTitle(title)

    def refresh_contents(self):
        current = self.app.book.current_page
        active_panel = None
        if current < 0:
            current = self.app.book.current_page = 0
        if current >= len(self.panels):
            current = self.app.book.current_page = len(self.panels) - 1
        for index, panel in enumerate(self.panels):
            if index == current:
                active_panel = panel
                panel.Show()
            else:
                panel.Hide()
        self.main_panel.Layout()
        active_panel.refresh_contents()

    def grab_contents(self):
        if self.app.initialized:
            panel = self.panels[self.app.book.current_page]
            panel.grab_contents()

    def refresh_file_history(self):
        self.file_history.AddFileToHistory(self.app.file_path)
        self.file_history.Save(wx.FileConfig(CONSTANTS.UI.CATEGORY_NAME))

    def book_loaded(self, is_loaded: bool = True):
        self.author_panel.book_loaded(is_loaded)

    def apply(self):
        self.review_panel.apply()
