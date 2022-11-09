from mock_wx import wxTestCase, note_func

import logging
from unittest.mock import call, patch
import wx

from style_stripper.data.enums import PaginationType
from style_stripper.control.settings_control import Settings
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
