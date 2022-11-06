import logging
import os
from typing import Dict
import wx

from style_stripper.data.constants import CONSTANTS
from style_stripper.data.enums import PanelType
from style_stripper.model.author_panel import AuthorPanel
from style_stripper.model.content_pane import ContentPanel
from style_stripper.model.template_panel import TemplatePanel
from style_stripper.model.options_panel import OptionsPanel
from style_stripper.model.review_panel import ReviewPanel
from style_stripper.model.done_panel import DonePanel

try:
    from style_stripper.model.main_app import StyleStripperApp
except ImportError:
    StyleStripperApp = None

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


class MainFrame(wx.Frame):
    app: StyleStripperApp
    author_panel: AuthorPanel
    template_panel: TemplatePanel
    options_panel: OptionsPanel
    review_panel: ReviewPanel
    done_panel: DonePanel
    file_history: wx.FileHistory
    status_bar: wx.StatusBar
    background_color: wx.Colour
    panels: Dict[PanelType, ContentPanel]

    def __init__(self, *args, **kwargs):
        self.app = wx.GetApp()
        wx.Frame.__init__(self, *args, **kwargs)

    def init(self):
        self.Bind(wx.EVT_CLOSE, self.app.frame_controls.on_close, self)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.VERTICAL)

        self.author_panel = AuthorPanel(self, name="author_panel")
        sizer2.Add(self.author_panel, 1, wx.EXPAND, 0)

        self.template_panel = TemplatePanel(self, name="template_panel")
        sizer2.Add(self.template_panel, 1, wx.EXPAND, 0)

        self.options_panel = OptionsPanel(self, name="options_panel")
        sizer2.Add(self.options_panel, 1, wx.EXPAND, 0)

        self.review_panel = ReviewPanel(self, "review_panel")
        sizer2.Add(self.review_panel, 1, wx.EXPAND, 0)

        self.done_panel = DonePanel(self, "done_panel")
        sizer2.Add(self.done_panel, 1, wx.EXPAND, 0)
        sizer1.Add(sizer2, 1, wx.EXPAND | wx.ALL, 10)

        self.panels = {
            PanelType.AUTHOR: self.author_panel,
            PanelType.TEMPLATE: self.template_panel,
            PanelType.OPTIONS: self.options_panel,
            PanelType.REVIEW: self.review_panel,
            PanelType.DONE: self.done_panel,
        }

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
        self.Bind(
            wx.EVT_MENU_RANGE,
            self.app.menu_controls.on_file_history,
            id=wx.ID_FILE1,
            id2=wx.ID_FILE9,
        )
        self.Bind(wx.EVT_MENU, self.app.menu_controls.on_save, save)
        self.Bind(wx.EVT_MENU, self.app.menu_controls.on_save_as, save_as)
        self.Bind(wx.EVT_MENU, self.app.menu_controls.on_quit, exit_cmd)

        self.status_bar = self.CreateStatusBar(name="status_bar")

        self.Show()
        self.SetSizerAndFit(sizer1)
        self.SetMinSize(wx.Size(400, 300))
        if self.app.settings.window_rect:
            self.SetRect(self.app.settings.window_rect)
        if self.app.settings.maximized:
            self.Maximize()

        self.background_color = self.GetBackgroundColour()

    def show_title(self):
        modified = "*" if self.app.book.is_modified() else ""
        if self.app.file_path:
            path, filename = os.path.split(self.app.file_path)
            title = f"{CONSTANTS.UI.APP_NAME} - {filename}{modified}"
        else:
            title = f"{CONSTANTS.UI.APP_NAME}{modified}"
        self.SetTitle(title)

    def refresh_file_history(self):
        """Move the active file to the top of the file history"""
        self.file_history.AddFileToHistory(self.app.file_path)
        self.file_history.Save(wx.FileConfig(CONSTANTS.UI.CATEGORY_NAME))
