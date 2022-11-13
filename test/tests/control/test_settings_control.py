from mock_wx import wxTestCase, note_func

import logging
import pickle
from unittest.mock import call
import wx

from style_stripper.control import settings_control

# Constants:
LOG = logging.getLogger(__name__)
B64 = (
    b"gASVygMAAAAAAACMJ3N0eWxlX3N0cmlwcGVyLmNvbnRyb2wuc2V0dGluZ3NfY29udHJvbJSMCFNldHRpbmdzlJOUKYGUfZQojAt3aW5kb3dfcmVjd"
    b"JQoSwpLFEseSyh0lIwJbWF4aW1pemVklImMDGZpbGVfdmVyc2lvbpRLAYwNbGF0ZXN0X2NvbmZpZ5RoAIwOQ29uZmlnU2V0dGluZ3OUk5QpgZR9lC"
    b"iMBnNwYWNlc5RoAIwMU3BhY2VzQ29uZmlnlJOUKYGUfZQojAxwdXJnZV9kb3VibGWUiIwNcHVyZ2VfbGVhZGluZ5SIjA5wdXJnZV90cmFpbGluZ5S"
    b"IdWKMBml0YWxpY5RoAIwMSXRhbGljQ29uZmlnlJOUKYGUfZSMHWFkanVzdF90b19pbmNsdWRlX3B1bmN0dWF0aW9ulIhzYowGcXVvdGVzlGgAjAxR"
    b"dW90ZXNDb25maWeUk5QpgZR9lIwQY29udmVydF90b19jdXJseZSIc2KMB2RpdmlkZXKUaACMDURpdmlkZXJDb25maWeUk5QpgZR9lCiMG2JsYW5rX"
    b"3BhcmFncmFwaF9pZl9ub19vdGhlcpSIjBByZXBsYWNlX3dpdGhfbmV3lIiMA25ld5SMBSMgIyAjlHVijAhlbGxpcHNlc5RoAIwORWxsaXBzZXNDb2"
    b"5maWeUk5QpgZR9lChoKIhoKYwP4oCKLuKAii7igIou4oCKlHVijAhoZWFkaW5nc5RoAIwOSGVhZGluZ3NDb25maWeUk5QpgZR9lCiMF3N0eWxlX3B"
    b"hcnRzX2FuZF9jaGFwdGVylIiMDXN0eWxlX3RoZV9lbmSUiIwLYWRkX3RoZV9lbmSUiIwHdGhlX2VuZJSMB1RoZSBFbmSUjBloZWFkZXJfZm9vdGVy"
    b"X2FmdGVyX2JyZWFrlImMFGJyZWFrX2JlZm9yZV9oZWFkaW5nlIwZc3R5bGVfc3RyaXBwZXIuZGF0YS5lbnVtc5SMDlBhZ2luYXRpb25UeXBllJOUS"
    b"wWFlFKUdWKMBmRhc2hlc5RoAIwMRGFzaGVzQ29uZmlnlJOUKYGUfZQojA5jb252ZXJ0X2RvdWJsZZSIjBJjb252ZXJ0X3RvX2VuX2Rhc2iUiYwSY2"
    b"9udmVydF90b19lbV9kYXNolIiME2ZpeF9hdF9lbmRfb2ZfcXVvdGWUiIwSZm9yY2VfYWxsX2VuX29yX2VtlIh1YowHc3R5bGluZ5RoAIwNU3R5bGl"
    b"uZ0NvbmZpZ5STlCmBlH2UjBZpbmRlbnRfZmlyc3RfcGFyYWdyYXBolIlzYnVidWIu"
)


