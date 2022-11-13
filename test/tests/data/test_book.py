from mock_wx import wxTestCase, note_func

import logging
import pickle
from unittest.mock import call, patch, Mock
import wx

from style_stripper.control.settings_control import ConfigSettings
from style_stripper.data import book
from style_stripper.data.enums import PaginationType
from style_stripper.data.paragraph import Paragraph

# Constants:
LOG = logging.getLogger(__name__)


class TestBook(wxTestCase):
    def setUp(self) -> None:
        self.app = wx.App()
        self.window = book.Book(ConfigSettings())

    def test_upgrade(self):
        """Should upgrade old version to the latest"""
        latest_version = 1
        ver1_pickle = (
            b"\x80\x04\x95J\x04\x00\x00\x00\x00\x00\x00\x8c\x18style_stripper.data.book\x94\x8c\x04Book\x94\x93\x94)"
            b"\x81\x94}\x94(\x8c\x06config\x94\x8c'style_stripper.control.settings_control\x94\x8c\x0eConfigSettings"
            b"\x94\x93\x94)\x81\x94}\x94(\x8c\x06spaces\x94h\x06\x8c\x0cSpacesConfig\x94\x93\x94)\x81\x94}\x94(\x8c\x0c"
            b"purge_double\x94\x88\x8c\rpurge_leading\x94\x88\x8c\x0epurge_trailing\x94\x88ub\x8c\x06italic\x94h\x06"
            b"\x8c\x0cItalicConfig\x94\x93\x94)\x81\x94}\x94\x8c\x1dadjust_to_include_punctuation\x94\x88sb\x8c\x06quot"
            b"es\x94h\x06\x8c\x0cQuotesConfig\x94\x93\x94)\x81\x94}\x94\x8c\x10convert_to_curly\x94\x88sb\x8c\x07divide"
            b"r\x94h\x06\x8c\rDividerConfig\x94\x93\x94)\x81\x94}\x94(\x8c\x1bblank_paragraph_if_no_other\x94\x88\x8c"
            b"\x10replace_with_new\x94\x88\x8c\x03new\x94\x8c\x05# # #\x94ub\x8c\x08ellipses\x94h\x06\x8c\x0eEllipsesCo"
            b"nfig\x94\x93\x94)\x81\x94}\x94(h%\x88h&\x8c\x0f\xe2\x80\x8a.\xe2\x80\x8a.\xe2\x80\x8a.\xe2\x80\x8a\x94ub"
            b"\x8c\x08headings\x94h\x06\x8c\x0eHeadingsConfig\x94\x93\x94)\x81\x94}\x94(\x8c\x17style_parts_and_chapter"
            b"\x94\x88\x8c\rstyle_the_end\x94\x88\x8c\x0badd_the_end\x94\x88\x8c\x07the_end\x94\x8c\x07The End\x94\x8c"
            b"\x19header_footer_after_break\x94\x89\x8c\x14break_before_heading\x94\x8c\x19style_stripper.data.enums"
            b"\x94\x8c\x0ePaginationType\x94\x93\x94K\x05\x85\x94R\x94ub\x8c\x06dashes\x94h\x06\x8c\x0cDashesConfig\x94"
            b"\x93\x94)\x81\x94}\x94(\x8c\x0econvert_double\x94\x88\x8c\x12convert_to_en_dash\x94\x89\x8c\x12convert_to"
            b"_em_dash\x94\x88\x8c\x13fix_at_end_of_quote\x94\x88\x8c\x12force_all_en_or_em\x94\x88ub\x8c\x07styling"
            b"\x94h\x06\x8c\rStylingConfig\x94\x93\x94)\x81\x94}\x94\x8c\x16indent_first_paragraph\x94\x89sbub\x8c\rori"
            b"ginal_docx\x94N\x8c\x0bbackup_docx\x94N\x8c\x0cfile_version\x94K\x01\x8c\rcurrent_panel\x94h:\x8c\tPanelT"
            b"ype\x94\x93\x94K\x01\x85\x94R\x94\x8c\x0bsource_path\x94\x8c\x00\x94\x8c\x06author\x94hX\x8c\x05title\x94"
            b"hX\x8c\nword_count\x94N\x8c\rlast_modified\x94N\x8c\t_modified\x94\x89ub."
        )
        upgraded = pickle.loads(ver1_pickle).init()
        assert upgraded.file_version == latest_version
        # Add more tests to catch what has been set in upgrade

    @note_func("is_loaded")
    @note_func("is_modified")
    @note_func("not_modified")
    @note_func("modified")
    def test_loaded_modified(self):
        """Should handle loaded and modified flags"""
        book = self.window
        mock = self.app._the_mock

        LOG.info("Not loaded")
        book.is_loaded()
        expect = [call.is_loaded(), call.is_loaded_return_value(False)]

        LOG.info("Loaded")
        book.original_docx = "a document!"
        book.is_loaded()
        expect += [call.is_loaded(), call.is_loaded_return_value(True)]

        LOG.info("Not modified")
        book.is_modified()
        expect += [call.is_modified(), call.is_modified_return_value(False)]

        LOG.info("Modified")
        book.modified()
        book.is_modified()
        expect += [
            call.modified(),
            call.App.frame.show_title(),
            call.is_modified(),
            call.is_modified_return_value(True),
        ]

        LOG.info("Not modified")
        book.not_modified()
        book.is_modified()
        expect += [
            call.not_modified(),
            call.App.frame.show_title(),
            call.is_modified(),
            call.is_modified_return_value(False),
        ]

        mock.assert_has_calls(expect)

    @patch("style_stripper.data.book.OriginalDocx")
    @note_func("load")
    @note_func("modified")
    def test_load(self, OriginalDocx):
        """Should load a docx"""
        the_book = self.window
        mock = self.app._the_mock
        book.OriginalDocx = mock.OriginalDocx
        mock.OriginalDocx.return_value = "original docx"
        the_book.load("/path/to/docx")
        mock.backup_docx(the_book.backup_docx)
        mock.source_path(the_book.source_path)
        expect = [
            call.load("/path/to/docx"),
            call.OriginalDocx("/path/to/docx", the_book),
            call.modified(),
            call.App.frame.show_title(),
            call.App.refresh_contents(),
            call.backup_docx("original docx"),
            call.source_path("/path/to/docx"),
        ]

        mock.assert_has_calls(expect)

    def test_reload(self):
        book = self.window
        book.backup_docx = "backup"
        book.reload()
        assert book.original_docx == "backup"

    @note_func("export")
    def test_export(self):
        """Should export a docx"""
        book = self.window
        mock = self.app._the_mock
        book.original_docx = Mock()
        book.original_docx.paragraphs = [
            Paragraph("line 1", "Normal"),
            Paragraph("header text", "Heading 2"),
            Paragraph("line 2", "Normal"),
        ]
        book.author = "Author Name"
        book.title = "Book Title"

        LOG.info("Continuous")
        book.config.headings.break_before_heading = PaginationType.CONTINUOUS
        book.export("/path/to/docx")
        expect = [
            call.export("/path/to/docx"),
            call.App.template.set_properties("Author Name", "Book Title"),
            call.App.template.add_content("line 1", "Normal"),
            call.App.template.add_content("header text", "Heading 2"),
            call.App.template.add_content("line 2", "Normal"),
            call.App.template.save_as("/path/to/docx"),
        ]

        LOG.info("Header/footer after break")
        book.config.headings.break_before_heading = PaginationType.ODD_PAGE
        book.config.headings.header_footer_after_break = True
        book.export("/path/to/docx")
        expect += [
            call.export("/path/to/docx"),
            call.App.template.set_properties("Author Name", "Book Title"),
            call.App.template.add_content("line 1", "Normal"),
            call.App.template.add_page_break(),
            call.App.template.add_content("header text", "Heading 2"),
            call.App.template.add_content("line 2", "Normal"),
            call.App.template.save_as("/path/to/docx"),
        ]

        LOG.info("No header/footer after break")
        book.config.headings.header_footer_after_break = False
        book.export("/path/to/docx")
        expect += [
            call.export("/path/to/docx"),
            call.App.template.set_properties("Author Name", "Book Title"),
            call.App.template.add_content("line 1", "Normal"),
            call.App.template.add_content(),
            call.App.template.add_section(4),
            call.App.template.add_content("header text", "Heading 2"),
            call.App.template.add_content("line 2", "Normal"),
            call.App.template.save_as("/path/to/docx"),
        ]

        mock.assert_has_calls(expect)
