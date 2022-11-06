from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
import logging
from typing import Optional
import wx

from style_stripper.control.settings_control import ConfigSettings
from style_stripper.data.constants import CONSTANTS
from style_stripper.data.enums import PanelType, PaginationType
from style_stripper.data.original_docx import OriginalDocx

# Constants:
LOG = logging.getLogger(__name__)


@dataclass
class Book:
    config: ConfigSettings
    original_docx: Optional[OriginalDocx] = None
    backup_docx: Optional[OriginalDocx] = None
    file_version: int = 1

    current_panel: PanelType = PanelType.AUTHOR
    source_path: str = ""
    author: str = ""
    title: str = ""
    word_count: Optional[int] = None
    last_modified: Optional[datetime] = None

    _modified: bool = False

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
        self.backup_docx = deepcopy(self.original_docx)
        self.source_path = path
        self.modified()
        wx.GetApp().frame.refresh_contents()

    def reload(self):
        LOG.debug("Reloading .docx from backup")
        self.original_docx = deepcopy(self.backup_docx)

    def export(self, path: str):
        # Open a template file to format the output
        template = wx.GetApp().template
        template.set_properties(self.author, self.title)

        # Dump paragraphs into the template
        for paragraph in self.original_docx.paragraphs:
            # May need to insert breaks before the headings
            if paragraph.style in [
                CONSTANTS.STYLING.NAMES.HEADING1,
                CONSTANTS.STYLING.NAMES.HEADING2,
            ]:
                if (
                    self.config.headings.break_before_heading
                    != PaginationType.CONTINUOUS
                ):
                    if self.config.headings.header_footer_after_break:
                        template.add_page_break()
                    else:
                        # template.add_content()
                        template.add_content()
                        template.add_section(
                            CONSTANTS.HEADINGS.BREAK_MAP[
                                self.config.headings.break_before_heading
                            ]
                        )

            template.add_content(paragraph.text, paragraph.style)

        # Save the resulting file
        template.save_as(path)