class TestSettingsControl(wxTestCase):
    def setUp(self) -> None:
        self.app = wx.App()
        self.window = settings_control.SettingsControl(self.app)

    @note_func("load_settings")
    def test_load_settings(self):
        """Should load settings"""
        control = self.window
        mock = self.app._the_mock

        LOG.info("Load success")
        wx.FileConfig._patch(".Read.return_value = %r" % B64)
        control.load_settings()
        mock.window_rect(self.app.settings.window_rect)
        expect = [
            call.load_settings(),
            call.FileConfig("StyleStripper"),
            call.FileConfig.Read("configuration", ""),
            call.window_rect((10, 20, 30, 40)),
        ]

        LOG.info("Load error")
        wx.FileConfig._patch(".Read.return_value = %r" % "not a valid B64 string")
        control.load_settings()
        mock.window_rect(self.app.settings.window_rect)
        expect += [
            call.load_settings(),
            call.FileConfig("StyleStripper"),
            call.FileConfig.Read("configuration", ""),
            call.window_rect(None),
        ]

        mock.assert_has_calls(expect)

    @note_func("save_settings_on_exit")
    def test_save_settings_on_exit(self):
        """Should cope with maximized windows on exit"""
        control = self.window
        mock = self.app._the_mock
        event = wx.CloseEvent()

        LOG.info("First pass, maximized")
        control.save_settings_on_exit(event)
        expect = [
            call.save_settings_on_exit(event),
            call.App.book.not_modified(),
            call.App.frame.IsMaximized(),
            call.App.frame.Maximize(False),
            call.CallLater(100, control.save_settings_on_exit2, True),
        ]

        LOG.info("Second pass, no longer maximized")
        control.save_settings_on_exit(event)
        expect += [
            call.save_settings_on_exit(event),
            call.App.book.not_modified(),
            call.App.frame.IsMaximized(),
            call.App.frame.Maximize(False),
            call.CallLater(100, control.save_settings_on_exit2, True),
        ]

        mock.assert_has_calls(expect)

    @note_func("save_settings_on_exit2")
    def test_save_settings_on_exit2(self):
        """Should save settings on exit"""
        control = self.window
        mock = self.app._the_mock
        self.app.frame.GetRect.return_value = (10, 20, 30, 40)
        self.app.settings = settings_control.Settings()

        LOG.info("Don't close the frame")
        control.save_settings_on_exit2(False)
        expect = [
            call.save_settings_on_exit2(False),
            call.App.frame.GetRect(),
            call.FileConfig("StyleStripper"),
            call.FileConfig.Write("configuration", B64),
        ]

        LOG.info("Close the frame")
        control.save_settings_on_exit2(True)
        expect += [
            call.save_settings_on_exit2(True),
            call.App.frame.GetRect(),
            call.FileConfig("StyleStripper"),
            call.FileConfig.Write("configuration", B64),
            call.App.frame.Close(),
        ]

        mock.assert_has_calls(expect)

    def test_upgrade(self):
        """Should upgrade old version to the latest"""
        latest_version = 1
        ver1_pickle = (
            b"\x80\x04\x95\xc0\x03\x00\x00\x00\x00\x00\x00\x8c'style_stripper.control.settings_control\x94\x8c\x08Setti"
            b"ngs\x94\x93\x94)\x81\x94}\x94(\x8c\x0bwindow_rect\x94N\x8c\tmaximized\x94\x89\x8c\x0cfile_version\x94K"
            b"\x01\x8c\rlatest_config\x94h\x00\x8c\x0eConfigSettings\x94\x93\x94)\x81\x94}\x94(\x8c\x06spaces\x94h\x00"
            b"\x8c\x0cSpacesConfig\x94\x93\x94)\x81\x94}\x94(\x8c\x0cpurge_double\x94\x88\x8c\rpurge_leading\x94\x88"
            b"\x8c\x0epurge_trailing\x94\x88ub\x8c\x06italic\x94h\x00\x8c\x0cItalicConfig\x94\x93\x94)\x81\x94}\x94\x8c"
            b"\x1dadjust_to_include_punctuation\x94\x88sb\x8c\x06quotes\x94h\x00\x8c\x0cQuotesConfig\x94\x93\x94)\x81"
            b"\x94}\x94\x8c\x10convert_to_curly\x94\x88sb\x8c\x07divider\x94h\x00\x8c\rDividerConfig\x94\x93\x94)\x81"
            b"\x94}\x94(\x8c\x1bblank_paragraph_if_no_other\x94\x88\x8c\x10replace_with_new\x94\x88\x8c\x03new\x94\x8c"
            b"\x05# # #\x94ub\x8c\x08ellipses\x94h\x00\x8c\x0eEllipsesConfig\x94\x93\x94)\x81\x94}\x94(h'\x88h(\x8c\x0f"
            b"\xe2\x80\x8a.\xe2\x80\x8a.\xe2\x80\x8a.\xe2\x80\x8a\x94ub\x8c\x08headings\x94h\x00\x8c\x0eHeadingsConfig"
            b"\x94\x93\x94)\x81\x94}\x94(\x8c\x17style_parts_and_chapter\x94\x88\x8c\rstyle_the_end\x94\x88\x8c\x0badd_"
            b"the_end\x94\x88\x8c\x07the_end\x94\x8c\x07The End\x94\x8c\x19header_footer_after_break\x94\x89\x8c\x14bre"
            b"ak_before_heading\x94\x8c\x19style_stripper.data.enums\x94\x8c\x0ePaginationType\x94\x93\x94K\x05\x85\x94"
            b"R\x94ub\x8c\x06dashes\x94h\x00\x8c\x0cDashesConfig\x94\x93\x94)\x81\x94}\x94(\x8c\x0econvert_double\x94"
            b"\x88\x8c\x12convert_to_en_dash\x94\x89\x8c\x12convert_to_em_dash\x94\x88\x8c\x13fix_at_end_of_quote\x94"
            b"\x88\x8c\x12force_all_en_or_em\x94\x88ub\x8c\x07styling\x94h\x00\x8c\rStylingConfig\x94\x93\x94)\x81\x94}"
            b"\x94\x8c\x16indent_first_paragraph\x94\x89sbubub.")
        upgraded = pickle.loads(ver1_pickle).init()
        assert upgraded.file_version == latest_version
        # Add more tests to catch what has been set in upgrade
