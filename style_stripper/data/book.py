from copy import deepcopy
import logging
import wx

from style_stripper.data.original_docx import OriginalDocx

# Constants:
LOG = logging.getLogger(__name__)


class Book(object):
    original_docx: OriginalDocx
    backup_docx: OriginalDocx

    def __init__(self, config):
        self.file_version = 1
        self.original_docx = self.backup_docx = None
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
        self.backup_docx = deepcopy(self.original_docx)
        self.source_path = path
        self.modified()
        wx.GetApp().frame.refresh_contents()

    def reload(self):
        LOG.debug("Reloading .docx from backup")
        self.original_docx = deepcopy(self.backup_docx)

    def export(self, path: str):
        # Open a template file to format the output
        template = Template(CONSTANTS.PAGE.TEMPLATE)

        # Dump paragraphs into the template
        for paragraph in document.paragraphs:
            # May need to insert breaks before the headings
            if paragraph.style in [CONSTANTS.STYLING.NAMES.HEADING1, CONSTANTS.STYLING.NAMES.HEADING2]:
                if CONSTANTS.HEADINGS.BREAK_BEFORE_HEADING is not None:
                    if CONSTANTS.HEADINGS.HEADER_FOOTER_AFTER_BREAK:
                        template.add_page_break()
                    else:
                        # template.add_content()
                        template.add_content()
                        template.add_section(CONSTANTS.HEADINGS.BREAK_BEFORE_HEADING)

            template.add_content(paragraph.text, paragraph.style)

        # Save the resulting file
        template.save_as(r"..\temp.docx")
