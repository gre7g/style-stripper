from mock_wx import wxTestCase, note_func

from copy import deepcopy
import logging
from unittest.mock import call, patch
import wx

from style_stripper.data.enums import PaginationType
from style_stripper.control.settings_control import (
    Settings,
    ConfigSettings,
    SpacesConfig,
    ItalicConfig,
    QuotesConfig,
    DividerConfig,
    EllipsesConfig,
    HeadingsConfig,
    DashesConfig,
    StylingConfig,
)
from style_stripper.model import content_panel
from style_stripper.model import options_panel

# Constants:
LOG = logging.getLogger(__name__)


class TestOptionsPanel(wxTestCase):
    def setUp(self) -> None:
        self.app = wx.App()
        self.window = options_panel.OptionsPanel()
        self.window._the_mock = self.app._the_mock

    @patch("style_stripper.model.content_panel.ContentPanel.is_current_panel")
    @note_func("refresh_contents")
    def test_refresh_contents(self, is_current_panel):
        """Should update the panel contents"""
        panel = self.window
        mock = panel._the_mock
        content_panel.ContentPanel.refresh_contents = mock.base_refresh_contents

        LOG.info("Default config")
        self.app.settings = Settings()
        panel.refresh_contents()
        expect = [
            call.refresh_contents(),
            call.base_refresh_contents(),
            call.double.SetValue(True),
            call.leading.SetValue(True),
            call.trailing.SetValue(True),
            call.italic.SetValue(True),
            call.quotes.SetValue(True),
            call.blank.SetValue(True),
            call.replace_divider.SetValue(True),
            call.divider.Enable(True),
            call.divider.SetValue("# # #"),
            call.replace_ellipses.SetValue(True),
            call.ellipses1.Enable(True),
            call.ellipses1_text.Enable(True),
            call.ellipses2.Enable(True),
            call.ellipses2_text.Enable(True),
            call.ellipses3.Enable(True),
            call.ellipses3_text.Enable(True),
            call.ellipses4.Enable(True),
            call.ellipses4_text.Enable(True),
            call.ellipses3.SetValue(True),
            call.part_chapter.SetValue(True),
            call.style_end.SetValue(True),
            call.add_end.SetValue(True),
            call.end.Enable(True),
            call.end.SetValue("The End"),
            call.breaks.SetSelection(3),
            call.indent.SetValue(False),
            call.replace_dashes.SetValue(True),
            call.replace_hyphens.SetValue(True),
            call.hyphen_at_end.SetValue(True),
            call.em_dash.SetValue(True),
        ]

        LOG.info("..., new page (no head/foot), en dash")
        self.app.settings.latest_config.ellipses.new = "..."
        self.app.settings.latest_config.headings.break_before_heading = (
            PaginationType.NEW_PAGE
        )
        self.app.settings.latest_config.dashes.convert_to_en_dash = True
        self.app.settings.latest_config.dashes.convert_to_em_dash = False
        panel.refresh_contents()
        expect += [
            call.refresh_contents(),
            call.base_refresh_contents(),
            call.double.SetValue(True),
            call.leading.SetValue(True),
            call.trailing.SetValue(True),
            call.italic.SetValue(True),
            call.quotes.SetValue(True),
            call.blank.SetValue(True),
            call.replace_divider.SetValue(True),
            call.divider.Enable(True),
            call.divider.SetValue("# # #"),
            call.replace_ellipses.SetValue(True),
            call.ellipses1.Enable(True),
            call.ellipses1_text.Enable(True),
            call.ellipses2.Enable(True),
            call.ellipses2_text.Enable(True),
            call.ellipses3.Enable(True),
            call.ellipses3_text.Enable(True),
            call.ellipses4.Enable(True),
            call.ellipses4_text.Enable(True),
            call.ellipses1.SetValue(True),
            call.part_chapter.SetValue(True),
            call.style_end.SetValue(True),
            call.add_end.SetValue(True),
            call.end.Enable(True),
            call.end.SetValue("The End"),
            call.breaks.SetSelection(2),
            call.indent.SetValue(False),
            call.replace_dashes.SetValue(True),
            call.replace_hyphens.SetValue(True),
            call.hyphen_at_end.SetValue(True),
            call.en_dash.SetValue(True),
        ]

        LOG.info("…, even page")
        self.app.settings.latest_config.ellipses.new = "…"
        self.app.settings.latest_config.headings.break_before_heading = (
            PaginationType.EVEN_PAGE
        )
        panel.refresh_contents()
        expect += [
            call.refresh_contents(),
            call.base_refresh_contents(),
            call.double.SetValue(True),
            call.leading.SetValue(True),
            call.trailing.SetValue(True),
            call.italic.SetValue(True),
            call.quotes.SetValue(True),
            call.blank.SetValue(True),
            call.replace_divider.SetValue(True),
            call.divider.Enable(True),
            call.divider.SetValue("# # #"),
            call.replace_ellipses.SetValue(True),
            call.ellipses1.Enable(True),
            call.ellipses1_text.Enable(True),
            call.ellipses2.Enable(True),
            call.ellipses2_text.Enable(True),
            call.ellipses3.Enable(True),
            call.ellipses3_text.Enable(True),
            call.ellipses4.Enable(True),
            call.ellipses4_text.Enable(True),
            call.ellipses2.SetValue(True),
            call.part_chapter.SetValue(True),
            call.style_end.SetValue(True),
            call.add_end.SetValue(True),
            call.end.Enable(True),
            call.end.SetValue("The End"),
            call.breaks.SetSelection(4),
            call.indent.SetValue(False),
            call.replace_dashes.SetValue(True),
            call.replace_hyphens.SetValue(True),
            call.hyphen_at_end.SetValue(True),
            call.en_dash.SetValue(True),
        ]

        LOG.info("\u2009.\u2009.\u2009.\u2009, continuous")
        self.app.settings.latest_config.ellipses.new = "\u2009.\u2009.\u2009.\u2009"
        self.app.settings.latest_config.headings.header_footer_after_break = True
        self.app.settings.latest_config.headings.break_before_heading = (
            PaginationType.CONTINUOUS
        )
        panel.refresh_contents()
        expect += [
            call.refresh_contents(),
            call.base_refresh_contents(),
            call.double.SetValue(True),
            call.leading.SetValue(True),
            call.trailing.SetValue(True),
            call.italic.SetValue(True),
            call.quotes.SetValue(True),
            call.blank.SetValue(True),
            call.replace_divider.SetValue(True),
            call.divider.Enable(True),
            call.divider.SetValue("# # #"),
            call.replace_ellipses.SetValue(True),
            call.ellipses1.Enable(True),
            call.ellipses1_text.Enable(True),
            call.ellipses2.Enable(True),
            call.ellipses2_text.Enable(True),
            call.ellipses3.Enable(True),
            call.ellipses3_text.Enable(True),
            call.ellipses4.Enable(True),
            call.ellipses4_text.Enable(True),
            call.ellipses3.SetValue(True),
            call.part_chapter.SetValue(True),
            call.style_end.SetValue(True),
            call.add_end.SetValue(True),
            call.end.Enable(True),
            call.end.SetValue("The End"),
            call.breaks.SetSelection(0),
            call.indent.SetValue(False),
            call.replace_dashes.SetValue(True),
            call.replace_hyphens.SetValue(True),
            call.hyphen_at_end.SetValue(True),
            call.en_dash.SetValue(True),
        ]

        LOG.info("next page (head/foot)")
        self.app.settings.latest_config.headings.header_footer_after_break = True
        self.app.settings.latest_config.headings.break_before_heading = (
            PaginationType.NEW_PAGE
        )
        panel.refresh_contents()
        expect += [
            call.refresh_contents(),
            call.base_refresh_contents(),
            call.double.SetValue(True),
            call.leading.SetValue(True),
            call.trailing.SetValue(True),
            call.italic.SetValue(True),
            call.quotes.SetValue(True),
            call.blank.SetValue(True),
            call.replace_divider.SetValue(True),
            call.divider.Enable(True),
            call.divider.SetValue("# # #"),
            call.replace_ellipses.SetValue(True),
            call.ellipses1.Enable(True),
            call.ellipses1_text.Enable(True),
            call.ellipses2.Enable(True),
            call.ellipses2_text.Enable(True),
            call.ellipses3.Enable(True),
            call.ellipses3_text.Enable(True),
            call.ellipses4.Enable(True),
            call.ellipses4_text.Enable(True),
            call.ellipses3.SetValue(True),
            call.part_chapter.SetValue(True),
            call.style_end.SetValue(True),
            call.add_end.SetValue(True),
            call.end.Enable(True),
            call.end.SetValue("The End"),
            call.breaks.SetSelection(1),
            call.indent.SetValue(False),
            call.replace_dashes.SetValue(True),
            call.replace_hyphens.SetValue(True),
            call.hyphen_at_end.SetValue(True),
            call.en_dash.SetValue(True),
        ]

        mock.assert_has_calls(expect)

    @patch("style_stripper.model.content_panel.ContentPanel.is_current_panel")
    @note_func("grab_contents")
    def test_grab_contents(self, is_current_panel):
        """Should update the settings"""
        panel = self.window
        mock = panel._the_mock
        content_panel.ContentPanel.refresh_contents = mock.base_refresh_contents
        self.app.settings = Settings()

        LOG.info("Default unchanged")
        for field, value in [
            ("double", True),
            ("leading", True),
            ("trailing", True),
            ("italic", True),
            ("quotes", True),
            ("blank", True),
            ("replace_divider", True),
            ("divider", "# # #"),
            ("replace_ellipses", True),
            ("ellipses1", False),
            ("ellipses2", False),
            ("ellipses3", True),
            ("ellipses4", False),
            ("part_chapter", True),
            ("style_end", True),
            ("add_end", True),
            ("end", "The End"),
            ("indent", False),
            ("replace_dashes", True),
            ("replace_hyphens", True),
            ("hyphen_at_end", True),
            ("en_dash", False),
            ("em_dash", True),
        ]:
            getattr(panel, field).GetValue.return_value = value
        panel.breaks.GetSelection.return_value = 3
        panel.grab_contents()
        mock.config(deepcopy(self.app.settings.latest_config))
        expect = [
            call.grab_contents(),
            call.double.GetValue(),
            call.leading.GetValue(),
            call.trailing.GetValue(),
            call.italic.GetValue(),
            call.quotes.GetValue(),
            call.blank.GetValue(),
            call.replace_divider.GetValue(),
            call.divider.GetValue(),
            call.replace_ellipses.GetValue(),
            call.ellipses1.GetValue(),
            call.ellipses2.GetValue(),
            call.ellipses3.GetValue(),
            call.part_chapter.GetValue(),
            call.style_end.GetValue(),
            call.add_end.GetValue(),
            call.end.GetValue(),
            call.breaks.GetSelection(),
            call.indent.GetValue(),
            call.replace_dashes.GetValue(),
            call.replace_hyphens.GetValue(),
            call.hyphen_at_end.GetValue(),
            call.en_dash.GetValue(),
            call.em_dash.GetValue(),
            call.config(
                ConfigSettings(
                    SpacesConfig(True, True, True),
                    ItalicConfig(True),
                    QuotesConfig(True),
                    DividerConfig(True, True, "# # #"),
                    EllipsesConfig(True, "\u200a.\u200a.\u200a.\u200a"),
                    HeadingsConfig(
                        True, True, True, "The End", False, PaginationType.ODD_PAGE
                    ),
                    DashesConfig(True, False, True, True, True),
                    StylingConfig(False),
                )
            ),
        ]

        LOG.info("Change everything")
        for field, value in [
            ("double", False),
            ("leading", False),
            ("trailing", False),
            ("italic", False),
            ("quotes", False),
            ("blank", False),
            ("replace_divider", False),
            ("divider", "* * *"),
            ("replace_ellipses", False),
            ("ellipses1", True),
            ("ellipses2", False),
            ("ellipses3", False),
            ("ellipses4", False),
            ("part_chapter", False),
            ("style_end", False),
            ("add_end", False),
            ("end", "fin"),
            ("indent", True),
            ("replace_dashes", False),
            ("replace_hyphens", False),
            ("hyphen_at_end", False),
            ("en_dash", True),
            ("em_dash", False),
        ]:
            getattr(panel, field).GetValue.return_value = value
        panel.breaks.GetSelection.return_value = 0
        panel.grab_contents()
        mock.config(deepcopy(self.app.settings.latest_config))
        expect_config = ConfigSettings(
            SpacesConfig(False, False, False),
            ItalicConfig(False),
            QuotesConfig(False),
            DividerConfig(False, False, "* * *"),
            EllipsesConfig(False, "..."),
            HeadingsConfig(False, False, False, "fin", True, PaginationType.CONTINUOUS),
            DashesConfig(False, True, False, False, False),
            StylingConfig(True),
        )
        expect += [
            call.grab_contents(),
            call.double.GetValue(),
            call.leading.GetValue(),
            call.trailing.GetValue(),
            call.italic.GetValue(),
            call.quotes.GetValue(),
            call.blank.GetValue(),
            call.replace_divider.GetValue(),
            call.replace_divider.GetValue(),
            call.divider.GetValue(),
            call.replace_ellipses.GetValue(),
            call.replace_ellipses.GetValue(),
            call.ellipses1.GetValue(),
            call.part_chapter.GetValue(),
            call.style_end.GetValue(),
            call.add_end.GetValue(),
            call.add_end.GetValue(),
            call.end.GetValue(),
            call.breaks.GetSelection(),
            call.indent.GetValue(),
            call.replace_dashes.GetValue(),
            call.replace_hyphens.GetValue(),
            call.hyphen_at_end.GetValue(),
            call.en_dash.GetValue(),
            call.em_dash.GetValue(),
            call.App.book.modified(),
            call.App.refresh_contents(),
            call.config(deepcopy(expect_config)),
        ]

        LOG.info("…, new page (head/foot)")
        panel.ellipses1.GetValue.return_value = False
        panel.ellipses2.GetValue.return_value = True
        panel.breaks.GetSelection.return_value = 1
        panel.grab_contents()
        mock.config(deepcopy(self.app.settings.latest_config))
        expect_config.ellipses.new = "…"
        expect_config.headings.break_before_heading = PaginationType.NEW_PAGE
        expect += [
            call.grab_contents(),
            call.double.GetValue(),
            call.leading.GetValue(),
            call.trailing.GetValue(),
            call.italic.GetValue(),
            call.quotes.GetValue(),
            call.blank.GetValue(),
            call.replace_divider.GetValue(),
            call.divider.GetValue(),
            call.replace_ellipses.GetValue(),
            call.ellipses1.GetValue(),
            call.ellipses2.GetValue(),
            call.part_chapter.GetValue(),
            call.style_end.GetValue(),
            call.add_end.GetValue(),
            call.end.GetValue(),
            call.breaks.GetSelection(),
            call.indent.GetValue(),
            call.replace_dashes.GetValue(),
            call.replace_hyphens.GetValue(),
            call.hyphen_at_end.GetValue(),
            call.en_dash.GetValue(),
            call.em_dash.GetValue(),
            call.App.book.modified(),
            call.config(deepcopy(expect_config)),
        ]

        LOG.info("\u2009.\u2009.\u2009.\u2009, new page (no head/foot)")
        panel.ellipses2.GetValue.return_value = False
        panel.ellipses4.GetValue.return_value = True
        panel.breaks.GetSelection.return_value = 2
        panel.grab_contents()
        mock.config(deepcopy(self.app.settings.latest_config))
        expect_config.ellipses.new = "\u2009.\u2009.\u2009.\u2009"
        expect_config.headings.header_footer_after_break = False
        expect += [
            call.grab_contents(),
            call.double.GetValue(),
            call.leading.GetValue(),
            call.trailing.GetValue(),
            call.italic.GetValue(),
            call.quotes.GetValue(),
            call.blank.GetValue(),
            call.replace_divider.GetValue(),
            call.divider.GetValue(),
            call.replace_ellipses.GetValue(),
            call.ellipses1.GetValue(),
            call.ellipses2.GetValue(),
            call.ellipses3.GetValue(),
            call.ellipses4.GetValue(),
            call.part_chapter.GetValue(),
            call.style_end.GetValue(),
            call.add_end.GetValue(),
            call.end.GetValue(),
            call.breaks.GetSelection(),
            call.indent.GetValue(),
            call.replace_dashes.GetValue(),
            call.replace_hyphens.GetValue(),
            call.hyphen_at_end.GetValue(),
            call.en_dash.GetValue(),
            call.em_dash.GetValue(),
            call.App.book.modified(),
            call.config(deepcopy(expect_config)),
        ]

        LOG.info("even page")
        panel.breaks.GetSelection.return_value = 4
        panel.grab_contents()
        expect_config.headings.break_before_heading = PaginationType.EVEN_PAGE
        mock.config(deepcopy(self.app.settings.latest_config))
        expect += [
            call.grab_contents(),
            call.double.GetValue(),
            call.leading.GetValue(),
            call.trailing.GetValue(),
            call.italic.GetValue(),
            call.quotes.GetValue(),
            call.blank.GetValue(),
            call.replace_divider.GetValue(),
            call.divider.GetValue(),
            call.replace_ellipses.GetValue(),
            call.ellipses1.GetValue(),
            call.ellipses2.GetValue(),
            call.ellipses3.GetValue(),
            call.ellipses4.GetValue(),
            call.part_chapter.GetValue(),
            call.style_end.GetValue(),
            call.add_end.GetValue(),
            call.end.GetValue(),
            call.breaks.GetSelection(),
            call.indent.GetValue(),
            call.replace_dashes.GetValue(),
            call.replace_hyphens.GetValue(),
            call.hyphen_at_end.GetValue(),
            call.en_dash.GetValue(),
            call.em_dash.GetValue(),
            call.App.book.modified(),
            call.config(deepcopy(expect_config)),
        ]

        mock.assert_has_calls(expect)
